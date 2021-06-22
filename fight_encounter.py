import random
import copy

import utilities
from character import Character
import enemy
from enemy import Enemy
import enemy_group
from elements import Elements
from item import ItemType
import ability
import spell
import skill


def get_random_fight(tags: [str], characters: [Character], depth: int):
    candidates = []
    enemies = []

    for tag in tags:
        candidates.append(random.choice(enemy_group.enemy_groups[tag]))

    for enemy_str in random.choice(candidates)[len(characters) - 1]:
        e = copy.deepcopy(enemy.enemies[enemy_str])
        e.scale(depth)
        enemies.append(e)

    return Fight(enemies, characters)


class Fight:
    def __init__(self, enemies: [enemy.Enemy], characters: [Character]):
        self.enemies = enemies
        self.characters = characters
        self.xp = self.level = self.coins = 0
        self.description = 'You see:'

        for e in self.enemies:
            self.description += '\n {}'.format(e.name)
            self.level += e.level
            self.xp += e.level * 10
            self.coins += e.level

        self.level = int(self.level / len(self.enemies))
        self.inits = characters + enemies
        self.update_turn_order()

    def update_turn_order(self):
        self.inits.sort(key=lambda x: x.init + x.bonus_init, reverse=True)

    def remove_character(self, character: Character):
        self.characters.remove(character)
        self.inits.remove(character)

    def remove_enemy(self, enemy_to_remove: Enemy):
        self.enemies.remove(enemy_to_remove)
        self.inits.remove(enemy_to_remove)

    def use_ability(self, char: Character, ab, target):
        out = f'{char.name} used {ab.name} on {target.name}.'
        targets = [target]

        if ab.area > 0:
            i = ab.area

            while i > 0:
                if ab is spell.Spell and not ab.targets_enemies:
                    if self.characters.index(target) + i <= len(self.characters) - 1:
                        targets.append(self.characters.index(target) + i)

                    if self.characters.index(target) - i > 0:
                        targets.insert(0, self.characters.index(target) - i)
                else:
                    if self.enemies.index(target) + i <= len(self.enemies) - 1:
                        targets.append(self.enemies.index(target) + i)

                    if self.enemies.index(target) - i > 0:
                        targets.insert(0, self.enemies.index(target) - i)

                i -= 1

        crit = False
        chance = None

        if isinstance(ab, skill.Skill):
            chance = min(char.equipped['weapon'].base_crit_chance, 0.5)
        elif isinstance(ab, spell.Spell):
            chance = min(ab.base_crit_chance, 0.5)

        if random.random() <= chance:
            crit = True
            out += f' CRITICAL HIT!'

        for _target in targets:
            for effect in ab.effects:
                if effect.type == ability.EffectType.damage_health:
                    dmgs = _target.take_damage(char.deal_damage(effect, critical=crit))

                    for dmg in dmgs:
                        out += f'\n{_target.name} suffered {dmg[0]} {Elements(dmg[1]).name} damage.'
                elif effect.type == ability.EffectType.restore_health:
                    heal = _target.restore_health(random.randint(effect.min, effect.max), char)
                    out += f'\n{_target.name} regained {heal} health.'
                elif effect.type == ability.EffectType.restore_stamina:
                    stam = _target.restore_stamina(random.randint(effect.min, effect.max), char)
                    out += f'\n{_target.name} regained {stam} stamina.'
                elif effect.type == ability.EffectType.restore_mana:
                    mana = _target.restore_mana(random.randint(effect.min, effect.max), char)
                    out += f'\n{_target.name} regained {mana} mana.'
                else:
                    raise Exception(f'{char.name} used ability {ab.name} with unsupported effect type {effect.type}')

            if _target.current_health <= 0:
                self.enemies.remove(_target)

        return out

    def display_enemy_menu(self):
        out = 'Enemies:'
        i = 1

        for e in self.enemies:
            out += f'\n{i} - {e.name} ({e.level}) {e.current_health}h {e.current_stamina}s {e.current_mana}m'
            i += 1

        return out

    def display_ally_menu(self, ally):
        out = 'Allies:'
        i = 1

        for c in self.characters:
            if c != ally:
                out += f'\n{i} - {c.name} {c.current_health}h {c.current_stamina}s {c.current_mana}m'
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
    def display_ability_menu(character):
        out = 'Abilities:'

        for i in range(1, 6):
            if character.ability_slots[str(i)] is not None:
                _ability = utilities.get_ability_by_name(character.ability_slots[str(i)])
                cost = f'{_ability.cost}'

                if _ability is skill.Skill:
                    cost += 's'
                elif _ability is spell.Spell:
                    cost = 'm'

                out += f'\n {str(i)} - {_ability.name} - {cost}'

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
