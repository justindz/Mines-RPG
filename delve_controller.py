import discord
from discord.errors import NotFound
from discord.ext import commands
import asyncio
import random

import skill
import spell
import utilities
from elements import Elements
from zone import Zone
from delve import Delve
from character import Character
from enemy import Enemy
from summon import Summon
from fight_encounter import Fight
from loot_encounter import Loot
from item import delete_item


async def check_ability_requirements_and_use(ability, actor, delve, target, fight):
    for stat in ability.cost.keys():
        cost = ability.cost[stat]

        if cost > 0:
            if stat == 'h' and actor.current_health < cost:
                await delve.channel.send(f'You need more health to use {ability.name}.')
                await DelveController.recover(actor, delve)
                return False
            elif stat == 's' and actor.current_stamina < cost:
                await delve.channel.send(f'You need more stamina to use {ability.name}.')
                await DelveController.recover(actor, delve)
                return False
            elif stat == 'm' and actor.current_mana < cost:
                await delve.channel.send(f'You need more mana to use {ability.name}.')
                await DelveController.recover(actor, delve)
                return False
            elif stat not in ['h', 's', 'm']:
                raise Exception(f'Invalid stat {stat} cost checked in check_ability_requirements_and_use for ability {ability.name}')

    if isinstance(ability, skill.Skill) and actor.equipped['weapon'] is None:
        await delve.channel.send('You cannot use this skill without an equipped weapon.')
        await DelveController.recover(actor, delve)
        return False
    elif isinstance(ability, skill.Skill) and actor.equipped['weapon']['_weapon_type'] in ability.weapon_types:
        await delve.channel.send(f'You cannot use this skill with this weapon type.')
        await DelveController.recover(actor, delve)
        return False
    elif not set(ability.consumes).issubset(set(fight.states)):
        await delve.channel.send(f'{ability.name} requires infused elements.')
        await DelveController.recover(actor, delve)
        return False
    else:
        await delve.channel.send(fight.use_ability(actor, ability, target))
        return True


class DelveController(commands.Cog):
    def __init__(self, bot, connection):
        self.bot = bot
        self.delves = {}
        self.connection = connection
        self.get = self.bot.get_cog('CharacterController').get

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

    async def request_delve(self, ctx, leader: discord.Member, players: [discord.Member], zone: Zone, restart: bool):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            leader: discord.PermissionOverwrite(read_messages=True)
        }

        for player in players:
            overwrites[player] = discord.PermissionOverwrite(read_messages=True)

        category = discord.utils.get(ctx.guild.categories, name='Delve RPG')
        channel = await ctx.guild.create_text_channel('{}-{}'.format(leader.name, zone.name), overwrites=overwrites, category=category)
        self.delves[channel.name] = Delve(ctx.bot, self.connection, leader, players, zone, channel, restart)

        for player in players:
            await player.send('Your delve has begun! Please join <#{}>'.format(channel.id))

        if restart:
            await channel.send('The party has re-entered {} at depth {}.'.format(zone.name, zone.level))
        else:
            await channel.send('The party has entered {} at depth {}.'.format(zone.name, zone.level))

        current_room = self.delves[channel.name].current_room
        await asyncio.sleep(2)
        await channel.send(utilities.blue('{}\n\n{}'.format(current_room.name, current_room.description)))

        if isinstance(current_room.encounter, Loot):
            await self.encounter_loot(self.delves[channel.name])
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

        for character in delve.characters:
            character.reset_stats()

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
    async def status(self, ctx):
        """View the status effects currently affecting you."""
        character = self.get(ctx.author)
        out = f'{character.name} is affected by:'

        if len(character.status_effects) > 0:
            for se in character.status_effects:
                out += f'\n- {se["name"]}: {se["value"]:+} {se["stat"]} ({se["turns_remaining"]} turns)'

        out += f'\n\nShock: {character.shock}/{character.shock_limit}\nConfusion: {character.confusion}/{character.confusion_limit}'
        await ctx.channel.send(out)

    @commands.command()
    @commands.check(check_correct_delve_channel)
    @commands.check(check_idle)
    async def use(self, ctx, index: int):
        character = self.get(ctx.author)

        try:
            consumable = character.inventory[index]
        except IndexError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))
            return

        await ctx.channel.send(character.use_consumable(self.connection, consumable))

    @commands.command()
    @commands.check(check_correct_delve_channel)
    @commands.check(check_is_leader)
    @commands.check(check_room_complete)
    async def proceed(self, ctx):
        """Delve deeper into the mine. You must complete the current room before proceeding."""
        delve = self.delves[ctx.channel.name]

        if delve.zone.name == 'Boon Mine' and delve.depth >= 10:
            await delve.channel.send('You have reached the end of Boon Mine.')
            return

        delve.proceed()

        for char in delve.characters:
            if char.update_depth_progress(delve.zone, delve.depth):
                await delve.channel.send(utilities.green(f'{char.name} has reached a new depth and gained a level up!'))

        await asyncio.sleep(2)
        await delve.channel.send(utilities.blue('{}\n\n{}'.format(delve.current_room.name, delve.current_room.description)))

        if isinstance(delve.current_room.encounter, Loot):
            await self.encounter_loot(self.delves[ctx.channel.name])
        elif isinstance(delve.current_room.encounter, Fight):
            await self.encounter_fight(self.delves[ctx.channel.name])

    async def encounter_fight(self, delve):
        await delve.channel.send(utilities.green(delve.current_room.encounter.description))
        await asyncio.sleep(5)
        delve.status = 'fighting'
        await delve.channel.send('The enemies attack!')
        fight = delve.current_room.encounter
        turn_count = 0

        while delve.status == 'fighting':
            await self.start_of_turn(delve, fight)

            for actor in fight.inits:
                try:
                    await delve.channel.send(utilities.bold(f'{actor.name} goes next.'))
                except NotFound:
                    return  # The channel has been deleted because the delve ended

                if actor.shock >= actor.shock_limit + (actor.bonus_shock_limit if isinstance(actor, Character) else 0):
                    await delve.channel.send(f'{actor.name} is shocked and cannot act.')
                    actor.shock = 0
                    if isinstance(actor, Character):
                        actor.save()
                    await asyncio.sleep(1)
                    continue
                elif actor.confusion >= actor.confusion_limit + (actor.bonus_confusion_limit if isinstance(actor, Character) else 0):
                    await delve.channel.send(f'{actor.name} is confused.')

                if isinstance(actor, Character):  # Player
                    if actor.confusion >= actor.confusion_limit + actor.bonus_confusion_limit:
                        actions = ['ability', 'item', 'recover']

                        if not actor.has_consumables():
                            actions.remove('item')

                        chosen = random.choice(actions)

                        if chosen == 'ability':
                            ability = random.choice([utilities.get_ability_by_name(x) for x in actor.ability_slots])
                            target = random.choice(fight.enemies)
                            await delve.channel.send(f'{actor.name} tries to use {ability.name} on {target.name}')
                            await check_ability_requirements_and_use(ability, actor, delve, target, fight)
                        elif chosen == 'item':
                            await delve.channel.send(actor.use_consumable(self.connection, random.choice([x for x in actor.inventory if x['_itype'] in [9, 10]])))
                        else:
                            await self.recover(actor, delve)

                        actor.confusion = 0
                        actor.save()
                        await asyncio.sleep(1)
                        continue

                    def check_action_menu(m):
                        if str(m.author) == actor.name and m.channel == delve.channel:
                            if m.content in ['1', '2', '3']:
                                if m.content == '2' and not actor.has_consumables():
                                    return False
                                return True
                        return False
                    try:
                        await delve.channel.send(Fight.display_action_menu(actor))
                        msg = await self.bot.wait_for('message', check=check_action_menu, timeout=30)
                        action = msg.content

                        if action == '1':  # Ability
                            await delve.channel.send(Fight.display_ability_menu(actor))

                            def check_ability_menu(m):
                                if str(m.author) == actor.name and m.channel == delve.channel:
                                    if 0 < int(m.content) <= len(actor.ability_slots) and actor.ability_slots[m.content] is not None:
                                        return True
                                return False

                            msg = await self.bot.wait_for('message', check=check_ability_menu, timeout=30)
                            ability = utilities.get_ability_by_name(actor.ability_slots[msg.content])

                            if isinstance(ability, skill.Skill) or (isinstance(ability, spell.Spell) and ability.targets_enemies):
                                def check_enemy_menu(m):
                                    if str(m.author) == actor.name and m.channel == delve.channel:
                                        if 0 < int(m.content) <= len(fight.enemies):
                                            return True
                                    return False

                                await self.display_enemy_list(delve, fight)
                                msg = await self.bot.wait_for('message', check=check_enemy_menu, timeout=30)
                                enemy_choice = int(msg.content)
                                enemy = fight.enemies[enemy_choice - 1]
                                await check_ability_requirements_and_use(ability, actor, delve, enemy, fight)
                            elif isinstance(ability, spell.Spell) and not ability.targets_enemies:
                                await delve.channel.send(fight.display_ally_menu(actor))

                                def check_ally_menu(m):
                                    if str(m.author) == actor.name and m.channel == delve.channel:
                                        if 0 < int(m.content) <= len(fight.characters):
                                            return True
                                    return False

                                msg = await self.bot.wait_for('message', check=check_ally_menu, timeout=30)
                                ally_choice = int(msg.content)
                                ally = fight.characters[ally_choice - 1]
                                await check_ability_requirements_and_use(ability, actor, delve, ally, fight)
                        elif action == '2':  # Item
                            menu, indices = Fight.display_item_menu(actor)
                            await delve.channel.send(menu)

                            def check_item_menu(m):
                                if str(m.author) == actor.name and m.channel == delve.channel and 0 < int(m.content) <= len(indices):
                                    return True
                                return False

                            msg = await self.bot.wait_for('message', check=check_item_menu, timeout=30)
                            choice = msg.content
                            await delve.channel.send(actor.use_consumable(self.connection, actor.inventory[indices[int(choice) - 1]]))
                        elif action == '3':  # Recover
                            await self.recover(actor, delve)

                        await self.check_for_defeated_enemies(actor, delve, fight)
                        dot = actor.apply_damage_over_time()

                        if dot is not None:
                            await delve.channel.send(dot[1])

                            if dot[0] is True:
                                await self.player_dead(delve, actor)
                    except asyncio.TimeoutError:
                        await delve.channel.send('{} did not take an action in time.'.format(actor.name))
                        await self.recover(actor, delve)
                elif isinstance(actor, Summon):
                    out = actor.take_a_turn(fight)
                    await delve.channel.send(out)
                    await self.check_for_defeated_enemies(actor, delve, fight)
                    dot = actor.apply_damage_over_time()

                    if dot is not None:
                        await delve.channel.send(dot[1])

                        if dot[0] is True:
                            fight.unsummon(actor)
                elif isinstance(actor, Enemy):
                    out = actor.take_a_turn(fight)
                    await delve.channel.send(out)

                    for target in fight.characters:
                        if target.current_health <= 0:
                            if isinstance(target, Character):
                                if fight.remove_character(target):
                                    await delve.channel.send(f'{target.name}\'s summons vanished.')

                                await self.player_dead(delve, target)
                            elif isinstance(target, Summon):
                                await delve.channel.send(fight.unsummon(target))

                    dot = actor.apply_damage_over_time()

                    if dot is not None:
                        await delve.channel.send(dot[1])

                        if dot[0] is True:
                            fight.remove_enemy(actor)
                            await delve.channel.send(f'{actor.name} was defeated.')
                if await self.check_end_of_fight(delve, fight):
                    break
                await asyncio.sleep(3)

            turn_count += 1
            await self.end_of_turn(delve, fight, turn_count)
        delve.current_room.encounter = None

    @staticmethod
    async def check_for_defeated_enemies(actor, delve, fight):
        for enemy in fight.enemies:
            if enemy.current_health <= 0:
                fight.remove_enemy(enemy)
                await delve.channel.send(f'{actor.name} defeated {enemy.name}.')

    async def start_of_turn(self, delve, fight):
        for actor in [x for x in fight.characters if isinstance(x, Character)]:
            await asyncio.sleep(1)
            await self.pay_summon_upkeep(actor, delve, fight)

        fight.update_turn_order()
        await asyncio.sleep(2)
        await delve.channel.send(utilities.underline('Turn order:'))

        for fighter in fight.inits:
            await self.display_fighter_summary(delve, fighter)

        await delve.channel.send(fight.display_active_elements())

    @staticmethod
    async def display_fighter_summary(delve, fighter, index=None):
        await delve.channel.send(utilities.underline(
            (f'{index} - ' if index is not None else '- ')
            + f'{fighter.name} {fighter.current_health}/{fighter.health}'
            + (f' [{fighter.list_active_effects()}]' if len(fighter.status_effects) > 0 else '')
            + (f' {utilities.get_elemental_symbol(Elements.fire)}' if fighter.burn['turns'] > 0 else '')
            + (f' :drop_of_blood:' if fighter.bleed['turns'] > 0 else '')
            + (
                f' {utilities.get_elemental_symbol(Elements.electricity)} {fighter.shock}/{fighter.shock_limit + fighter.bonus_shock_limit}' if fighter.shock > 0 else '')
            + (f' :grey_question: {fighter.confusion}/{fighter.confusion_limit + fighter.bonus_confusion_limit}' if
               fighter.confusion > 0 else '')
        ))

    @staticmethod
    async def display_enemy_list(delve, fight):
        i = 1

        for enemy in fight.enemies:
            await DelveController.display_fighter_summary(delve, enemy, i)
            i += 1

    @staticmethod
    async def pay_summon_upkeep(actor, delve, fight):
        for summon in [x for x in fight.characters if isinstance(x, Summon) and x.owner == actor.name]:
            if actor.current_health <= summon.cost['h']:
                await delve.channel.send(f'{actor.name} has insufficient health to sustain {summon.name}.')
                fight.unsummon(summon, actor)
                break
            if actor.current_stamina < summon.cost['s']:
                await delve.channel.send(f'{actor.name} has insufficient stamina to sustain {summon.name}.')
                fight.unsummon(summon, actor)
                break
            if actor.current_mana < summon.cost['m']:
                await delve.channel.send(f'{actor.name} has insufficient mana to sustain {summon.name}.')
                fight.unsummon(summon, actor)
                break

            out = f'{summon.name} drained '

            if summon.cost['h'] > 0:
                actor.current_health -= summon.cost['h']
                out += f'{summon.cost["h"]}h, '
            if summon.cost['s'] > 0:
                actor.current_stamina -= summon.cost['s']
                out += f'{summon.cost["s"]}s, '
            if summon.cost['m'] > 0:
                actor.current_mana -= summon.cost['m']
                out += f'{summon.cost["m"]}m, '

            out = out.rstrip(", ") + f' from {actor.name}.'
            await delve.channel.send(out)
            actor.save()

    @staticmethod
    async def end_of_turn(delve, fight, turn_count):
        for actor in fight.inits:
            out = actor.end_of_turn()

            if out != '':
                await delve.channel.send(out)

        if fight.end_of_turn():
            await delve.channel.send('Elements have dissipated.')

        await delve.channel.send('End of turn {}.'.format(turn_count))

    @staticmethod
    async def check_end_of_fight(delve, fight) -> bool:
        if len(fight.enemies) == 0:
            await delve.channel.send('The enemies have been defeated.')

            for character in [x for x in delve.characters if isinstance(x, Character)]:
                character.remove_all_status_effects()
                character.shock = 0
                character.confusion = 0

            fight.unsummon_all()
            delve.status = 'idle'
            return True
        return False

    @staticmethod
    async def recover(actor, delve):
        h, s, m = actor.recover()
        await delve.channel.send(f'{actor.name} recovered {h}h, {s}s, {m}m.')

    async def encounter_loot(self, delve):
        loot = delve.current_room.encounter
        await delve.channel.send(utilities.green(loot.description))
        await delve.channel.send(f'The party also found: {loot.roll_item["name"]} {utilities.get_rarity_symbol(loot.roll_item["rarity"])}')
        await asyncio.sleep(1)
        await delve.channel.send(f'Each player may +roll in the next 15 seconds to attempt to acquire.')

        def check_roll(m):
            if m.channel == delve.channel:
                if m.content.startswith('+roll'):
                    loot.add_to_roll_list(str(m.author))
            return False
        try:
            await self.bot.wait_for('message', check=check_roll, timeout=15)
        except asyncio.TimeoutError:
            winner = loot.choose_winner()

            if winner is not None:
                for character in delve.characters:
                    if character['name'] == winner:
                        character.add_to_inventory(loot.roll_item, True)
                        await delve.channel.send(utilities.green(f'{character["name"]} acquired the {loot.roll_item["name"]}!'))
                        break
            else:
                await delve.channel.send(utilities.green(f'The party leaves the item behind.'))

        delve.current_room.encounter = None

    async def player_dead(self, delve, character):
        for slot in character.equipped.keys():
            character.unequip(slot)

        for item in character.inventory:
            delete_item(self.connection, item)

        character.inventory = []
        character.current_carry = 0
        character.deaths += 1
        character.reset_stats()
        character.save()
        await delve.channel.send(utilities.red('{} has died.'.format(character.name)))

        if len(delve.players) == 1:
            await delve.channel.send(utilities.red('Thus ends the delve.'))
            self.delves.pop(delve.channel.name)
            await asyncio.sleep(3)
            await delve.channel.delete()
        else:
            for player in delve.players:
                if str(player) == character.name:
                    await delve.remove_player(character)
