import discord
from discord.ext import commands
import asyncio
import re
import random

#local
import utilities
from zone import Zone
from delve import Delve
from character import Character
from challenge_encounter import Challenge
from trap_encounter import Trap
from fight_encounter import Fight
#

class DelveController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.delves = {}

    async def check_correct_delve_channel(ctx):
        try:
            delves = ctx.bot.get_cog('DelveController').delves

            if ctx.channel.name in delves.keys():
                if ctx.author in delves[ctx.channel.name].players:
                    return True
        except AttributeError: #DMChannel
            return False

        return False

    async def check_is_leader(ctx):
        try:
            delves = ctx.bot.get_cog('DelveController').delves

            if delves[ctx.channel.name].leader == ctx.author:
                return True

            await ctx.channel.send('You must be the party leader to do this.')
            return False
        except KeyError:
            return False

    async def check_idle(ctx):
        try:
            delves = ctx.bot.get_cog('DelveController').delves

            if delves[ctx.channel.name].status == 'idle':
                return True

            await ctx.channel.send('You are too occupied at the moment.')
            return False
        except KeyError:
            return False

    async def check_room_complete(ctx):
        delves = ctx.bot.get_cog('DelveController').delves

        if ctx.channel.name in delves.keys() and delves[ctx.channel.name].status == 'idle' and delves[ctx.channel.name].current_room.encounter == None:
            return True

        await ctx.channel.send('Your path is blocked.')
        return False

    async def request_delve(self, ctx, leader: discord.Member, players: [discord.Member], zone: Zone):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            leader: discord.PermissionOverwrite(read_messages=True)
        }

        for player in players:
            overwrites[player] = discord.PermissionOverwrite(read_messages=True)

        category = discord.utils.get(ctx.guild.categories, name='Delve RPG')
        channel = await ctx.guild.create_text_channel('{}-{}'.format(leader.name, zone.name), overwrites=overwrites, category=category)
        self.delves[channel.name] = Delve(ctx.bot, leader, players, zone, channel)

        for player in players:
            await player.send('Your delve has begun! Please join <#{}>'.format(channel.id))

        await channel.send('The party has entered {} at depth {}.'.format(zone.name, zone.level))
        current_room = self.delves[channel.name].current_room
        await asyncio.sleep(2)
        await channel.send(utilities.blue('{}\n\n{}'.format(current_room.name, current_room.description)))

        if isinstance(current_room.encounter, Trap):
            await self.encounter_trap(self.delves[channel.name])
        elif isinstance(current_room.encounter, Fight):
            await self.encounter_fight(self.delves[channel.name])

    @commands.command()
    @commands.check(check_correct_delve_channel)
    @commands.check(check_idle)
    async def look(self, ctx):
        """Display the current room description and contents again."""
        current_room = self.delves[ctx.channel.name].current_room
        await ctx.channel.send(utilities.blue('{} - d{}\n\n{}'.format(current_room.name, self.delves[ctx.channel.name].depth, current_room.description)))

    @commands.command()
    @commands.check(check_correct_delve_channel)
    @commands.check(check_is_leader)
    @commands.check(check_idle)
    async def exit(self, ctx):
        """The party leader can end the delve, without risking going further. This can only be performed when the party is idle."""
        delve = self.delves[ctx.channel.name]
        await delve.channel.send('{} has chosen to end the delve. The party will exit the mine in 5 seconds.'.format(ctx.author.name))
        self.delves.pop(delve.channel.name)
        await asyncio.sleep(5)
        await delve.channel.delete()

    @commands.command()
    @commands.check(check_correct_delve_channel)
    async def depth(self, ctx):
        """Check the current mine depth."""
        delve = self.delves[ctx.channel.name]
        await ctx.channel.send('Current depth is {}.'.format(delve.depth))

    @commands.command()
    @commands.check(check_correct_delve_channel)
    @commands.check(check_is_leader)
    @commands.check(check_idle)
    async def attempt(self, ctx, player: discord.Member):
        """The player chosen by the party leader will attempt to clear the challenge or disarm the trap in this room."""
        delve = self.delves[ctx.channel.name]
        character = ctx.bot.get_cog('CharacterController').get(player)

        if delve.current_room.encounter != None:
            delve.status = 'busy'
            await ctx.channel.send('{} makes the attempt...'.format(player.name))
            await asyncio.sleep(5)

            if isinstance(delve.current_room.encounter, Challenge):
                if delve.current_room.encounter.get_result(character, delve.depth):
                    await ctx.channel.send(delve.current_room.encounter.success.format(player.name))
                    await ctx.channel.send('{} has gained {} xp, and the rest of the party has gained half as much.'.format(player.name, xp))
                    xp = 10 * delve.depth

                    for char in delve.characters:
                        if char.name == player.name:
                            char.gain_xp(xp, delve.depth)
                        else:
                            char.gain_xp(int(xp / 2), delve.depth)
                else:
                    await ctx.channel.send(delve.current_room.encounter.failure.format(player.name))

                delve.status = 'idle'
                delve.current_room.encounter = None
        else:
            await ctx.channel.send('Nothing remains to attempt here.')

    @commands.command()
    @commands.check(check_correct_delve_channel)
    @commands.check(check_is_leader)
    @commands.check(check_room_complete)
    async def proceed(self, ctx):
        """Delve deeper into the mine. You must complete the current room before proceeding."""
        delve = self.delves[ctx.channel.name]
        delve.proceed()
        await asyncio.sleep(2)
        await delve.channel.send(utilities.blue('{} - d{}\n\n{}'.format(delve.current_room.name, delve.depth, delve.current_room.description)))

        if isinstance(delve.current_room.encounter, Trap):
            await self.encounter_trap(delve)
        elif isinstance(delve.current_room.encounter, Fight):
            await self.encounter_fight(delve)

    async def encounter_trap(self, delve):
        delve.status = 'busy'
        await delve.channel.send(utilities.yellow(delve.current_room.encounter.description))
        await asyncio.sleep(3)

        for player in delve.players:
            character = self.bot.get_cog('CharacterController').get(player)

            if delve.current_room.encounter.get_result(character, delve.depth):
                await delve.channel.send(delve.current_room.encounter.success.format(player.name))
            else:
                dmg, element = character.take_damage([[2 * delve.depth, delve.current_room.encounter.element]])
                await delve.channel.send(utilities.red(delve.current_room.encounter.failure.format(player.name, dmg)))

                if dmg > 0 and character.current_health <= 0:
                    await self.player_dead(delve, player)

        delve.status = 'idle'
        delve.current_room.encounter = None

    async def encounter_fight(self, delve):
        delve.status = 'fighting'
        await delve.channel.send(utilities.green(delve.current_room.encounter.description))
        await delve.channel.send('The enemies attack!')
        fight = delve.current_room.encounter

        turn_count = 1
        while delve.status == 'fighting':
            await asyncio.sleep(2)

            for el in fight.enemies:
                await delve.channel.send(utilities.underline('{} ({}/{})'.format(el.name, el.current_health, el.health)))

            for actor in fight.inits:
                await delve.channel.send(utilities.bold('{} goes next.'.format(actor.name)))

                if isinstance(actor, Character): # Player
                    def check(m):
                        if m.author.name == actor.name and m.channel == delve.channel:
                            mg = re.match('(attack|att)\s+([1-9])', m.content, re.I)

                            if mg is not None:
                                return True
                        return False
                    try:
                        msg = await self.bot.wait_for('message', check=check, timeout=30)
                        mg = re.match('(attack|att)\s+([1-9])', msg.content, re.I)
                        enemy = fight.enemies[int(mg[2]) - 1]

                        if actor.equipped['weapon'] is None:
                            await delve.channel.send('{} kicks {} ineffectually.'.format(actor.name, enemy.name))
                        else:
                            dmgs = enemy.take_damage(actor.attack())
                            await delve.channel.send('{} attacks {} with {} for {}.'.format(actor.name, enemy.name, actor.equipped['weapon'].name, utilities.dmgs_to_str(dmgs)))

                            if enemy.current_health <= 0: # Enemy defeated
                                fight.remove_enemy(enemy)
                                await delve.channel.send('{} has been defeated.'.format(enemy.name))

                                if len(fight.enemies) == 0: # All enemies defeated
                                    await delve.channel.send('All enemies have been defeated.')
                                    [await delve.channel.send('{} has gained {} xp.'.format(c.name, c.gain_xp(fight.xp, fight.level))) for c in fight.characters]
                                    delve.status = 'idle'

                    except asyncio.TimeoutError:
                        await delve.channel.send('{} did not take an action in time.'.format(actor.name))
                else: # Enemy
                    target = random.choice(delve.characters)
                    dmgs = target.take_damage(actor.attack())
                    await delve.channel.send('{} attacks {} for {}.'.format(actor.name, target.name, utilities.dmgs_to_str(dmgs)))

                    if target.current_health <= 0:
                        await self.player_dead(delve, target.player)
                        fight.remove_character(target)

                await asyncio.sleep(3)

            await delve.channel.send('End of turn {}.'.format(turn_count))
            turn_count += 1

        delve.current_room.encounter = None

    async def player_dead(self, delve, player: discord.Member):
        await delve.channel.send('{} has died'.format(player.name))

        if len(delve.players) == 1:
            await delve.channel.send(utilities.red('Thus ends the delve.'))
            self.delves.pop(delve.channel.name)
            await asyncio.sleep(3)
            await delve.channel.delete()
        else:
            await delve.remove_player(player)
