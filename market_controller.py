import asyncio
import discord
from discord.ext import commands, tasks
import random

import utilities
from secrets import market_channel_id


class MarketController(commands.Cog):
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.banter.start()
        self.get = self.bot.get_cog('CharacterController').get
        self.name = 'Bigsby'
        self.buy_rate = 0.5

    #  CHECKS  #
    async def check_idle(ctx):
        delves = ctx.bot.get_cog('DelveController').delves

        for channel_name in delves.keys():
            delve = delves[channel_name]

            if ctx.author in delve.players and delve.status != 'idle':
                return False

        return True

    async def check_market_channel(ctx):
        if ctx.channel.id == market_channel_id:
            return True

        return False

    #  COMMANDS  #
    def cog_unload(self):
        self.banter.cancel()

    @tasks.loop(seconds=180.0)
    async def banter(self):
        self.banter.change_interval(seconds=480.0 + random.uniform(0.0, 120.0))
        market_channel = self.bot.get_channel(market_channel_id)
        rare = False

        if random.randint(1, 100) <= 1:
            rare = True

        if rare:
            await market_channel.send('{} says, "{}"'.format(self.name, random.choice(monolog_rare)))
        else:
            await market_channel.send('{} says, "{}"'.format(self.name, random.choice(monolog)))

    @banter.before_loop
    async def before_banter(self):
        await self.bot.wait_until_ready()

    @commands.command()
    @commands.check(check_idle)
    @commands.check(check_market_channel)
    async def list(self, ctx):
        """Display the NPC vendor's current inventory."""
        character = self.get(ctx.author)

    @commands.command()
    @commands.check(check_idle)
    @commands.check(check_market_channel)
    async def buy(self, ctx, index: int):
        """Buy a listed item from the NPC vendor."""
        character = self.get(ctx.author)

    @commands.command()
    @commands.check(check_idle)
    @commands.check(check_market_channel)
    async def offer(self, ctx, index: int):
        """Ask how much the NPC vendor will pay for an item in your inventory."""
        character = self.get(ctx.author)

        try:
            item = character.inventory[index]
            n = item['name']
            offer = int(item['value'] * self.buy_rate)
            await ctx.channel.send(f'{self.name} says, "I\'d give you {offer} coins for your {n}, {character.name}."')
        except KeyError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))

    @commands.command()
    @commands.check(check_idle)
    @commands.check(check_market_channel)
    async def sell(self, ctx, index: int):
        """Sell an item to the NPC vendor. Sold items cannot be bought back."""
        character = self.get(ctx.author)

        try:
            item = character.inventory[index]
            n = item['name']
            offer = int(item['value'] * self.buy_rate)
            character.coins += offer
            character.remove_from_inventory(item, False)
            await ctx.channel.send(f'{character.name} sold {n} to {self.name} for {offer} coins."')
        except KeyError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))


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
