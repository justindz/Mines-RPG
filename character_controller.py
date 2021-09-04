import asyncio
import discord
from discord.ext import commands

import utilities
import weapon
from weapon import WeaponType
import armor
from item import delete_item, generate_random_item, generate_random_book, ItemType, Rarity


class CharacterController(commands.Cog):
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection

    def get(self, player: discord.Member):
        # if the player is delving, get that reference instead of reloading from the DB
        delves = self.bot.get_cog('DelveController').delves

        for channel_name in delves.keys():
            delve = delves[channel_name]

            if player in delve.players:
                for char in delve.characters:
                    if char.name == str(player):
                        return char

        # if the player is not delving, get the DB reference
        character = self.connection.Character.find_one({'name': str(player)})

        # otherwise, this is a new player and we want to create a new character
        if character is None:
            character = self.connection.Character()
            character.name = str(player)
            character.reset_stats()
            character.add_to_inventory(generate_random_item(self.connection, 1, item_type=ItemType.weapon,
                                                            rarity=Rarity.common), False)
            character.add_to_inventory(generate_random_item(self.connection, 1, item_type=ItemType.head,
                                                            rarity=Rarity.common), False)
            character.add_to_inventory(generate_random_item(self.connection, 1, item_type=ItemType.potion,
                                                            rarity=Rarity.common), False)
            character.save()
            print(f'Created new character for {str(player)}')  # TODO make a logging call

        return character

    #  CHECKS  #
    async def check_idle(ctx):
        delves = ctx.bot.get_cog('DelveController').delves

        for channel_name in delves.keys():
            delve = delves[channel_name]

            if ctx.author in delve.players and delve.status != 'idle':
                return False

        return True

    #  COMMANDS  #
    @commands.command(aliases=['statistics'])
    async def stats(self, ctx):
        """Displays your character's vital statistics, including base stats and any current modifiers due to equipment or active effects."""
        character = self.get(ctx.author)
        await ctx.author.send(f'''
--<-(@  --<-(@  --<-(@  --<-(@
| Name: {character.name}
| Level: {character.level}
| XP: {character.xp}
| Coins: {character.coins}
| Level Points: {character.points}
|----
| Strength: {character.strength} ({character.bonus_strength:+})
| Intelligence: {character.intelligence} ({character.bonus_intelligence:+})
| Dexterity: {character.dexterity} ({character.bonus_dexterity:+})
| Willpower: {character.willpower} ({character.bonus_willpower:+})
|----
| Health: {character.current_health}/{character.health} ({character.bonus_health:+})
| Health Regen: {character.health_regen} ({character.bonus_health_regen:+})
| Stamina: {character.current_stamina}/{character.stamina} ({character.bonus_stamina:+})
| Stamina Regen: {character.stamina_regen} ({character.bonus_stamina_regen:+})
| Mana: {character.current_mana}/{character.mana} ({character.bonus_mana:+})
| Mana Regen: {character.mana_regen} ({character.bonus_mana_regen:+})
|----
| Initiative: {character.init} ({character.bonus_init:+})
| Carry Weight: {character.current_carry}/{character.carry} ({character.bonus_carry:+})
|----
| Earth Res: {character.earth_res:.0%} ({character.bonus_earth_res:+.0%})
| Fire Res: {character.fire_res:.0%} ({character.bonus_fire_res:+.0%})
| Electricity Res: {character.electricity_res:.0%} ({character.bonus_electricity_res:+.0%})
| Water Res: {character.water_res:.0%} ({character.bonus_water_res:+.0%})
| Damage Over Time Res: {character.dot_res:.0%} ({character.bonus_dot_res:+.0%})
| Damage Over Time Reduction: {character.dot_reduction} ({character.bonus_dot_reduction:+})
| Damage Over Time Effectiveness: {character.dot_effect:.0%} ({character.bonus_dot_effect:+.0%})
| Damage Over Time Duration: {character.dot_duration} ({character.bonus_dot_duration:+})
|----
| Deaths: {character.deaths}
--<-(@  --<-(@  --<-(@  --<-(@''')

    @commands.command(aliases=['inventory'])
    async def inv(self, ctx):
        """Lists all your equipped and carried items. Use the show command to view an individual item once you have its position number in your inventory."""
        character = self.get(ctx.author)
        inv_string = '=================EQUIPPED================\n'
        inv_string += 'Weapon: {}\n'.format(
            character.equipped['weapon']['name'] if character.equipped['weapon'] is not None else 'None')
        inv_string += 'Head: {}\n'.format(
            character.equipped['head']['name'] if character.equipped['head'] is not None else 'None')
        inv_string += 'Chest: {}\n'.format(
            character.equipped['chest']['name'] if character.equipped['chest'] is not None else 'None')
        inv_string += 'Belt: {}\n'.format(
            character.equipped['belt']['name'] if character.equipped['belt'] is not None else 'None')
        inv_string += 'Boots: {}\n'.format(
            character.equipped['boots']['name'] if character.equipped['boots'] is not None else 'None')
        inv_string += 'Gloves: {}\n'.format(
            character.equipped['gloves']['name'] if character.equipped['gloves'] is not None else 'None')
        inv_string += 'Amulet: {}\n'.format(
            character.equipped['amulet']['name'] if character.equipped['amulet'] is not None else 'None')
        inv_string += 'Ring: {}\n'.format(
            character.equipped['ring']['name'] if character.equipped['ring'] is not None else 'None')
        inv_string += '================INVENTORY================\n'

        i = 0
        for it in character.inventory:
            inv_string += f'{i} - {it["name"]}{utilities.get_rarity_symbol(it["rarity"])} - {it["weight"]}wgt\n'
            i += 1

        inv_string += 'Carry: {}/{}\n'.format(character.current_carry, character.carry + character.bonus_carry)
        await ctx.author.send(inv_string)

    @commands.command(aliases=['item'])
    async def show(self, ctx, pos):
        """View the details of an item in your inventory by position number or equipped gear by slot name (obtained using the 'inv' command)."""
        character = self.get(ctx.author)

        if pos.isdigit() and int(pos) + 1 <= len(character.inventory):
            it = character.inventory[int(pos)]
        elif isinstance(pos, str) and pos in weapon.valid_slots:
            it = character.equipped[pos]
        else:
            await ctx.author.send(utilities.red('Invalid inventory position or gear slot.'))
            return

        if it is not None:
            item_string = '''
====================ITEM===================='''
            item_string += f'''
{it["name"]} - Level {it["level"]} {utilities.get_rarity_symbol(it['rarity'])}

"{it["description"]}"
'''
            if it['_itype'] == ItemType.weapon.value:
                item_string += f'''
Class: {WeaponType(it['_weapon_type']).name.capitalize()}
Damage: {weapon.get_damages_display_string(it)}
Crit Damage: +{it['crit_damage']}

Requirements
------------
{utilities.get_requirements_display_string(it)}

Bonuses
-------
{weapon.get_bonuses_display_string(it)}

Sockets
-------
{utilities.get_socket_display(it)}
'''
            elif it['_itype'] in [ItemType.head.value, ItemType.chest.value, ItemType.belt.value,
                                  ItemType.boots.value, ItemType.gloves.value, ItemType.amulet.value,
                                  ItemType.ring.value]:
                item_string += f'''
Class: {ItemType(it['_itype']).name.capitalize()}

Requirements
------------
{utilities.get_requirements_display_string(it)}

Bonuses
-------
{armor.get_bonuses_display_string(it)}

Sockets
-------
{utilities.get_socket_display(it)}
'''
            item_string += f'''
Weight: {it["weight"]}
Value: {it["value"]}'''
            await ctx.author.send(item_string)
        else:
            await ctx.author.send('No item equipped in that slot.')

    @commands.command(aliases=['skills', 'spells'])
    async def abilities(self, ctx):
        character = self.get(ctx.author)
        """List your prepared abilities, and all abilities known to your character."""
        out = f'''
==========Prepared=========='''
        for i in range(1, len(character.ability_slots) + 1):
            out += f'\n{i}: {"None" if character.ability_slots[str(i)] is None else utilities.get_ability_by_name(character.ability_slots[str(i)]).name}'

        i = 0
        out += '\n==========Known==========\n'

        for ab in character.abilities:
            out += f'{i} - {utilities.get_ability_by_name(ab).name}\n'
            i += 1

        await ctx.author.send(out)

    @commands.command(aliases=['skill', 'spell'])
    async def ability(self, ctx, index=0):
        """Show the details of a specific ability known to your character."""
        character = self.get(ctx.author)

        try:
            await ctx.author.send(utilities.ability_to_str(character.abilities[index], character.level))
        except IndexError:
            await ctx.author.send(utilities.red('Invalid ability index.'))

    @commands.command(aliases=['assign'])
    @commands.check(check_idle)
    async def prepare(self, ctx, index: int, slot: int):
        """Prepare a known ability, assigning it to an action slot (1-6) for use in fights."""
        character = self.get(ctx.author)

        if character.assign_ability_to_slot(index, slot):
            await ctx.author.send(f'Ability prepared in slot {slot}.')
        else:
            await ctx.author.send(utilities.red('Invalid ability index or slot.'))

    @commands.command(aliases=['read'])
    @commands.check(check_idle)
    async def learn(self, ctx, index: int):
        """Consume a manual or tome to learn a new ability."""
        character = self.get(ctx.author)
        book = character.inventory[index]

        try:
            if character.learn(book):
                await ctx.author.send(utilities.bold('You have learned a new ability!'))
                delete_item(self.connection, book)
            else:
                await ctx.author.send(utilities.yellow(
                    f'You are unable to learn anything by reading the {character.inventory[index]["name"]}.'))
        except IndexError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))
        except KeyError:
            await ctx.author.send(
                utilities.yellow(f'You find it difficult to read the {character.inventory[index]["name"]}.'))

    @commands.command(aliases=['eq'])
    @commands.check(check_idle)
    async def equip(self, ctx, pos: int):
        """Attempts to equip the item from your inventory at the specified position. Will first unequip anything already equipped in that same slot."""
        character = self.get(ctx.author)

        try:
            item = character.inventory[pos]
        except IndexError:
            await ctx.author.send(utilities.red('Invalid inventory position.'))
            return

        if item is not None:
            if character.equip(item):
                await ctx.author.send(f'{utilities.underline(item["name"])} equipped.')
            else:
                await ctx.author.send(f'You do not meet the requirements to equip {item["name"]}.')

    @commands.command(aliases=['uneq'])
    @commands.check(check_idle)
    async def unequip(self, ctx, slot):
        """Unequips the item from your gear in the specified slot."""
        if slot not in weapon.valid_slots:
            await ctx.author.send(utilities.red('Invalid gear slot.'))
        else:
            character = self.get(ctx.author)
            item = character.unequip(slot)

            if item is not None:
                await ctx.author.send(f'{utilities.underline(item["name"])} unequipped.')

    @commands.command()
    async def depths(self, ctx):
        """Displays your maximum depths achieved in each mine you have entered."""
        character = self.get(ctx.author)
        out = '==========DEPTHS=========='

        if len(character.depths) == 0:
            out += '\nNone'
        else:
            for zone_name in character.depths.keys():
                out += f'\n{zone_name}: {character.depths[zone_name]}'

        await ctx.author.send(out)

    @commands.command()
    @commands.check(check_idle)
    async def level(self, ctx):
        """Consumes a level point, allowing you to choose from a set of improvements to your character."""
        character = self.get(ctx.author)

        if character.points <= 0:
            await ctx.author.send(utilities.red('You do not have any available level points.'))
        else:
            await ctx.author.send(character.display_level_up_menu())

            def check_level_up_menu_selection(m):
                if str(m.author) == character.name and m.content in ['1', '2', '3', '4', '5', '6', '7']:
                    return True

            try:
                msg = await self.bot.wait_for('message', check=check_level_up_menu_selection, timeout=30)
                choice = int(msg.content)
            except asyncio.TimeoutError:
                await ctx.author.send(
                    utilities.yellow('Selection timed out. Please use \\level again when you are ready.'))
                return

            if choice == 1:
                character.strength += 3
                await ctx.author.send('Your base strength has been permanently increased by 3.')
            elif choice == 2:
                character.intelligence += 3
                await ctx.author.send('Your base intelligence has been permanently increased by 3.')
            elif choice == 3:
                character.dexterity += 3
                await ctx.author.send('Your base dexterity has been permanently increased by 3.')
            elif choice == 4:
                character.willpower += 3
                await ctx.author.send('Your base willpower has been permanently increased by 3.')
            elif choice == 5:
                character.health += 5
                await ctx.author.send('Your base health has been permanently increased by 5.')
            elif choice == 6:
                character.stamina += 5
                await ctx.author.send('Your base stamina has been permanently increased by 5.')
            elif choice == 7:
                character.mana += 5
                await ctx.author.send('Your base mana has been permanently increased by 5.')
            else:
                await ctx.channel.send(utilities.red(f'Invalid level up reward selection {msg}.'))
                return

            character.points -= 1
            character.level += 1
            character.save()
            items = []

            for _ in range(2):
                items.append(generate_random_item(self.connection, character.level, rarity=Rarity.common))
                items.append(generate_random_book(self.connection, character.level))

            character.restock(items)
            await ctx.channel.send(utilities.green(f'{character.name} has grown in power!'))
