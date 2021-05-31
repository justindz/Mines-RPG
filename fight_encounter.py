import random
import copy

import utilities
from character import Character
import enemy
from enemy import Enemy
import enemy_group
from consumable import Consumable
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


class Fight(object):
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
        self.inits.sort(key=lambda x: x.init, reverse=True)

    def remove_character(self, character: Character):
        self.characters.remove(character)
        self.inits.remove(character)

    def remove_enemy(self, enemy_to_remove: Enemy):
        self.enemies.remove(enemy_to_remove)
        self.inits.remove(enemy_to_remove)

    def use_ability(self, char, ab, target):
        out = f'{char.name} used {ab.name} on {target.name}.'

        for effect in ab.effects:
            if effect.type == ability.EffectType.damage_health:
                dmgs = target.take_damage(char.deal_damage(effect))

                for dmg in dmgs:
                    out += f'\n{target.name} suffered {dmg[0]} {dmg[1].name} damage.'
            else:
                raise Exception(f'{char.name} used ability {ab.name} with unsupported effect type {effect.type}')

        if target.current_health <= 0:
            self.enemies.remove(target)

        return out

    def display_enemy_menu(self):
        out = 'Enemies:'
        i = 1

        for e in self.enemies:
            out += f'\n{i} - {e.name} ({e.level}) {e.current_health}h {e.current_stamina}s {e.current_mana}m'
            i += 1

        return out

    @staticmethod
    def display_action_menu():
        return '1 - Ability\n2 - Item\n3 - Recover'

    @staticmethod
    def display_ability_menu(character):
        out = 'Abilities:'

        for i in range(1, 6):
            if character.ability_slots[i] is not None:
                out += '\n' + str(i) + ' - ' + utilities.get_ability_by_name(character.ability_slots[i]).name

        return out

    @staticmethod
    def display_item_menu(character):
        indices_counter = 0
        display_counter = 1
        display_string = 'Consumables in inventory:'
        indices = []

        for item in character.inventory:
            if type(item) is Consumable:
                display_string += f'\n{display_counter} - {item.name} ({item.uses})'
                display_counter += 1
                indices.append(indices_counter)

            indices_counter += 1

        if indices_counter == 0:
            display_string += '\n None'

        return display_string, indices
