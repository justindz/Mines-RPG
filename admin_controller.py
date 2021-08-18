from discord.ext import commands

from secrets import admins
from item import generate_random_item


class AdminController(commands.Cog):
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.get = self.bot.get_cog('CharacterController').get

    #  CHECKS  #
    async def check_if_admin(ctx):
        return True if ctx.author.id in admins else False

    #  COMMANDS  #
    @commands.command(hidden=True)
    @commands.check(check_if_admin)
    async def spawn_test_items(self, ctx, level: int):
        character = self.get(ctx.author)

        for _ in range(1, 10):
            character.add_to_inventory(generate_random_item(self.connection, level), False)
