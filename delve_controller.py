import discord
from discord.ext import commands
import asyncio
import random

import skill
import utilities
from zone import Zone
from delve import Delve
from character import Character
from fight_encounter import Fight


async def check_ability_requirements_and_use(ability, actor, delve, target, fight):
    for stat in ability.cost.keys():
        cost = ability.cost[stat]

        if cost > 0:
            if stat == 'h' and actor.health <= cost:
                await delve.channel.send(f'You need more health to use {ability.name}')
                return False
            elif stat == 's':
                await delve.channel.send(f'You need more stamina to use {ability.name}')
                return False
            elif stat == 'm':
                await delve.channel.send(f'You need more mana to use {ability.name}')
                return False
            else:
                raise Exception(f'Invalid stat {stat} cost checked in check_ability_requirements_and_use for ability {ability.name}')

    if type(ability) == skill.Skill and actor.equipped['weapon'] is None:
        await delve.channel.send('You cannot use this skill without an equipped weapon.')
        return False
    elif type(ability) == skill.Skill and actor.equipped['weapon'].weapon_type != ability.weapon_type:
        await delve.channel.send(f'This skill requires a {ability.weapon_type}.')
        return False
    else:
        await delve.channel.send(fight.use_ability(actor, ability, target))
        return True


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
        except AttributeError:  # DMChannel
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

        if ctx.channel.name in delves.keys() and delves[ctx.channel.name].status == 'idle' and delves[ctx.channel.name].current_room.encounter is None:
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

        # if isinstance(current_room.encounter, None):
        #     await self.encounter_loot(self.delves[channel.name])
        # elif isinstance(current_room.encounter, Fight):
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
    @commands.check(check_room_complete)
    async def proceed(self, ctx):
        """Delve deeper into the mine. You must complete the current room before proceeding."""
        delve = self.delves[ctx.channel.name]
        delve.proceed()
        await asyncio.sleep(2)
        await delve.channel.send(utilities.blue('{} - d{}\n\n{}'.format(delve.current_room.name, delve.depth, delve.current_room.description)))

        # if isinstance(delve.current_room.encounter, Loot):
        #     await self.encounter_loot(self.delves[ctx.channel.name])
        # elif isinstance(delve.current_room.encounter, Fight):
        await self.encounter_fight(self.delves[ctx.channel.name])

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

                if isinstance(actor, Character):  # Player
                    def check_action_menu(m):
                        if m.author.name == actor.name and m.channel == delve.channel:
                            if m.content in ['1', '2', '3']:
                                return True
                        return False
                    try:
                        await delve.channel.send(Fight.display_action_menu())
                        msg = await self.bot.wait_for('message', check=check_action_menu, timeout=30)
                        action = msg.content

                        if action == '1':  # Ability
                            await delve.channel.send(Fight.display_ability_menu(actor))

                            def check_ability_menu(m):
                                if m.author.name == actor.name and m.channel == delve.channel:
                                    if 0 < int(m.content) <= 6 and actor.ability_slots[int(m.content)] is not None:
                                        return True
                                return False

                            msg = await self.bot.wait_for('message', check=check_ability_menu, timeout=30)
                            ability_choice = msg.content
                            ability = utilities.get_ability_by_name(actor.ability_slots[int(ability_choice)])

                            if ability.targets_enemies:
                                await delve.channel.send(fight.display_enemy_menu())

                                def check_enemy_menu(m):
                                    if m.author.name == actor.name and m.channel == delve.channel:
                                        if 0 < int(m.content) <= len(fight.enemies):
                                            return True
                                    return False

                                msg = await self.bot.wait_for('message', check=check_enemy_menu, timeout=30)
                                enemy_choice = int(msg.content)
                                enemy = fight.enemies[enemy_choice - 1]
                                await check_ability_requirements_and_use(ability, actor, delve, enemy, fight)
                            else:
                                await delve.channel.send(fight.display_ally_menu(actor))

                                def check_ally_menu(m):
                                    if m.author.name == actor.name and m.channel == delve.channel:
                                        if 0 < int(m.content) <= len(fight.characters):
                                            return True
                                    return False

                                msg = await self.bot.wait_for('message', check=check_ally_menu, timeout=30)
                                ally_choice = int(msg.content)
                                ally = fight.characters[ally_choice - 1]
                                await check_ability_requirements_and_use(ability, actor, delve, ally, fight)

                            if len(fight.enemies) == 0:
                                await delve.channel.send('All enemies have been defeated.')
                                [await delve.channel.send(
                                    '{} has gained {} xp.'.format(c.name, c.gain_xp(fight.xp, fight.level))) for c in
                                 fight.characters]
                                delve.status = 'idle'
                        elif action == '2':  # Item
                            menu, indices = Fight.display_item_menu(actor)
                            await delve.channel.send(menu)

                            def check_item_menu(m):
                                if m.author.name == actor.name and m.channel == delve.channel and 0 < int(m.content) <= len(indices):
                                    return True
                                return False

                            msg = await self.bot.wait_for('message', check=check_item_menu, timeout=30)
                            choice = msg.content
                            await delve.channel.send(actor.use_consumable(actor.inventory[indices[int(choice) - 1]]))
                        elif action == '3':  # Recover
                            h, s, m = actor.recover()
                            await delve.channel.send(f'{actor.name} recovered {h}h, {s}s, {m}m.')
                    except asyncio.TimeoutError:
                        await delve.channel.send('{} did not take an action in time.'.format(actor.name))
                else:  # Enemy
                    # TODO GOAP me
                    target = random.choice(delve.characters)
                    dmgs = target.take_damage(actor.attack())
                    await delve.channel.send('{} attacks {} for {}.'.format(actor.name, target.name, utilities.dmgs_to_str(dmgs)))

                    if target.current_health <= 0:
                        await self.player_dead(delve, target.player)
                        fight.remove_character(target)

                await asyncio.sleep(3)

            turn_count += 1
            await delve.channel.send('End of turn {}.'.format(turn_count))

            for character in delve.characters:
                h, s, m = character.regen()

                if h > 0 or s > 0 or m > 0:
                    await delve.channel.send(f'{character.name} regenerates {h}h {s}s {m}m.')

        delve.current_room.encounter = None

    async def encounter_loot(self, delve):
        await delve.channel.send(utilities.green(delve.current_room.encounter.description))
        await delve.channel.send('Loot encounters are not implemented yet. This would have been sweet, sweet loot.')

    async def player_dead(self, delve, player: discord.Member):
        await delve.channel.send('{} has died'.format(player.name))

        if len(delve.players) == 1:
            await delve.channel.send(utilities.red('Thus ends the delve.'))
            self.delves.pop(delve.channel.name)
            await asyncio.sleep(3)
            await delve.channel.delete()
        else:
            await delve.remove_player(player)
