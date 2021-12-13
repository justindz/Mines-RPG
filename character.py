import datetime
from pymodm import MongoModel, fields
from pymongo import WriteConcern

import ability
from items import item, book
import utilities
from items.item import ItemType
from elements import Elements
import dice


class Character(MongoModel):
    name = fields.CharField(required=True)
    created = fields.DateTimeField(default=datetime.datetime.utcnow())

    level = fields.IntegerField(default=1)
    xp = fields.IntegerField(default=0)
    coins = fields.IntegerField(default=0)
    strength = fields.IntegerField(default=0)
    bonus_strength = fields.IntegerField(default=0)
    intelligence = fields.IntegerField(default=0)
    bonus_intelligence = fields.IntegerField(default=0)
    dexterity = fields.IntegerField(default=0)
    bonus_dexterity = fields.IntegerField(default=0)
    willpower = fields.IntegerField(default=0)
    bonus_willpower = fields.IntegerField(default=0)
    health = fields.IntegerField(default=100)
    bonus_health = fields.IntegerField(default=0)
    current_health = fields.IntegerField(default=100)
    health_regen = fields.IntegerField(default=0)
    bonus_health_regen = fields.IntegerField(default=0)
    stamina = fields.IntegerField(default=100)
    bonus_stamina = fields.IntegerField(default=0)
    current_stamina = fields.IntegerField(default=100)
    stamina_regen = fields.IntegerField(default=0)
    bonus_stamina_regen = fields.IntegerField(default=0)
    mana = fields.IntegerField(default=100)
    bonus_mana = fields.IntegerField(default=0)
    current_mana = fields.IntegerField(default=100)
    mana_regen = fields.IntegerField(default=0)
    bonus_mana_regen = fields.IntegerField(default=0)
    init = fields.IntegerField(default=0)
    bonus_init = fields.IntegerField(default=0)
    carry = fields.IntegerField(default=100)
    bonus_carry = fields.IntegerField(default=0)
    current_carry = fields.IntegerField(default=0)

    earth_res = fields.FloatField(default=0.0)
    bonus_earth_res = fields.FloatField(default=0.0)
    fire_res = fields.FloatField(default=0.0)
    bonus_fire_res = fields.FloatField(default=0.0)
    electricity_res = fields.FloatField(default=0.0)
    bonus_electricity_res = fields.FloatField(default=0.0)
    water_res = fields.FloatField(default=0.0)
    bonus_water_res = fields.FloatField(default=0.0)
    dot_res = fields.FloatField(default=0.0)
    bonus_dot_res = fields.FloatField(default=0.0)
    dot_reduction = fields.IntegerField(default=0)
    bonus_dot_reduction = fields.IntegerField(default=0)
    dot_effect = fields.FloatField(default=0.0)
    bonus_dot_effect = fields.FloatField(default=0.0)
    dot_duration = fields.IntegerField(default=0)
    bonus_dot_duration = fields.IntegerField(default=0)

    points = fields.IntegerField(default=0)
    abilities = fields.ListField(default=['skill-strike'])
    ability_slots = fields.DictField(default={'1': 'skill-strike', '2': None, '3': None, '4': None})

    eq_weapon = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)
    eq_head = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)
    eq_chest = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)
    eq_belt = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)
    eq_boots = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)
    eq_gloves = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)
    eq_amulet = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)
    eq_ring = fields.EmbeddedDocumentField(item.Item, default=None, blank=True)

    inventory = fields.EmbeddedDocumentListField(item.Item, default=[], blank=True)
    bank = fields.EmbeddedDocumentListField(item.Item, default=[], blank=True)
    bank_limit = fields.IntegerField(default=10)
    shop = fields.EmbeddedDocumentListField(item.Item, default=[], blank=True)

    depths = fields.DictField(default={})
    profession = fields.CharField(default='')
    deaths = fields.IntegerField(default=0)
    status_effects = fields.ListField(default=[])  # list of dicts w/ keys = name, stat, value, turns_remaining
    burn = fields.DictField(default={'turns': 0, 'dmg': 0})
    bleed = fields.DictField(default={'turns': 0, 'dmg': 0})
    shock = fields.IntegerField(default=0)
    shock_limit = fields.IntegerField(default=5)
    bonus_shock_limit = fields.IntegerField(default=0)
    confusion = fields.IntegerField(default=0)
    confusion_limit = fields.IntegerField(default=5)
    bonus_confusion_limit = fields.IntegerField(default=0)

    class Meta:
        write_concern = WriteConcern(j=True)

    def reset_stats(self):
        self.current_health = self.health + self.bonus_health
        self.current_stamina = self.stamina + self.bonus_stamina
        self.current_mana = self.mana + self.bonus_mana
        self.remove_all_status_effects()
        self.save()

    def learn(self, _book) -> bool:
        if _book.level <= self.level and self.add_ability(book.get_ability_string(_book)):
            self.remove_from_inventory(_book)
            return True

        return False

    def add_ability(self, ability_string: str) -> bool:
        if ability_string not in self.abilities:
            self.abilities.append(ability_string)
            self.save()
            return True

        return False

    def assign_ability_to_slot(self, index: int, slot: int) -> bool:
        if 0 < slot < 7 and 0 <= index < len(self.abilities):
            slot = str(slot)
            self.ability_slots[slot] = self.abilities[index]
            self.save()
            return True

        return False

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
        if item.itype not in [ItemType.weapon.value, ItemType.head.value, ItemType.chest.value, ItemType.belt.value,
                              ItemType.boots.value, ItemType.gloves.value, ItemType.amulet.value, ItemType.ring.value]:
            return False

        if self.level < item.level:
            return False

        if item.itype == ItemType.weapon.value:
            if self.strength + self.bonus_strength < item.required_strength:
                return False

            if self.intelligence + self.bonus_intelligence < item.required_intelligence:
                return False

            if self.dexterity + self.bonus_dexterity < item.required_dexterity:
                return False

            if self.willpower + self.bonus_willpower < item.required_willpower:
                return False

        slot = ItemType(item.itype).name

        if getattr(self, 'eq_' + slot) is not None:
            self.unequip(slot)
            self.save()

        if self.level >= item.level:
            self.remove_from_inventory(item, True)
            setattr(self, 'eq_' + slot, item)
            self.update_stats(item, True)
            return True

        return False

    def unequip(self, slot: str):
        if slot not in ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring'] \
                or getattr(self, 'eq_' + slot) is None:
            return False
        else:
            item = getattr(self, 'eq_' + slot)
            setattr(self, 'eq_' + slot, None)
            self.update_stats(item, False)
            self.add_to_inventory(item, True, True)
            return item

    def unequip_all(self):
        for slot in ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring']:
            self.unequip(slot)

    def update_stats(self, item, equip: bool):
        if equip:
            self.apply_equippable_bonuses(item)
        else:
            self.remove_equippable_bonuses(item)

        self.save()

    def apply_equippable_bonuses(self, item):
        for bonus in [x for x in dir(item) if x.startswith('bonus_')]:
            setattr(self, bonus, getattr(self, bonus) + getattr(item, bonus))

    def remove_equippable_bonuses(self, item):
        for bonus in [x for x in dir(item) if x.startswith('bonus_')]:
            setattr(self, bonus, getattr(self, bonus) - getattr(item, bonus))

    def deposit(self, index: int) -> bool:
        if len(self.inventory) - 1 < index < 0 or len(self.bank) >= self.bank_limit:
            return False

        it = self.inventory[index]
        self.bank.append(it)
        self.remove_from_inventory(it)
        return True

    def withdraw(self, index: int) -> bool:
        if len(self.bank) - 1 < index < 0:
            return False

        it = self.bank[index]

        if self.add_to_inventory(it, False):
            cost = len(self.bank)
            self.bank.remove(it)
            self.coins -= cost
            self.save()
            return True

        return False

    def use_consumable(self, consumable):
        if consumable.itype != ItemType.potion.value:
            return f'{consumable.name} is not consumable.'
        elif consumable['uses'] <= 0:
            raise Exception(f'Consumable {consumable.name} used by {self.name} had {consumable.uses} uses.')
        else:
            out = f'The {ItemType(consumable.itype).name}:'

            if consumable.health != 0:
                result = self.restore_health(consumable.health)

                if result >= 0:
                    out += f'\nRestores {result} health'
                else:
                    out += f'\nDrains {result} health'

            if consumable.stamina != 0:
                result = self.restore_stamina(consumable.stamina)

                if result >= 0:
                    out += f'\nRestores {result} stamina'
                else:
                    out += f'\nDrains {result} stamina'

            if consumable.mana != 0:
                result = self.restore_mana(consumable.mana)

                if result >= 0:
                    out += f'\nRestores {result} mana'
                else:
                    out += f'\nDrains {result} mana'

            if consumable.burn != 0:
                result = self.affect_burning(consumable.burn)

                if result != 0:
                    out += f'\nBurning duration {result:+}'

            if consumable.bleed != 0:
                result = self.affect_bleeding(consumable.bleed)

                if result != 0:
                    out += f'\nBleeding duration {result:+}'

            if consumable.shock != 0:
                result = self.affect_shock(consumable.shock)

                if result != 0:
                    out += f'\nShock level {result:+}'

            if consumable.confusion != 0:
                result = self.affect_confusion(consumable.confusion)

                if result != 0:
                    out += f'\nConfusion level {result:+}'

            consumable.uses -= 1

            if consumable.uses < 1:
                self.remove_from_inventory(consumable)
                # consumable.delete()
                out += '\n... and was consumed'

            self.save()
            return out

    def has_consumables(self):
        for item in self.inventory:
            if item.itype == ItemType.potion.value:
                return True

        return False

    def restore_health(self, amount: int, source=None):
        start = self.current_health

        if source is not None and isinstance(source, Character):
            self.current_health += int(amount * source.get_element_scaling(Elements.water))
        else:
            self.current_health += amount

        if self.current_health > self.health + self.bonus_health:
            self.current_health = self.health + self.bonus_health

        return self.current_health - start

    def restore_stamina(self, amount: int, source=None):
        start = self.current_stamina

        if source is not None and isinstance(source, Character):
            self.current_stamina += int(amount * source.get_element_scaling(Elements.water))
        else:
            self.current_stamina += amount

        if self.current_stamina > self.stamina + self.bonus_stamina:
            self.current_stamina = self.stamina + self.bonus_stamina

        return self.current_stamina - start

    def restore_mana(self, amount: int, source=None):
        start = self.current_mana

        if source is not None and isinstance(source, Character):
            self.current_mana += int(amount * source.get_element_scaling(Elements.water))
        else:
            self.current_mana += amount

        if self.current_mana > self.mana + self.bonus_mana:
            self.current_mana = self.mana + self.bonus_mana

        return self.current_mana - start

    def restore_all(self, h: int, s: int, m: int):
        return self.restore_health(h), self.restore_stamina(s), self.restore_mana(m)

    def recover(self):
        percentage = 0.1
        return self.restore_all(0, int((self.stamina + self.bonus_stamina) * percentage),
                                int((self.mana + self.bonus_mana) * percentage))

    def regen(self):
        return self.restore_all(self.health_regen + self.bonus_health_regen,
                                self.stamina_regen + self.bonus_stamina_regen, self.mana_regen + self.bonus_mana_regen)

    def affect_burning(self, turns: int) -> int:
        start = self.burn['turns']
        self.burn['turns'] = max(self.burn['turns'] + turns, 0)

        if self.burn['turns'] == 0:
            self.burn['dmg'] = 0

        return self.burn['turns'] - start

    def affect_bleeding(self, turns: int) -> int:
        start = self.bleed['turns']
        self.bleed['turns'] = max(self.bleed['turns'] + turns, 0)

        if self.bleed['turns'] == 0:
            self.bleed['dmg'] = 0

        return self.bleed['turns'] - start

    def affect_shock(self, amount: int) -> int:
        start = self.shock
        self.shock = utilities.clamp(self.shock + amount, 0, self.shock_limit + self.bonus_shock_limit)
        return self.shock - start

    def affect_confusion(self, amount: int) -> int:
        start = self.confusion
        self.confusion = utilities.clamp(self.confusion + amount, 0, self.confusion_limit + self.bonus_confusion_limit)
        return self.confusion - start

    def get_ele_pens(self) -> tuple:
        if self.eq_weapon is None:
            return 0.0, 0.0, 0.0, 0.0

        return self.eq_weapon.earth_penetration, self.eq_weapon.fire_penetration, self.eq_weapon.electricity_penetration, self.eq_weapon.water_penetration

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
            raise Exception(f'{self.name} called character get_element_scaling with invalid element {element.name}')

        return 1.0 + (stat / 1000)

    def apply_element_damage_resistances(self, amt: int, element) -> float:
        if element == Elements.earth:
            amt *= (1.0 - (self.earth_res + self.bonus_earth_res))
        elif element == Elements.fire:
            amt *= (1.0 - (self.fire_res + self.bonus_fire_res))
        elif element == Elements.electricity:
            amt *= (1.0 - (self.electricity_res + self.bonus_electricity_res))
        elif element == Elements.water:
            amt *= (1.0 - (self.water_res + self.bonus_water_res))
        return amt

    def deal_damage(self, effect, critical=False, multi=1.0):
        dmgs = []

        if effect.type == ability.EffectType.damage_health:
            if effect.element is None:
                weapon = self.eq_weapon

                for dmg in weapon.damages:
                    total = dice.roll(dmg[0], dmg[1], critical)
                    total *= self.get_element_scaling(Elements(dmg[2]))
                    total = round(total * multi)

                    if critical:
                        total += weapon.crit_damage

                    dmgs.append((total, Elements(dmg[2])))
            elif type(effect) == ability.Effect:
                total = dice.roll(dice.count(self.level), effect.dice_value, critical)
                total *= self.get_element_scaling(effect.element)
                total = round(total)
                dmgs.append((total, effect.element))
        else:
            raise Exception(f'{self.name} called character deal damage with invalid effect type {type(effect)}')

        return dmgs

    def take_damage(self, dmgs: list, ele_pens: tuple) -> list:
        """ele_pens unused on players, but passed in for compability with summon vs. enemy planners (and vice versa)"""
        for dmg in dmgs:
            amt = self.apply_element_damage_resistances(dmg[0], dmg[1])
            self.current_health -= round(amt)
            self.current_health = max(0, self.current_health)

        return dmgs

    def estimate_damage_from_enemy_action(self, enemy, action) -> int:
        amt = 0

        for effect in action.effects:
            if effect.type == ability.EffectType.damage_health:
                element_scaling = enemy.get_element_scaling(effect.element)
                avg = (dice.count(enemy.level) * effect.dice_value) / 2 + element_scaling
                avg += int((dice.count(enemy.level) * effect.dice_value - avg) * action.base_crit_chance)
                amt += self.apply_element_damage_resistances(avg, effect.element)
            elif effect.type in [ability.EffectType.burn, ability.EffectType.bleed]:
                turns = effect.effect_turns + enemy.dot_duration - self.dot_reduction - self.bonus_dot_reduction
                turns = min(turns, 0)
                amt += round(effect.dot_value * (1.0 + enemy.dot_effect - self.dot_res - self.dot_bonus_res)) * turns

        return amt

    def apply_status_effect(self, name: str, stat: str, value: int, turns_remaining: int):
        remove = None
        ret = None

        for se in self.status_effects:
            if se['name'] == name:
                remove = se
                break

        if remove is not None:
            self.remove_status_effect(remove)

        self.status_effects.append({'name': name, 'stat': stat, 'value': value, 'turns_remaining': turns_remaining})
        setattr(self, stat, getattr(self, stat) + value)
        self.save()

        if remove is not None:
            ret = remove['name']

        return ret

    def remove_status_effect(self, se):
        try:
            setattr(self, se['stat'], getattr(self, set['stat'] - se['value']))
            self.status_effects.remove(se)
        except KeyError:
            raise Exception(f'remove_status_effect failed for {self.name}: {se["name"]}, {se["stat"]}')

    def remove_all_status_effects(self):
        for se in self.status_effects:
            self.remove_status_effect(se)

    def list_active_effects(self):
        out = ''

        for se in self.status_effects:
            out += se['name'] + ', '

        return out.rstrip(', ')

    def countdown_status_effects(self):
        removes = []
        out = ''

        for se in self.status_effects:
            if se['turns_remaining'] > 1:
                se['turns_remaining'] -= 1
            else:
                removes.append(se)

        if len(removes) > 0:
            for se in removes:
                out += f'{se["name"]} expired on {self.name}\n'
                self.remove_status_effect(se)

        self.save()
        return out

    def apply_burn(self, turns: int, dmg: int, strength: float, duration: int) -> bool:
        turns += duration - self.dot_reduction - self.bonus_dot_reduction
        turns = max(turns, 0)
        dmg = round(dmg * (1.0 + strength - self.dot_res - self.dot_bonus_res))

        if turns * dmg > self.burn['turns'] * self.burn['dmg']:
            self.burn['turns'] = turns
            self.burn['dmg'] = dmg
            self.save()
            return True

        return False

    def apply_bleed(self, turns: int, dmg: int, strength: float, duration: int) -> bool:
        pre_turns = self.bleed['turns']
        turns += duration - self.dot_reduction - self.bonus_dot_reduction
        turns = max(turns, 0)
        dmg = round(dmg * (1.0 + strength - self.dot_res - self.dot_bonus_res))
        self.bleed['turns'] += turns
        self.bleed['dmg'] += dmg
        self.save()
        return True if pre_turns == 0 else False

    def apply_damage_over_time(self):
        out = ''

        if self.burn['turns'] <= 0 and self.bleed['turns'] <= 0:
            return None  # no DOT occurred

        if self.burn['turns'] > 0:
            self.current_health -= self.burn['dmg']
            self.current_health = max(0, self.current_health)
            self.burn['turns'] -= 1
            out += f'{self.name} burned for {self.bleed["dmg"]} damage.'

            if self.burn['turns'] == 0:
                self.burn['dmg'] = 0

        if self.bleed['turns'] > 0:
            self.current_health -= self.bleed['dmg']
            self.current_health = max(0, self.current_health)
            self.bleed['turns'] -= 1
            out += f'{self.name} bled for {self.burn["dmg"]} damage.'

            if self.bleed['turns'] == 0:
                self.bleed['dmg'] = 0

        if self.current_health <= 0:
            return True, out
        else:
            return False, out

    def end_of_turn(self):
        out = ''
        h, s, m = self.regen()

        if h > 0 or s > 0 or m > 0:
            out += f'{self.name} regenerates {h}h {s}s {m}m.\n'

        if self.burn['turns'] > 0:
            self.burn['turns'] -= 1

            if self.burn['turns'] == 0:
                self.burn['dmg'] = 0
                out += f'{self.name} has stopped burning.\n'

        return out + self.countdown_status_effects()

    def has_completed_tutorial(self) -> bool:
        if 'Boon Mine' in self.depths.keys() and self.depths['Boon Mine'] >= 10:
            return True

        return False

    def get_depth_progress(self, zone_name: str) -> int:
        if zone_name in self.depths.keys():
            return self.depths[zone_name]
        else:
            return 0

    def update_depth_progress(self, zone, depth: int) -> bool:
        if zone.name in self.depths.keys() and depth <= self.depths[zone.name]:
            return False

        highest = 0

        for key in self.depths.keys():
            if self.depths[key] > highest:
                highest = self.depths[key]

        self.depths[zone.name] = depth
        self.save()

        if depth % 5 == 0 and depth > highest:
            self.points += 1
            self.save()
            return True

    def restock(self, items: list):
        self.shop = []
        self.shop += items
        self.save()

    @staticmethod
    def display_level_up_menu(threshold=False):
        if threshold:
            return 'Choose one:\n1 - Earth Resistance +1%\n2 - Fire Resistance +1%\n3 - Electricity Resistance +1%\n4 - Water Resistance +1%\n5 - DOT Resistance +3%\n6 - DOT Strength +3%'
        else:
            return 'Choose one:\n1 - Strength +3\n2 - Intelligence +3\n3 - Dexterity +3\n4 - Willpower +3\n5 - Health +5\n6 - Stamina +5\n7 - Mana +5'
