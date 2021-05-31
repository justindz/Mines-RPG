import discord
from discord.ext import commands

import utilities
import weapon
from character import Character
from weapon import Weapon
from armor import Armor


class CharacterController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.characters = []

    def get(self, player: discord.Member):
        # see if they already exist
        for character in self.characters:
            if character.name == player.name:
                return character

        # didn't find them, so create
        character = Character(player)
        self.characters.append(character)
        return character

    #  CHECKS  #
    async def check_idle_or_not_delving(ctx):
        delves = ctx.bot.get_cog('DelveController').delves

        for delve in delves:
            if ctx.author in delve.players and delve.status != 'idle':
                return False

        return True

    #  COMMANDS  #
    @commands.command(aliases=['statistics'])
    async def stats(self, ctx):
        """Displays your character's vital statistics, including base stats and any current modifiers due to equipment or active effects."""
        character = self.get(ctx.author)
        await ctx.author.send('''
--<-(@  --<-(@  --<-(@  --<-(@
| Name: {}
| Level: {}
| XP: {}
| Coins: {}
| Skill Points: {}
|----
| Strength: {:-} ({:+})
| Intelligence: {:-} ({:+})
| Dexterity: {:-} ({:+})
| Willpwer: {:-} ({:+})
|----
| Health: {}/{} ({:+})
| Stamina: {}/{} ({:+})
| Mana: {}/{} ({:+})
|----
| Initiative: {:-} ({:+})
| Carry Weight: {}/{} ({:+})
|----
| Earth Res: {}
| Fire Res: {}
| Electricity Res: {}
| Water Res: {}
--<-(@  --<-(@  --<-(@  --<-(@
        '''.format(character.name, character.level, character.xp, character.coins, character.points,
                   character.strength, character.bonus_strength, character.intelligence, character.bonus_intelligence,
                   character.dexterity, character.bonus_dexterity, character.willpower, character.bonus_willpower,
                   character.current_health, character.health, character.bonus_health, character.current_stamina,
                   character.stamina, character.bonus_stamina, character.current_mana, character.mana,
                   character.bonus_mana,
                   character.init, character.bonus_init, character.current_carry, character.carry,
                   character.bonus_carry,
                   character.earth_res, character.fire_res, character.electricity_res, character.water_res))

    @commands.command(aliases=['inventory'])
    async def inv(self, ctx):
        """Lists all your equipped and carried items. Use the show command to view an individual item once you have its position number in your inventory."""
        character = self.get(ctx.author)
        inv_string = '=================EQUIPPED================\n'
        inv_string += 'Weapon: {}\n'.format(
            character.equipped['weapon'].name if character.equipped['weapon'] is not None else 'None')
        inv_string += 'Head: {}\n'.format(
            character.equipped['head'].name if character.equipped['head'] is not None else 'None')
        inv_string += 'Chest: {}\n'.format(
            character.equipped['chest'].name if character.equipped['chest'] is not None else 'None')
        inv_string += 'Belt: {}\n'.format(
            character.equipped['belt'].name if character.equipped['belt'] is not None else 'None')
        inv_string += 'Boots: {}\n'.format(
            character.equipped['boots'].name if character.equipped['boots'] is not None else 'None')
        inv_string += 'Gloves: {}\n'.format(
            character.equipped['gloves'].name if character.equipped['gloves'] is not None else 'None')
        inv_string += 'Amulet: {}\n'.format(
            character.equipped['amulet'].name if character.equipped['amulet'] is not None else 'None')
        inv_string += 'Ring: {}\n'.format(
            character.equipped['ring'].name if character.equipped['ring'] is not None else 'None')
        inv_string += '================INVENTORY================\n'

        i = 0
        for item in character.inventory:
            inv_string += '{} - {} ({}) {}wgt\n'.format(i, item.name, item.level, item.weight)
            i += 1

        inv_string += 'Carry: {}/{}\n'.format(character.current_carry, character.carry + character.bonus_carry)
        inv_string += '========================================='
        await ctx.author.send(inv_string)

    @commands.command(aliases=['item'])
    async def show(self, ctx, pos):
        """View the details of an item in your inventory by position number or equipped gear by slot name (obtained using the 'inv' command)."""
        character = self.get(ctx.author)

        if isinstance(pos, int) and pos + 1 <= len(character.inventory):
            item = character.inventory[pos]
        elif isinstance(pos, str) and pos in weapon.valid_slots:
            item = character.equipped[pos]
        else:
            await ctx.author.send(utilities.red('Invalid inventory position or gear slot.'))
            return

        if item is not None:
            item_string = '''
====================ITEM===================='''
            item_string += '''
{} - Level {}

"{}"
'''.format(item.name, item.level, item.description)
            if isinstance(item, Weapon):
                item_string += '''
Class: {}
Damage: {}

Bonuses
-------
{}
'''.format(item.weapon_type, item.get_damages_display_string(), item.get_bonuses_display_string())
            elif isinstance(item, Armor):
                item_string += '''
Class: {}

Bonuses
-------
{}
'''.format(item.type, item.get_bonuses_display_string())
            item_string += '''
Weight: {}
============================================'''.format(item.weight)
            await ctx.author.send(item_string)
        else:
            await ctx.author.send('No item equipped in that slot.')

    @commands.command(aliases=['eq'])
    @commands.check(check_idle_or_not_delving)
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
                await ctx.author.send('{} equipped.'.format(utilities.underline(item.name)))
            else:
                await ctx.author.send('You do not meet the requirements to equip {}.'.format(item.name))

    @commands.command(aliases=['uneq'])
    @commands.check(check_idle_or_not_delving)
    async def unequip(self, ctx, slot):
        """Unequips the item from your gear in the specified slot."""
        if slot not in weapon.valid_slots:
            await ctx.author.send(utilities.red('Invalid gear slot.'))
        else:
            character = self.get(ctx.author)
            item = character.unequip(slot)

            if item is not None:
                await ctx.author.send('{} unequipped.'.format(utilities.underline(item.name)))
