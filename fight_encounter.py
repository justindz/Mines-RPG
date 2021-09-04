import random
import copy

import utilities
from character import Character
import enemy
from enemy import Enemy
import enemy_group
from enemies import enemies
from summon import Summon
from summons import summons
from elements import Elements
from item import ItemType
import ability
import spell
import skill
import dice


def get_random_fight(tags: [str], characters: [Character], depth: int):
    candidates = []
    _enemies = []

    for tag in tags:
        candidates.append(random.choice(enemy_group.enemy_groups[tag]))

    for enemy_str in random.choice(candidates)[len(characters) - 1]:
        e = copy.deepcopy(enemies[enemy_str])
        e.scale(depth)
        _enemies.append(e)

    return Fight(_enemies, characters)


class Fight:
    def __init__(self, _enemies: [enemy.Enemy], characters: [Character]):
        self.enemies = _enemies
        self.characters = characters
        self.level = self.coins = 0
        self.description = 'You see:'

        for e in self.enemies:
            self.description += f'\n {e.name}'
            self.level += e.level

        self.level = int(self.level / len(self.enemies))
        self.inits = self.characters + self.enemies
        self.update_turn_order()
        self.elements_strong = []
        self.elements_weak = []

    @property
    def states(self):
        return self.elements_strong + self.elements_weak

    def update_turn_order(self):
        self.inits.sort(key=lambda x: x.init + x.bonus_init, reverse=True)

    def add_enemy(self, enemy_str: str):
        e = copy.deepcopy(enemies[enemy_str])
        e.scale(self.level)
        self.enemies.append(e)
        self.inits.append(e)
        self.description += f'\n {e.name}'
        # Note: don't update turn order here, this could cause some enemies to go twice
        return e.name

    def remove_character(self, character: Character):
        self.characters.remove(character)
        self.inits.remove(character)
        return self.unsummon_all_by_character(character)

    def remove_enemy(self, enemy_to_remove: Enemy):
        self.enemies.remove(enemy_to_remove)
        self.inits.remove(enemy_to_remove)

    def summon(self, summon: Summon, owner: Character):
        summon.owner = owner.name
        summon.name = f'{owner.name}\'s {summon.name}'
        self.characters.append(summon)
        self.inits.append(summon)
        return f'{summon.owner} summoned {summon.name}.'

    def unsummon(self, summon: Summon) -> str:
        self.characters.remove(summon)
        self.inits.remove(summon)
        return f'{summon.owner}\'s {summon.name} vanished.'

    def unsummon_all_by_character(self, owner: Character) -> bool:
        i = 0

        for s in [x for x in self.characters if isinstance(x, Summon) and x.owner == owner.name]:
            i += 1
            self.characters.remove(s)
            self.inits.remove(s)

        return True if i > 0 else False

    def unsummon_all(self):
        for s in [x for x in self.characters if isinstance(x, Summon)]:
            self.characters.remove(s)
            self.inits.remove(s)

    def activate(self, element: Elements):
        if element in self.elements_weak:
            self.elements_strong.append(element)
            self.elements_weak.remove(element)
        elif element not in self.elements_weak and element not in self.elements_strong:
            self.elements_strong.append(element)

    def consume(self, element: Elements):
        if element in self.elements_weak:
            self.elements_weak.remove(element)
        elif element in self.elements_strong:
            self.elements_strong.remove(element)

    def end_of_turn(self):
        check = len(self.elements_weak) + len(self.elements_strong)
        self.elements_weak = self.elements_strong.copy()
        self.elements_strong = []

        if check > 0:
            return True

        return False

    def use_ability(self, char: Character, ab, target):
        out = f'{char.name} used {ab.name} on {target.name}.'
        targets = [target]
        i = ab.area

        while i > 0:
            if ab is spell.Spell and not ab.targets_enemies:
                if self.characters.index(target) + i <= len(self.characters) - 1:
                    targets.append(self.characters[self.characters.index(target) + i])

                if self.characters.index(target) - i >= 0:
                    targets.insert(0, self.characters[self.characters.index(target) - i])
            else:
                if self.enemies.index(target) + i <= len(self.enemies) - 1:
                    targets.append(self.enemies[self.enemies.index(target) + i])

                if self.enemies.index(target) - i >= 0:
                    targets.insert(0, self.enemies[self.enemies.index(target) - i])

            i -= 1

        crit = False
        chance = None

        if isinstance(ab, skill.Skill):
            chance = char.equipped['weapon']['base_crit_chance']
        elif isinstance(ab, spell.Spell):
            chance = ab.base_crit_chance

        if random.random() <= chance:
            crit = True
            out += f' CRITICAL HIT!'

        for _target in targets:
            for effect in ab.effects:
                if effect.type == ability.EffectType.damage_health:
                    dmgs = _target.take_damage(char.deal_damage(effect, critical=crit, multi=1.0 if isinstance(ab, spell.Spell) else ab.multiplier), char.get_ele_pens())

                    for dmg in dmgs:
                        out += f'\n{_target.name} suffered {dmg[0]} {Elements(dmg[1]).name} damage.'
                elif effect.type == ability.EffectType.burn:
                    if target.apply_burn(effect.status_effect_turns, effect.status_effect_value,
                                         char.dot_str + char.bonus_dot_str, char.dot_duration + char.bonus_dot_duration):
                        out += f'\n{target.name} is burning.'
                    else:
                        out += f'\n{target.name} is already seriously burning.'
                elif effect.type == ability.EffectType.bleed:
                    if target.apply_bleed(effect.status_effect_turns, effect.status_effect_value,
                                          char.dot_str + char.bonus_dot_str, char.dot_duration + char.bonus_dot_duration):
                        out += f'\n{target.name} is bleeding.'
                    else:
                        out += f'\n{target.name} is bleeding more severely.'
                elif effect.type == ability.EffectType.restore_health:
                    heal = _target.restore_health(dice.roll(dice.count(char.level), effect.dice_value, crit), char)
                    out += f'\n{_target.name} regained {heal} health.'
                elif effect.type == ability.EffectType.restore_stamina:
                    stam = _target.restore_stamina(dice.roll(dice.count(char.level), effect.dice_value, crit), char)
                    out += f'\n{_target.name} regained {stam} stamina.'
                elif effect.type == ability.EffectType.restore_mana:
                    mana = _target.restore_mana(dice.roll(dice.count(char.level), effect.dice_value, crit), char)
                    out += f'\n{_target.name} regained {mana} mana.'
                elif effect.type in [ability.EffectType.buff, ability.EffectType.debuff]:
                    overwrite = _target.apply_status_effect(effect.status_effect_name, effect.stat, effect.status_effect_value,
                                                            effect.status_effect_turns)
                    out += f'\n{_target.name} has been affected by {effect.status_effect_name}.'

                    if overwrite is not None:
                        out += f' The existing {overwrite} was replaced.'
                else:
                    raise Exception(f'{char.name} used ability {ab.name} with unsupported effect type {effect.type}')

        if isinstance(ab, spell.Spell):
            for summ_str in ab.summon:
                s = copy.deepcopy(summons[summ_str])
                out += '\n' + self.summon(s, char)

        for stat in ab.cost.keys():
            cost = ab.cost[stat]

            if stat == 'h':
                char.current_health -= cost
            elif stat == 's':
                char.current_stamina -= cost
            elif stat == 'm':
                char.current_mana -= cost
            else:
                raise Exception(f'{char.name} used ability {ab.name} with unsupported cost {cost} {stat}')

        for state in ab.consumes:
            self.consume(state)
            out += f'\n{state.name.capitalize()} has been consumed.'

        for state in ab.activates:
            self.activate(state)
            out += f'\n{state.name.capitalize()} has been infused.'

        char.save()
        return out

    def display_active_elements(self):
        if len(self.elements_strong) + len(self.elements_weak) > 0:
            out = 'Strong: '

            for ele in self.elements_strong:
                out += f'{utilities.get_elemental_symbol(ele)} '

            out += '\nWeak: '

            for ele in self.elements_weak:
                out += f'{utilities.get_elemental_symbol(ele)} '
        else:
            out = 'No elements are infused in the environment.'

        return out

    def display_enemy_menu(self):
        out = 'Enemies:'
        i = 1

        for e in self.enemies:
            out += f'\n{i} - {e.name} ({e.level}) {e.current_health}h'
            i += 1

        return out

    def display_ally_menu(self, ally):
        out = 'Allies:'
        i = 1

        for c in self.characters:
            if c != ally:
                if isinstance(c, Character):
                    out += f'\n{i} - {c.name} {c.current_health}h {c.current_stamina}s {c.current_mana}m'
                elif isinstance(c, Summon):
                    out += f'\n{i} - {c.owner}\'s {c.name} {c.current_health}h'
            else:
                out += f'\n{i} - YOU {c.current_health}h {c.current_stamina}s {c.current_mana}m'

        return out

    @staticmethod
    def display_action_menu(char: Character):
        if char.has_consumables():
            return '1 - Ability\n2 - Item\n3 - Recover'
        else:
            return '1 - Ability\n2 - Item (None)\n3 - Recover'

    @staticmethod
    def display_ability_cost(cost: dict):
        out = ''

        if cost['h'] > 0:
            out += f'{cost["h"]}h '
        if cost['s'] > 0:
            out += f'{cost["s"]}s '
        if cost['m'] > 0:
            out += f'{cost["m"]}m'

        return out

    @staticmethod
    def display_ability_menu(character):
        out = 'Abilities:'

        for i in range(1, len(character.ability_slots) + 1):
            if character.ability_slots[str(i)] is not None:
                _ability = utilities.get_ability_by_name(character.ability_slots[str(i)])
                cost = f'{Fight.display_ability_cost(_ability.cost)}'
                ability_type = 'Error'

                if isinstance(_ability, skill.Skill):
                    ability_type = 'Skill'
                elif isinstance(_ability, spell.Spell):
                    ability_type = 'Spell'

                activates = ''
                consumes = ''

                if len(_ability.activates) > 0:
                    activates += ' Activates: '

                    for ele in _ability.activates:
                        activates += utilities.get_elemental_symbol(ele) + ' '

                if len(_ability.consumes) > 0:
                    consumes += ' Consumes: '

                    for ele in _ability.consumes:
                        consumes += utilities.get_elemental_symbol(ele) + ' '

                out += f'\n {str(i)} - {_ability.name} ({ability_type}) - {cost}{consumes}{activates}'

        return out

    @staticmethod
    def display_item_menu(character):
        indices_counter = 0
        display_counter = 1
        display_string = 'Consumables in inventory:'
        indices = []

        for item in character.inventory:
            if item['_itype'] in [ItemType.potion.value, ItemType.food.value]:
                display_string += f'\n{display_counter} - {item["name"]} ({item["uses"]})'
                display_counter += 1
                indices.append(indices_counter)

            indices_counter += 1

        if indices_counter == 0:
            display_string += '\n None'

        return display_string, indices
