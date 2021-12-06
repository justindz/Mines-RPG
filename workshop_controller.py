from discord.ext import commands, tasks
import random

import gemstone
import utilities
from item_factory import socket_gemstone
from consumable import create_consumable
from secrets import workshop_channel_id


class WorkshopController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banter.start()
        self.get = self.bot.get_cog('CharacterController').get
        self.name = 'Emma'

    #  CHECKS  #
    async def check_workshop_channel(ctx):
        if ctx.channel.id == workshop_channel_id:
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
        workshop_channel = self.bot.get_channel(workshop_channel_id)
        rare = False

        if random.randint(1, 100) <= 1:
            rare = True

        if rare:
            await workshop_channel.send(f'{self.name} says, "{random.choice(monolog_rare)}"')
        else:
            await workshop_channel.send(f'{self.name} says, "{random.choice(monolog)}"')

    @banter.before_loop
    async def before_banter(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=['profs', 'trades', 'trade'])
    @commands.check(check_workshop_channel)
    @commands.check(check_not_delving)
    async def professions(self, ctx):
        """Learn about the available professions."""
        await ctx.author.send(utilities.blue(f'{self.name} says, "{professions_desc}"'))

    @commands.command(aliases=['jeweler'])
    @commands.check(check_workshop_channel)
    @commands.check(check_not_delving)
    async def jewelers(self, ctx):
        """Learn about the jeweler profession."""
        await ctx.author.send(utilities.blue(f'{self.name} says, "{jeweler_desc}"'))

    @commands.command(aliases=['alchemist'])
    @commands.check(check_workshop_channel)
    @commands.check(check_not_delving)
    async def alchemists(self, ctx):
        """Learn about the alchemist profession."""
        await ctx.author.send(utilities.blue(f'{self.name} says, "{alchemist_desc}"'))

    @commands.command(aliases=['cartographer', 'mapmakers', 'mapmaker'])
    @commands.check(check_workshop_channel)
    @commands.check(check_not_delving)
    async def cartographers(self, ctx):
        """Learn about the cartographer profession."""
        await ctx.author.send(utilities.blue(f'{self.name} says, "{cartographer_desc}"'))

    @commands.command()
    @commands.check(check_workshop_channel)
    @commands.check(check_not_delving)
    async def choose(self, ctx, profession: str):
        """Choose a profession: jeweler, alchemist, or cartographer. Note: this choice is difficult to undo!"""
        character = self.get(ctx.author)

        if character.profession != '':
            await ctx.author.send(utilities.yellow(f'You have already chosen the {character.profession} trade.'))
            return

        if profession == 'jeweler':
            character.profession = 'jeweler'
            character.save()
            await self.bot.get_channel(workshop_channel_id).send(
                f'{self.name} announces, "Congratulations to {character.name}, our newest {character.profession}!"')
        elif profession == 'alchemist':
            character.profession = 'alchemist'
            character.save()
            await self.bot.get_channel(workshop_channel_id).send(
                f'{self.name} announces, "Congratulations to {character.name}, our newest {character.profession}!"')
        elif profession == 'cartographer':
            # character.profession = 'cartographer'
            # character.save()
            # await self.bot.get_channel(workshop_channel_id).send(
            #     f'{self.name} announces, "Congratulations to {character.name}, our newest {character.profession}!"')
            await ctx.author.send(utilities.blue(
                f'{self.name} says, "I\'m not currently taking new students in the {profession} trade."'))
        else:
            await ctx.author.send(utilities.blue(
                f'{self.name} says, "I\'m afraid I don\'t know the {profession} trade."'))

    @commands.command()
    @commands.check(check_workshop_channel)
    @commands.check(check_not_delving)
    async def socket(self, ctx, item_index: int, gemstone_index: int):
        """Socket a gemstone into an unequipped weapon or armor in your inventory with an open socket. The change is irreversible. You must be a Jeweler to use this crafting option."""
        character = self.get(ctx.author)

        if character.profession != 'jeweler':
            return

        workshop_channel = self.bot.get_channel(workshop_channel_id)
        gem = None
        item = None

        try:
            gem = character.inventory[gemstone_index]
            item = character.inventory[item_index]

            if gem.itype != 11:
                await ctx.author.send(utilities.red('That is not a gemstone.'))
                return
            if item.itype not in [1, 2, 3, 5, 6]:
                await ctx.author.send(utilities.red('That is not a socketable item.'))
                return
        except IndexError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))

        if character.level < gem.level:
            await ctx.author.send(utilities.yellow('You are not experienced enough to work with this quality of gem.'))
            return

        if not gemstone.usable_in(gem, item):
            await ctx.author.send(utilities.yellow(f'{gem.name} cannot be applied to this item type.'))
            return

        if socket_gemstone(item, gem):
            character.remove_from_inventory(gem)
            await workshop_channel.send(f'{ctx.author.name} improved their {item.name}, adding: {gem.name}.')
        else:
            await ctx.author.send(utilities.yellow(f'{item.name} has no open sockets.'))

    @commands.command()
    @commands.check(check_workshop_channel)
    @commands.check(check_not_delving)
    async def brew(self, ctx, *indices):
        """Combine up to 3 ingredients to create a potion with deterministic properties depending on the ingredients used. The ingredients are consumed."""
        character = self.get(ctx.author)
        ingredients = []

        if character.profession != 'alchemist':
            return

        workshop_channel = self.bot.get_channel(workshop_channel_id)

        if len(indices) < 1 or len(indices) > 3:
            await ctx.author.send(utilities.yellow(
                'You must provide 1-3 ingredients by inventory position to brew a potion.'))
            return

        try:
            for index in [int(x) for x in indices]:
                ing = character.inventory[index]

                if ing.itype != 12:
                    await ctx.author.send(utilities.red(f'{ing.name} is not an ingredient.'))
                    return

                if ing.level > character.level:
                    await ctx.author.send(
                        utilities.yellow('You are not experienced enough to work with these ingredients.'))
                    return

                ingredients.append(ing)
        except IndexError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))

        consumable = create_consumable(ingredients)

        if consumable is False:
            await workshop_channel.send(utilities.yellow(
                'You must provide 1-3 ingredients by inventory position to brew a potion.'))
            return

        consumable.description = consumable.description.replace('|', character.name)
        consumable.save()

        for ing in ingredients:
            character.remove_from_inventory(ing)

        character.add_to_inventory(consumable, True)
        await workshop_channel.send(f'{ctx.author.name} brewed: {consumable.name}.')


professions_desc = "So, you're interested in learning a trade to practice here in my workshop? Wonderful! At the moment, I'm equipped to support the activities of \\jewelers, \\alchemists, and \\cartographers. When you have made up your mind, you can \\choose a profession. While professions are entirely optional, they can help you in your journey. You can choose your profession at any time, but only once! As you become more experienced in the mines, your capabilities in your chosen profession will improve accordingly."
jeweler_desc = "Jewelers can socket gemstones into weapons and armor, enhancing the item's properties. Items have a limited number of sockets, and gemstones cannot be safely removed, so this profession is not or the anxiety-prone!"
alchemist_desc = "Alchemists can combine specific organic reagants to create restorative potions to aid in exploring the mines. Potions are consumed on use, but can have multiple uses."
cartographer_desc = "Cartographers can use a variety of resources to make modifications to maps discovered in the mines. These modifications affect the risk and reward levels of a delve using the enhanced map, and are consumed. I'm not currently taking new students in this profession."

monolog = [
    "Let me know if you have any questions about the \\professions you can pursue in my workshop.",
    "I suppose if I charged you all to use my workshop, I could afford to eat more often. But... that seems pushy.",
]

monolog_rare = [
    "I highly recommend you don't combine those two ingre... oh.",
]
