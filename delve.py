import discord

from zone import Zone
from character import Character


class Delve(object):
    def __init__(self, bot, leader: discord.Member, players: [discord.Member], zone: Zone, channel: discord.TextChannel, restart: bool):
        self.bot = bot
        self.leader = leader
        self.players = players
        self.players.append(leader)
        self.characters = []
        cc = bot.get_cog('CharacterController')

        for player in players:
            char = cc.get(player)
            char.reset_stats()
            self.characters.append(char)

        self.zone = zone

        if restart:
            leader_char = cc.get(leader)

            if zone.name in leader_char.depths.keys():
                self.depth = zone.get_restart_level(leader_char.get_depth_progress(zone.name))
        else:
            self.depth = 1

        self.solo = True if len(players) == 1 else False
        self.channel = channel
        self.current_room = self.zone.get_next_room(self.characters, self.depth)
        self.status = 'idle'  # idle, fighting

    def proceed(self):
        self.depth += 1
        self.current_room = self.zone.get_next_room(self.characters, self.depth)

    async def remove_player(self, player: discord.Member):
        self.players.remove(player)
        leader = None

        for character in self.characters:
            if character.name == player.name:
                self.characters.remove(character)
                break

        if player == self.leader:
            leader = self.players[0]

        await self.channel.set_permissions(player, overwrite=None)
        return leader.name

    async def remove_character(self, character: Character):
        leader_name = await self.remove_player(character.player)
        return leader_name
