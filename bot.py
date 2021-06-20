import discord
from discord.ext import commands
import logging
from mongokit_ng import Connection
import secrets

import character_controller
import party_controller
import delve_controller
from character import Character
from armor import Armor
from consumable import Consumable
from weapon import Weapon

#   LOGGING CONFIG   #
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#   DB CONFIG   #
connection = Connection(secrets.MONGODB_URI)
connection.register([Character])
connection.register([Armor])
connection.register([Consumable])
connection.register([Weapon])

#   BOT CONFIG   #
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix='\\', intents=intents)
bot.add_cog(character_controller.CharacterController(bot, connection))
bot.add_cog(party_controller.PartyController(bot))
bot.add_cog(delve_controller.DelveController(bot, connection))


@bot.check
def check_guild_member(ctx):
    """Bot should only respond to game commands from guild members."""
    return ctx.author in bot.get_all_members()


#   BASIC COMMANDS   #
@bot.event
async def on_ready():
    encampment = bot.get_channel(secrets.encampment_channel_id)
    await encampment.send(':hammer_pick: **DELVE RPG** :crossed_swords:\nGame server is online.')


@bot.event
async def on_disconnect():
    encampment = bot.get_channel(secrets.encampment_channel_id)
    await encampment.send(':hammer_pick: ~~**DELVE RPG**~~ :crossed_swords:\nGame server has temporarily lost connection.')


@bot.event
async def on_resumed():
    encampment = bot.get_channel(secrets.encampment_channel_id)
    await encampment.send(':hammer_pick: **DELVE RPG** :crossed_swords:\nGame server has reconnected.')

#   STARTUP   #
bot.run(secrets.client_token)
