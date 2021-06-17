import discord
import random
import datetime
from mongokit_ng import Document

import ability
from weapon import Weapon
from armor import Armor
from consumable import Consumable
from elements import Elements
import utilities
import skill
import spell


class Character(Document):
    __database__ = 'delverpg'
    __collection__ = 'characters'
    structure = {
        'name': str,
        'level': int,
        'xp': int,
        'coins': int,
        'created': datetime.datetime,

        'strength': int,
        'bonus_strength': int,
        'intelligence': int,
        'bonus_intelligence': int,
        'dexterity': int,
        'bonus_dexterity': int,
        'willpower': int,
        'bonus_willpower': int,

        'health': int,
        'bonus_health': int,
        'current_health': int,
        'stamina': int,
        'bonus_stamina': int,
        'current_stamina': int,
        'mana': int,
        'bonus_mana': int,
        'current_mana': int,

        'init': int,
        'bonus_init': int,
        'carry': int,
        'bonus_carry': int,
        'current_carry': int,

        'earth_res': float,
        'fire_res': float,
        'electricity_res': float,
        'water_res': float,

        'points': int,
        'abilities': [str],
        'ability_slots': dict,
        'equipped': dict,
        'inventory': None,
    }
    required_fields = ['name']
    default_values = {
        'level': 1,
        'xp': 0,
        'coins': 0,
        'created': datetime.datetime.utcnow,

        'strength': 0,
        'bonus_strength': 0,
        'intelligence': 0,
        'bonus_intelligence': 0,
        'dexterity': 0,
        'bonus_dexterity': 0,
        'willpower': 0,
        'bonus_willpower': 0,

        'health': 100,
        'bonus_health': 0,
        'current_health': 100,
        'stamina': 100,
        'bonus_stamina': 0,
        'current_stamina': 100,
        'mana': 100,
        'bonus_mana': 0,
        'current_mana': 100,

        'init': 0,
        'bonus_init': 0,
        'carry': 500,
        'current_carry': 0,
        'bonus_carry': 0,

        'earth_res': 0.0,
        'fire_res': 0.0,
        'electricity_res': 0.0,
        'water_res': 0.0,

        'points': 0,
        'abilities': ['spell-stalagmite', 'skill-slash', 'spell-mend_wounds'],
        'ability_slots': {'1': 'spell-stalagmite', '2': 'skill-slash', '3': 'spell-mend_wounds', '4': None, '5': None, '6': None},
        'equipped': {'weapon': None, 'head': None, 'chest': None, 'belt': None, 'boots': None, 'gloves': None,
                     'amulet': None, 'ring': None},
        'inventory': [],
    }
    use_dot_notation = True
    use_autorefs = True

    def update_current_hsm(self):
        self.current_health = self.health + self.bonus_health
        self.current_stamina = self.stamina + self.bonus_stamina
        self.current_mana = self.mana + self.bonus_mana

    def add_to_inventory(self, item, ignore_carry, unequipping=False):
        if ignore_carry or self.current_carry + item.weight <= self.carry + self.bonus_carry:
            self.inventory.append(item)

            if not unequipping:
                self.current_carry += item.weight

            self.save()
            return True
        return False

    def remove_from_inventory(self, item, equipping=False):
        self.inventory.remove(item)

        if not equipping:
            self.current_carry -= item.weight

        self.save()

    def equip(self, item):
        if type(item) not in [Weapon, Armor]:
            return False

        if self.equipped[item.type.name] is not None:
            self.unequip(item.type.name)
            self.save()

        if self.level >= item.level:
            self.remove_from_inventory(item, True)
            self.equipped[item.type.name] = item
            self.update_stats(item, True)
            return True

        return False

    def unequip(self, slot):
        if slot not in ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring'] or self.equipped[
                slot] is None:
            return False
        else:
            item = self.equipped[slot]
            self.equipped[slot] = None
            self.update_stats(item, False)
            self.add_to_inventory(item, True, True)
            return item

    def update_stats(self, thing, equip):
        if isinstance(thing, Weapon):
            if equip:
                self.apply_weapon_bonuses(thing)
            else:
                self.remove_weapon_bonuses(thing)
        if isinstance(thing, Armor):
            if equip:
                self.apply_armor_bonuses(thing)
            else:
                self.remove_armor_bonuses(thing)

        self.update_current_hsm()
        self.save()

    def apply_weapon_bonuses(self, weapon):
        if weapon.bonus_strength != 0:
            self.bonus_strength += weapon.bonus_strength
        if weapon.bonus_intelligence != 0:
            self.bonus_intelligence += weapon.bonus_intelligence
        if weapon.bonus_dexterity != 0:
            self.bonus_dexterity += weapon.bonus_dexterity
        if weapon.bonus_willpower != 0:
            self.bonus_willpower += weapon.bonus_willpower
        if weapon.bonus_health != 0:
            self.bonus_health += weapon.bonus_health
        if weapon.bonus_stamina != 0:
            self.bonus_stamina += weapon.bonus_stamina
        if weapon.bonus_mana != 0:
            self.bonus_mana += weapon.bonus_mana
        if weapon.bonus_init != 0:
            self.bonus_init += weapon.bonus_init

    def remove_weapon_bonuses(self, weapon):
        if weapon.bonus_strength != 0:
            self.bonus_strength -= weapon.bonus_strength
        if weapon.bonus_intelligence != 0:
            self.bonus_intelligence -= weapon.bonus_intelligence
        if weapon.bonus_dexterity != 0:
            self.bonus_dexterity -= weapon.bonus_dexterity
        if weapon.bonus_willpower != 0:
            self.bonus_willpower -= weapon.bonus_willpower
        if weapon.bonus_health != 0:
            self.bonus_health -= weapon.bonus_health
        if weapon.bonus_stamina != 0:
            self.bonus_stamina -= weapon.bonus_stamina
        if weapon.bonus_mana != 0:
            self.bonus_mana -= weapon.bonus_mana
        if weapon.bonus_init != 0:
            self.bonus_init -= weapon.bonus_init

    def apply_armor_bonuses(self, armor):
        if armor.bonus_strength != 0:
            self.bonus_strength += armor.bonus_strength
        if armor.bonus_intelligence != 0:
            self.bonus_intelligence += armor.bonus_intelligence
        if armor.bonus_dexterity != 0:
            self.bonus_dexterity += armor.bonus_dexterity
        if armor.bonus_willpower != 0:
            self.bonus_willpower += armor.bonus_willpower
        if armor.bonus_health != 0:
            self.bonus_health += armor.bonus_health
        if armor.bonus_stamina != 0:
            self.bonus_stamina += armor.bonus_stamina
        if armor.bonus_mana != 0:
            self.bonus_mana += armor.bonus_mana
        if armor.bonus_init != 0:
            self.bonus_init += armor.bonus_init
        if armor.bonus_carry != 0:
            self.bonus_carry += armor.bonus_carry
        if armor.earth_res != 0:
            self.earth_res += armor.earth_res
        if armor.fire_res != 0:
            self.fire_res += armor.fire_res
        if armor.electricity_res != 0:
            self.electricity_res += armor.electricity_res
        if armor.water_res != 0:
            self.water_res += armor.water_res

    def remove_armor_bonuses(self, armor):
        if armor.bonus_strength != 0:
            self.bonus_strength -= armor.bonus_strength
        if armor.bonus_intelligence != 0:
            self.bonus_intelligence -= armor.bonus_intelligence
        if armor.bonus_dexterity != 0:
            self.bonus_dexterity -= armor.bonus_dexterity
        if armor.bonus_willpower != 0:
            self.bonus_willpower -= armor.bonus_willpower
        if armor.bonus_health != 0:
            self.bonus_health -= armor.bonus_health
        if armor.bonus_stamina != 0:
            self.bonus_stamina -= armor.bonus_stamina
        if armor.bonus_mana != 0:
            self.bonus_mana -= armor.bonus_mana
        if armor.bonus_init != 0:
            self.bonus_init -= armor.bonus_init
        if armor.bonus_carry != 0:
            self.bonus_carry -= armor.bonus_carry
        if armor.earth_res != 0:
            self.earth_res -= armor.earth_res
        if armor.fire_res != 0:
            self.fire_res -= armor.fire_res
        if armor.electricity_res != 0:
            self.electricity_res -= armor.electricity_res
        if armor.water_res != 0:
            self.water_res -= armor.water_res

    def use_consumable(self, consumable):
        if type(consumable) not in [Consumable]:
            raise Exception(f'Invalid consumable {consumable.name} of type {consumable.type} used by {self.name}.')
        elif consumable.uses <= 0:
            raise Exception(f'Consumable {consumable.name} used by {self.name} had {consumable.uses} uses.')
        else:
            out = f'The {consumable.type.name}:'

            if consumable.health != 0:
                result = self.restore_health(consumable.health)

                if result > 0:
                    out += f'\nRestores {result} health'
                else:
                    out += f'\nDrains {result} health'

            if consumable.stamina != 0:
                result = self.restore_stamina(consumable.stamina)

                if result > 0:
                    out += f'\nRestores {result} stamina'
                else:
                    out += f'\nDrains {result} stamina'

            if consumable.mana != 0:
                result = self.restore_mana(consumable.mana)

                if result > 0:
                    out += f'\nRestores {result} mana'
                else:
                    out += f'\nDrains {result} mana'

            consumable.uses -= 1

            if consumable.uses < 1:
                self.remove_from_inventory(consumable)
                out += '\n... and was consumed'

            self.save()
            return out

    def restore_health(self, amount):
        start = self.current_health
        self.current_health += amount

        if self.current_health > self.health:
            self.current_health = self.health

        return self.current_health - start

    def restore_stamina(self, amount):
        start = self.current_stamina
        self.current_stamina += amount

        if self.current_stamina > self.stamina:
            self.current_stamina = self.stamina

        return self.current_stamina - start

    def restore_mana(self, amount):
        start = self.current_mana
        self.current_mana += amount

        if self.current_mana > self.mana:
            self.current_mana = self.mana

        return self.current_mana - start

    def restore_all(self, h, s, m):
        return self.restore_health(h), self.restore_stamina(s), self.restore_mana(m)

    def recover(self):
        percentage = 0.1
        return self.restore_all(int(self.health * percentage), int(self.stamina * percentage),
                                int(self.mana * percentage))

    def regen(self):
        h = 0
        s = 0
        m = 0
        return self.restore_all(h, s, m)

    def deal_damage(self, effect, critical=False):
        dmgs = []

        if effect.type == ability.EffectType.damage_health:
            if type(effect) == skill.SkillEffect:
                weapon = self.equipped['weapon']
                for dmg in weapon.damages:
                    min = int(dmg[0] * effect.damage_scaling)
                    max = int(dmg[1] * effect.damage_scaling)
                    # TODO apply element scaling
                    # TODO apply active character effects

                    if critical:
                        dmgs.append((max, dmg[2]))
                    else:
                        dmgs.append((random.randint(min, max), dmg[2]))
            elif type(effect) == spell.SpellEffect:
                min = effect.min
                max = effect.max
                # TODO apply element scaling
                # TODO apply active character effects

                if critical:
                    dmgs.append((max, effect.element))
                else:
                    dmgs.append((random.randint(min, max), effect.element))
        else:
            raise Exception(f'{self.name} called deal damage with invalid effect type {type(effect)}')

        return dmgs

    def take_damage(self, dmgs: list):
        for dmg in dmgs:
            if dmg[1] == Elements.earth:
                dmg[0] *= (1.0 - self.earth_res)
            elif dmg[1] == Elements.fire:
                dmg[0] *= (1.0 - self.fire_res)
            elif dmg[1] == Elements.electricity:
                dmg[0] *= (1.0 - self.electricity_res)
            elif dmg[1] == Elements.water:
                dmg[0] *= (1.0 - self.water_res)

            self.current_health -= round(dmg[0])
            self.current_health = max(0, self.current_health)

        return dmgs

    def gain_xp(self, xp: int, level: int):
        gain = utilities.scale_xp(xp, self.level, level)
        self.xp += gain
        self.save()
        return gain


xp_table = {
    1: 0,
    2: 1000,
    3: 2500,
    4: 5000,
    5: 8000,
    6: 11000,
    7: 15000,
    8: 18500,
    9: 22500,
    10: 27000,
    11: 31500,
    12: 36500,
    13: 41500,
    14: 47000,
    15: 52500,
    16: 58000,
    17: 64000,
    18: 70000,
    19: 76500,
    20: 83000,
    21: 89500,
    22: 96000,
    23: 103000,
    24: 110500,
    25: 117500,
    26: 125000,
    27: 132000,
    28: 140000,
    29: 148000,
    30: 156000,
    31: 164000,
    32: 173000,
    33: 181000,
    34: 190000,
    35: 198000,
    36: 207000,
    37: 216000,
    38: 225000,
    39: 235000,
    40: 250000,
}
