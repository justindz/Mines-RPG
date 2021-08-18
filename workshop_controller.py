from discord.ext import commands, tasks
import random

import gemstone
import utilities
from item import socket_gemstone
from secrets import workshop_channel_id


class WorkshopController(commands.Cog):
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.banter.start()
        self.get = self.bot.get_cog('CharacterController').get
        self.name = 'Emma'

    #  CHECKS  #
    async def check_idle(ctx):
        delves = ctx.bot.get_cog('DelveController').delves

        for channel_name in delves.keys():
            delve = delves[channel_name]

            if ctx.author in delve.players and delve.status != 'idle':
                return False

        return True

    async def check_workshop_channel(ctx):
        if ctx.channel.id == workshop_channel_id:
            return True

        return False

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

    @commands.command()
    @commands.check(check_idle)
    @commands.check(check_workshop_channel)
    async def socket(self, ctx, gemstone_index: int, item_index: int):
        """Socket a gemstone into an unequipped weapon or armor in your inventory with an open socket. The change is irreversible. You must be a Jeweler to use this crafting option."""
        character = self.get(ctx.author)
        workshop_channel = self.bot.get_channel(workshop_channel_id)
        gem = None
        item = None

        try:
            gem = character.inventory[gemstone_index]
            item = character.inventory[item_index]

            if gem['_itype'] != 12:
                await ctx.author.send(utilities.red('That is not a gemstone.'))
                return
            if item['_itype'] not in [1, 2, 3, 5, 6]:
                await ctx.author.send(utilities.red('That is not a socketable item.'))
                return
        except IndexError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))

        if not gemstone.usable_in(gem, item):
            await ctx.author.send(utilities.yellow(f'{gem["name"]} cannot be applied to this item type.'))
            return

        if socket_gemstone(self.connection, item, gem):
            character.remove_from_inventory(gem)
            await workshop_channel.send(f'{ctx.author.name} improved their {item["name"]}, adding: {gem["name"]}.')
        else:
            await ctx.author.send(utilities.yellow(f'{item["name"]} has no open sockets.'))


monolog = [
    "Hmmm.",
]

monolog_rare = [
    "Fuck!",
]
