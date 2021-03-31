import discord
import random

#Local
from actor import Actor
import weapon
from weapon import Weapon
from armor import Armor
from elements import Elements
import utilities
#

class Character(Actor):
    def __init__(self, player: discord.Member):
        # Core
        super().__init__()
        # Stats
        self.strength = self.bonus_strength = 0
        self.intelligence = self.bonus_intelligence = 0
        self.dexterity = self.bonus_dexterity = 0
        self.willpower = self.bonus_willpower = 0
        self.health = self.current_health = 100
        self.stamina = self.current_stamina = 100
        self.mana = self.current_mana = 100
        self.bonus_health = self.bonus_stamina = self.bonus_mana = 0
        self.init = self.bonus_init = 0
        self.carry = 500
        self.current_carry = self.bonus_carry = 0

        # Resistances
        self.earth_res = self.fire_res = self.electricity_res = self.water_res = 0.0

        self.points = 0
        self.player = player
        self.name = player.name
        self.equipped = {'weapon':None, 'head':None, 'chest':None, 'belt':None, 'boots':None, 'gloves':None, 'amulet':None, 'ring':None}
        self.inventory = []
        self.add_to_inventory(Weapon(), True)
        self.add_to_inventory(Armor(), True)

    def add_to_inventory(self, item, ignore_carry, unequipping=False):
        if ignore_carry or self.current_carry + item.weight <= self.carry + self.bonus_carry:
            self.inventory.append(item)

            if not unequipping:
                self.current_carry += item.weight

            return True
        return False

    def remove_from_inventory(self, item, equipping=False):
        self.inventory.remove(item)

        if not equipping:
            self.current_carry -= item.weight

    def equip(self, item):
        if self.equipped[item.type.name] is not None:
            self.unequip(item.type.name)

        if self.level >= item.level:
            self.remove_from_inventory(item, True)
            self.equipped[item.type.name] = item
            self.update_stats(item, True)
            return True
        return False

    def unequip(self, slot):
        if slot not in ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring'] or self.equipped[slot] is None:
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

    def attack(self):
        if self.equipped['weapon'] is None:
            raise Exception('Attempted attack by {} with no weapon equipped.'.format(self.name))

        dmgs = []

        for dmg in self.equipped['weapon'].damages:
            dmgs.append([random.randint(dmg[0], dmg[1]), dmg[2]])

        return dmgs

    def gain_xp(self, xp: int, level: int):
        gain = utilities.scale_xp(xp, self.level, level)
        self.xp += gain
        return gain

    xp_table = {
        1:	0,
        2:	1000,
        3:	2500,
        4:	5000,
        5:	8000,
        6:	11000,
        7:	15000,
        8:	18500,
        9:	22500,
        10:	27000,
        11:	31500,
        12:	36500,
        13:	41500,
        14:	47000,
        15:	52500,
        16:	58000,
        17:	64000,
        18:	70000,
        19:	76500,
        20:	83000,
        21:	89500,
        22:	96000,
        23:	103000,
        24:	110500,
        25:	117500,
        26:	125000,
        27:	132000,
        28:	140000,
        29:	148000,
        30:	156000,
        31:	164000,
        32:	173000,
        33:	181000,
        34:	190000,
        35:	198000,
        36:	207000,
        37:	216000,
        38:	225000,
        39:	235000,
        40:	250000,
    }
