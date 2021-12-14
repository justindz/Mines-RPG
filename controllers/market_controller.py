from discord.ext import commands, tasks
import random

import utilities
from secrets import market_channel_id


class MarketController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banter.start()
        self.get = self.bot.get_cog('CharacterController').get
        self.name = 'Bigsby'
        self.buy_rate = 0.5
        self.sell_rate = 1.25

    #  CHECKS  #
    async def check_market_channel(ctx):
        if ctx.channel.id == market_channel_id:
            return True

        return False

    async def check_not_delving(ctx):
        delves = ctx.bot.get_cog('DelveController').delves
        for delve in delves:
            if ctx.author in delve.players:
                return False

        return True

    #  COMMANDS  #
    def cog_unload(self):
        self.banter.cancel()

    @tasks.loop(seconds=180.0)
    async def banter(self):
        self.banter.change_interval(seconds=480.0 + random.uniform(0.0, 120.0))
        market_channel = self.bot.get_channel(market_channel_id)
        last_message = await market_channel.history(limit=1).flatten()

        if last_message[0].content.startswith(f'{self.name}'):
            return

        rare = False

        if random.randint(1, 100) <= 1:
            rare = True

        if rare:
            await market_channel.send(f'{self.name} says, "{random.choice(monolog_rare)}"')
        else:
            await market_channel.send(f'{self.name} says, "{random.choice(monolog)}"')

    @banter.before_loop
    async def before_banter(self):
        await self.bot.wait_until_ready()

    @commands.command()
    @commands.check(check_market_channel)
    @commands.check(check_not_delving)
    async def list(self, ctx):
        """Display the NPC vendor's current inventory."""
        character = self.get(ctx.author)
        out = f'=========={self.name}\'s Inventory==========='
        i = 0

        for item in character.shop:
            out += f'\n{i} - {item.name} ({int(item.value * self.sell_rate)}c)'
            i += 1

        await ctx.author.send(out)

    @commands.command()
    @commands.check(check_market_channel)
    @commands.check(check_not_delving)
    async def buy(self, ctx, index: int):
        """Buy a listed item from the NPC vendor."""
        character = self.get(ctx.author)

        try:
            item = character.shop[index]
            price = int(item.value * self.sell_rate)

            if character.coins >= price:
                if character.add_to_inventory(item, False):
                    character.coins -= price
                    character.shop.remove(item)
                    character.save()
                    await ctx.channel.send(f'{character.name} bought: {item.name}')
                else:
                    await ctx.author.send(utilities.yellow('You are carrying too much to buy that.'))
            else:
                await ctx.author.send(f'{self.name} informs you, sharply, that you are too poor to afford that.')
        except IndexError:
            await ctx.author.send(utilities.red('Invalid shop inventory position.'))

    @commands.command()
    @commands.check(check_market_channel)
    @commands.check(check_not_delving)
    async def offer(self, ctx, index: int):
        """Ask how much the NPC vendor will pay for an item in your inventory."""
        character = self.get(ctx.author)

        try:
            item = character.inventory[index]
            n = item.name  # TODO is this needed?
            offer = int(item.value * self.buy_rate)
            await ctx.channel.send(f'{self.name} says, "I\'d give you {offer} coins for your {n}, {character.name}."')
        except KeyError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))

    @commands.command()
    @commands.check(check_market_channel)
    @commands.check(check_not_delving)
    async def sell(self, ctx, index: int):
        """Sell an item to the NPC vendor. Sold item_specs cannot be bought back."""
        character = self.get(ctx.author)

        try:
            item = character.inventory[index]
            n = item.name  # TODO is this needed?
            offer = int(item.value * self.buy_rate)
            character.coins += offer
            character.remove_from_inventory(item, False)
            # item.delete()
            await ctx.channel.send(f'{character.name} sold {n} to {self.name} for {offer} coins."')
        except KeyError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))

    @commands.command()
    @commands.check(check_market_channel)
    @commands.check(check_not_delving)
    async def bank(self, ctx):
        """View a list of the item_specs stored in your bank."""
        character = self.get(ctx.author)
        out = f'=========={character.name}\'s Storage==========='
        i = 0

        for item in character.bank:
            out += f'\n{i} - {item.name}'
            i += 1

        await ctx.author.send(out)

    @commands.command()
    @commands.check(check_market_channel)
    @commands.check(check_not_delving)
    async def deposit(self, ctx, index: int):
        """Deposit an item into your bank from your inventory."""
        character = self.get(ctx.author)

        try:
            name = character.inventory[index].name
        except IndexError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))
            return

        if len(character.bank) >= character.bank_limit:
            await ctx.author.send(utilities.yellow(f'Your bank account is at the current limit of {character.bank_limit} item_specs.'))
        elif character.deposit(index):
            await ctx.channel.send(f'{character.name} deposited {name} to the bank.')

    @commands.command()
    @commands.check(check_market_channel)
    @commands.check(check_not_delving)
    async def withdraw(self, ctx, index: int):
        """Add an item from your bank to your inventory. This action costs 1 coin per item in your bank account."""
        character = self.get(ctx.author)

        try:
            name = character.bank[index].name
        except IndexError:
            await ctx.author.send(utilities.red('Invalid bank position.'))
            return

        if character.coins < len(character.bank):
            await ctx.author.send(utilities.yellow(f'You need {len(character.bank)} coins to pay your withdrawal fee.'))
        elif character.withdraw(index):
            await ctx.channel.send(f'{character.name} withdrew {name} from the bank.')
        else:
            await ctx.author.send(utilities.red(f'Unable to withdraw an item. You may be at maximum carry weight.'))


monolog = [
    "Have fun toiling in the mines. I'll just be here. Making money.",
    "Skill manuals! Spell scrolls! Everything you need to delay your own demise!",
    "Turn your trash into treasures right here, friends. Very, very slowly.",
    "Deals are my art form.",
    "Introducing our new installment plan. How many installments, you ask? One!",
    "I have the lowest/only prices in the region!",
    "Bigsby beats the competition in every way, including existing!",
    "Return policy? You can return to wherever you came from.",
    "W... warr... warranty? Not familiar with the word.",
    "Ten percent of nothin' is... let me do the math here...",
    "Bigsby buys everything! Except livers.",
    "Do you see this sign? The one that says 'Discounts' with the big red X through it?",
]

monolog_rare = [
    "I'm not trying to be sexy. It's just my way of expressing myself when I move around.",
    "And what do we say to Death? 'If only I had bought that upgrade from Bigsby. Argh!' *gurgling noises*",
    "Today only: the Euler's identity discount!",
]
