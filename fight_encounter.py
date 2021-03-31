import random
import copy

#local
from character import Character
import enemy
from enemy import Enemy
import enemy_group
import utilities
#

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

    def remove_enemy(self, enemy: Enemy):
        self.enemies.remove(enemy)
        self.inits.remove(enemy)
