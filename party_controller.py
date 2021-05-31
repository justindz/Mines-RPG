import discord
from discord.ext import commands
import asyncio

import utilities
import zone


class PartyController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parties = {}

    def is_player_in_a_party(self, name):
        for party in self.parties:
            if name in party:
                return True

        return False

    async def check_correct_channel(ctx):
        try:
            return ctx.channel.name in ['encampment']
        except AttributeError:  # DMChannel
            return False

    async def check_not_delving(ctx):
        delves = ctx.bot.get_cog('DelveController').delves
        for delve in delves:
            if ctx.author in delve.players:
                return False

        return True

    @commands.command()
    @commands.check(check_correct_channel)
    @commands.check(check_not_delving)
    async def invite(self, ctx, member: discord.Member):
        """Invite another player in the encampment to party up with you. Only the party leader can invite players. Maximum party size is three."""
        if member == ctx.author:
            await ctx.author.send(utilities.yellow('You cannot party with yourself. Well... you know what I mean.'))
            return
        elif ctx.author.name in self.parties.keys():
            if len(self.parties.keys()) > 2:
                await ctx.author.send(utilities.yellow('Your party is full. You cannot invite another player.'))
                return
            elif member.name in self.parties[ctx.author.name]:
                await ctx.author.send(utilities.yellow('{} is already in your party.'.format(member.name)))
                return

        if self.is_player_in_a_party(ctx.author.name):
            await ctx.author.send(utilities.yellow(
                'You are already in a party. If you want to form a party, you will need to \\leave this one.'))
            return

        message = await member.send(
            '{} has invited you to join their party. Thumbs up to accept, or thumbs down to decline.'.format(
                ctx.author.name))
        await message.add_reaction('\N{THUMBS UP SIGN}')
        await message.add_reaction('\N{THUMBS DOWN SIGN}')

        def check(reaction, user):
            return user == member

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

            if str(reaction) == '\N{THUMBS UP SIGN}':
                if ctx.author.name in self.parties.keys():
                    self.parties[ctx.author.name].append(member.name)
                else:
                    self.parties[ctx.author.name] = [member.name]

                await member.send('You are now in a party with {}.'.format(ctx.author.name))
                await ctx.author.send('{} accepted your party invitation.'.format(member.name))
            elif str(reaction) == '\N{THUMBS DOWN SIGN}':
                await ctx.author.send('{} declined your party invitation.'.format(member.name))
        except asyncio.TimeoutError:
            await ctx.author.send('{} did not respond to your party invite.'.format(member.name))

    @commands.command()
    async def party(self, ctx):
        """View your current party."""
        if ctx.author.name in self.parties.keys():
            party_string = '----------PARTY----------\n{} (Leader)\n'.format(ctx.author.name)

            for name in self.parties[ctx.author.name]:
                party_string += '{}\n'.format(name)

            party_string += '-------------------------'
            await ctx.author.send(party_string)
            return
        else:
            for leader, party in self.parties.items():
                for name in party:
                    if name == ctx.author.name:
                        party_string = '----------PARTY----------\n{} (Leader)\n'.format(leader)

                        for name2 in party:
                            party_string += '{}\n'.format(name2)

                        party_string += '-------------------------'
                        await ctx.author.send(party_string)
                        return

        await ctx.author.send(utilities.yellow('You are not currently in a party.'))

    @commands.command()
    @commands.check(check_correct_channel)
    @commands.check(check_not_delving)
    async def leave(self, ctx):
        """Leave your current party from the encampment. If you are the leader or the last member of the party, this will disband the party."""
        if ctx.author.name in self.parties.keys():
            party = self.parties.pop(ctx.author.name)
            await ctx.author.send('You have disbanded the party.')

            for name in party:
                ex = ctx.guild.get_member_named(name)

                if ex is not None:
                    await ex.send('{} has disbanded the party.'.format(ctx.author.name))
        else:
            leader_to_modify = None

            for leader, party in self.parties.items():
                for name in party:
                    if name == ctx.author.name:
                        leader_to_modify = leader
                        break

            if leader_to_modify is not None:
                party_to_modify = self.parties[leader_to_modify]

                if len(party_to_modify) < 2:
                    disband = self.parties.pop(leader_to_modify)
                    await ctx.guild.get_member_named(leader_to_modify).send(
                        'The last member {} left, so the party has disbanded.'.format(ctx.author.name))
                else:
                    self.parties[leader_to_modify].remove(ctx.author.name)
                    await ctx.guild.get_member_named(leader_to_modify).send(
                        '{} has left the party.'.format(ctx.author.name))

                    for name in self.parties[leader_to_modify]:
                        await ctx.guild.get_member_named(name).send('{} has left the party.'.format(ctx.author.name))

                await ctx.author.send('You have left the party.')

    @commands.command(aliases=['dungeons', 'zones'])
    @commands.check(check_correct_channel)
    @commands.check(check_not_delving)
    async def mines(self, ctx):
        """Displays the mines currently available for delving, as well as their starting level and a description. Use the index number to start a delve."""
        await ctx.channel.send(zone.get_zone_list())

    @commands.command()
    @commands.check(check_correct_channel)
    @commands.check(check_not_delving)
    async def delve(self, ctx, index: int):
        """Start a delve. The index is availaable through \\mines. If in a party, the leader must start the delve, and party members are given a period of time to decline before the delve starts."""
        if index < 0 or index > len(zone.zones) + 1:
            await ctx.author.send('Invalid mine index number.')
            return

        if ctx.author.name in self.parties.keys():
            players = []

            for player in self.parties[ctx.author.name]:
                players.append(ctx.guild.get_member_named(player))

            await self.bot.get_cog('DelveController').request_delve(ctx, ctx.author, players, zone.zones[index])
        elif self.is_player_in_a_party(ctx.author.name):
            await ctx.author.send('Only the party leader can initiate a delve.')
        else:
            await self.bot.get_cog('DelveController').request_delve(ctx, ctx.author, [], zone.zones[index])
