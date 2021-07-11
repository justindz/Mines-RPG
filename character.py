import random
import datetime
from mongokit_ng import Document

import ability
from item import ItemType
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
        'depths': dict,
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
        'ability_slots': {'1': 'spell-stalagmite', '2': 'skill-slash', '3': 'spell-mend_wounds', '4': None, '5': None,
                          '6': None},
        'equipped': {'weapon': None, 'head': None, 'chest': None, 'belt': None, 'boots': None, 'gloves': None,
                     'amulet': None, 'ring': None},
        'inventory': [],
        'depths': {},
    }
    use_dot_notation = True
    use_autorefs = True

    def set_current_hsm(self):
        self.current_health = self.health + self.bonus_health
        self.current_stamina = self.stamina + self.bonus_stamina
        self.current_mana = self.mana + self.bonus_mana

    def add_to_inventory(self, item, ignore_carry, unequipping=False):
        if ignore_carry or self.current_carry + item['weight'] <= self.carry + self.bonus_carry:
            self.inventory.append(item)

            if not unequipping:
                self.current_carry += item['weight']

            self.save()
            return True
        return False

    def remove_from_inventory(self, item, equipping=False):
        self.inventory.remove(item)

        if not equipping:
            self.current_carry -= item['weight']

        self.save()

    def equip(self, item):
        if item['_itype'] not in [ItemType.weapon.value, ItemType.head.value, ItemType.chest.value, ItemType.belt.value,
                                  ItemType.boots.value, ItemType.gloves.value, ItemType.amulet.value,
                                  ItemType.ring.value]:
            return False

        if self.level < item['level']:
            return False

        if self.strength + self.bonus_strength < item['required_strength']:
            return False

        if self.intelligence + self.bonus_intelligence < item['required_intelligence']:
            return False

        if self.dexterity + self.bonus_dexterity < item['required_dexterity']:
            return False

        if self.willpower + self.bonus_willpower < item['required_willpower']:
            return False

        slot = ItemType(item['_itype']).name

        if self.equipped[slot] is not None:
            self.unequip(slot)
            self.save()

        if self.level >= item['level']:
            self.remove_from_inventory(item, True)
            self.equipped[slot] = item
            self.update_stats(item, True)
            return True

        return False

    def unequip(self, slot: str):
        if slot not in ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring'] or self.equipped[
                        slot] is None:
            return False
        else:
            item = self.equipped[slot]
            self.equipped[slot] = None
            self.update_stats(item, False)
            self.add_to_inventory(item, True, True)
            return item

    def update_stats(self, item, equip: bool):
        if item['_itype'] == ItemType.weapon.value:
            if equip:
                self.apply_weapon_bonuses(item)
            else:
                self.remove_weapon_bonuses(item)
        elif item['_itype'] in [ItemType.head.value, ItemType.chest.value, ItemType.belt.value,
                                ItemType.boots.value, ItemType.gloves.value, ItemType.amulet.value,
                                ItemType.ring.value]:
            if equip:
                self.apply_armor_bonuses(item)
            else:
                self.remove_armor_bonuses(item)

        self.save()

    def apply_weapon_bonuses(self, weapon):
        self.bonus_strength += weapon['bonus_strength']
        self.bonus_intelligence += weapon['bonus_intelligence']
        self.bonus_dexterity += weapon['bonus_dexterity']
        self.bonus_willpower += weapon['bonus_willpower']
        self.bonus_health += weapon['bonus_health']
        self.bonus_stamina += weapon['bonus_stamina']
        self.bonus_mana += weapon['bonus_mana']
        self.bonus_init += weapon['bonus_init']

    def remove_weapon_bonuses(self, weapon):
        self.bonus_strength -= weapon['bonus_strength']
        self.bonus_intelligence -= weapon['bonus_intelligence']
        self.bonus_dexterity -= weapon['bonus_dexterity']
        self.bonus_willpower -= weapon['bonus_willpower']
        self.bonus_health -= weapon['bonus_health']
        self.bonus_stamina -= weapon['bonus_stamina']
        self.bonus_mana -= weapon['bonus_mana']
        self.bonus_init -= weapon['bonus_init']
        
    def apply_armor_bonuses(self, armor):
        self.bonus_strength += armor['bonus_strength']
        self.bonus_intelligence += armor['bonus_intelligence']
        self.bonus_dexterity += armor['bonus_dexterity']
        self.bonus_willpower += armor['bonus_willpower']
        self.bonus_health += armor['bonus_health']
        self.bonus_stamina += armor['bonus_stamina']
        self.bonus_mana += armor['bonus_mana']
        self.bonus_init += armor['bonus_init']
        self.bonus_carry += armor['bonus_carry']
        self.earth_res += armor['earth_res']
        self.fire_res += armor['fire_res']
        self.electricity_res += armor['electricity_res']
        self.water_res += armor['water_res']

    def remove_armor_bonuses(self, armor):
        self.bonus_strength -= armor['bonus_strength']
        self.bonus_intelligence -= armor['bonus_intelligence']
        self.bonus_dexterity -= armor['bonus_dexterity']
        self.bonus_willpower -= armor['bonus_willpower']
        self.bonus_health -= armor['bonus_health']
        self.bonus_stamina -= armor['bonus_stamina']
        self.bonus_mana -= armor['bonus_mana']
        self.bonus_init -= armor['bonus_init']
        self.bonus_carry -= armor['bonus_carry']
        self.earth_res -= armor['earth_res']
        self.fire_res -= armor['fire_res']
        self.electricity_res -= armor['electricity_res']
        self.water_res -= armor['water_res']

    def use_consumable(self, consumable):
        if consumable['_itype'] not in [ItemType.potion.value, ItemType.food.value]:
            raise Exception(f'Invalid consumable {consumable["name"]} of type {ItemType(consumable["_itype"]).name} used by {self.name}.')
        elif consumable['uses'] <= 0:
            raise Exception(f'Consumable {consumable["name"]} used by {self.name} had {consumable["uses"]} uses.')
        else:
            out = f'The {ItemType(consumable["_itype"]).name}:'

            if consumable['health'] != 0:
                result = self.restore_health(consumable['health'])

                if result >= 0:
                    out += f'\nRestores {result} health'
                else:
                    out += f'\nDrains {result} health'

            if consumable['stamina'] != 0:
                result = self.restore_stamina(consumable['stamina'])

                if result >= 0:
                    out += f'\nRestores {result} stamina'
                else:
                    out += f'\nDrains {result} stamina'

            if consumable['mana'] != 0:
                result = self.restore_mana(consumable['mana'])

                if result >= 0:
                    out += f'\nRestores {result} mana'
                else:
                    out += f'\nDrains {result} mana'

            consumable['uses'] -= 1

            if consumable['uses'] < 1:
                self.remove_from_inventory(consumable)
                out += '\n... and was consumed'

            self.save()
            return out

    def has_consumables(self):
        for item in self.inventory:
            if item['_itype'] in [ItemType.potion.value, ItemType.food.value]:
                return True

        return False

    def restore_health(self, amount: int, source=None):
        start = self.current_health

        if source is not None and isinstance(source, Character):
            self.current_health += amount * source.get_element_scaling(Elements.water)
        else:
            self.current_health += amount

        if self.current_health > self.health + self.bonus_health:
            self.current_health = self.health + self.bonus_health

        return self.current_health - start

    def restore_stamina(self, amount: int, source=None):
        start = self.current_stamina

        if source is not None and isinstance(source, Character):
            self.current_stamina += amount * source.get_element_scaling(Elements.water)
        else:
            self.current_stamina += amount

        if self.current_stamina > self.stamina + self.bonus_stamina:
            self.current_stamina = self.stamina + self.bonus_stamina

        return self.current_stamina - start

    def restore_mana(self, amount: int, source=None):
        start = self.current_mana

        if source is not None and isinstance(source, Character):
            self.current_mana += amount * source.get_element_scaling(Elements.water)
        else:
            self.current_mana += amount

        if self.current_mana > self.mana + self.bonus_mana:
            self.current_mana = self.mana + self.bonus_mana

        return self.current_mana - start

    def restore_all(self, h: int, s: int, m: int):
        return self.restore_health(h), self.restore_stamina(s), self.restore_mana(m)

    def recover(self):
        percentage = 0.1
        return self.restore_all(int((self.health + self.bonus_health) * percentage),
                                int((self.stamina + self.bonus_stamina) * percentage),
                                int((self.mana + self.bonus_mana) * percentage))

    def regen(self):
        h = 0
        s = 0
        m = 0
        return self.restore_all(h, s, m)

    def get_element_scaling(self, element: Elements):
        if element == Elements.earth:
            stat = self.strength + self.bonus_strength
        elif element == Elements.fire:
            stat = self.intelligence + self.bonus_intelligence
        elif element == Elements.electricity:
            stat = self.dexterity + self.bonus_dexterity
        elif element == Elements.water:
            stat = self.willpower + self.bonus_willpower
        else:
            raise Exception(f'{self.name} called get_element_scaling with invalid element {element.name}')

        return 1.0 + (stat / 1000)

    def deal_damage(self, effect, critical=False):
        dmgs = []

        if effect.type == ability.EffectType.damage_health:
            if type(effect) == skill.SkillEffect:
                weapon = self.equipped['weapon']
                for dmg in weapon['damages']:
                    element_scaling = self.get_element_scaling(Elements(dmg[2]))
                    max = int(dmg[1] * effect.damage_scaling * element_scaling)
                    # TODO apply active character effects

                    if critical:
                        dmgs.append((max + weapon['crit_damage'], dmg[2]))
                    else:
                        min = int(dmg[0] * effect.damage_scaling * element_scaling)
                        dmgs.append((random.randint(min, max), dmg[2]))
            elif type(effect) == spell.SpellEffect:
                element_scaling = self.get_element_scaling(effect.element)
                min = effect.min
                max = effect.max
                # TODO apply active character effects

                if critical:
                    dmgs.append((int(max * element_scaling), effect.element))
                else:
                    dmgs.append((int(random.randint(min, max) * element_scaling), effect.element))
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

    def has_completed_tutorial(self):
        if 'Boon Mine' in self.depths.keys() and self.depths['Boon Mine'] >= 10:
            return True

        return False

    def get_depth_progress(self, zone_name: str):
        if zone_name in self.depths.keys():
            return self.depths[zone_name]
        else:
            return 0

    def update_depth_progress(self, zone, depth):
        if zone.name in self.depths.keys() and depth <= self.depths[zone.name]:
            return False

        highest = 0

        for key in self.depths.keys():
            if self.depths[key] > highest:
                highest = self.depths[key]

        self.depths[zone.name] = depth
        self.save()

        if depth % 5 == 0 and depth > highest:
            self.level += 1
            self.points += 1
            self.save()
            return True

    @staticmethod
    def display_level_up_menu():
        return 'Choose one:\n1 - Strength +3\n2 - Intelligence +3\n3 - Dexterity +3\n4 - Willpower +3\n5 - Health +5\n6 - Stamina +5\n7 - Mana +5'
