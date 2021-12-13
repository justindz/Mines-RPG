from discord.ext import commands

from secrets import admins
from item_factory import generate_random_item, generate_book


class AdminController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
            character.add_to_inventory(generate_random_item(level), False)

    @commands.command(hidden=True)
    @commands.check(check_if_admin)
    async def spawn_book(self, ctx, key: str):
        character = self.get(ctx.author)
        book = generate_book(key)

        if book is not None:
            character.add_to_inventory(book, False)

    @commands.command(hidden=True)
    @commands.check(check_if_admin)
    async def add_points(self, ctx, points: int):
        character = self.get(ctx.author)
        character.points += points
        character.save()
