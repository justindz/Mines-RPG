import copy
import random

import enemies
import loot_encounter
import utilities
import biome
from biome import Biome
from character import Character
from fight_encounter import Fight


class Zone(object):
    def __init__(self, name: str, level: int, description: str, _biome: Biome):
        self.name = name
        self.level = level
        self.description = description
        self.biome = _biome

    def get_next_room(self, connection, characters: [Character], depth: int):
        if self.name == 'Boon Mine':
            room = Biome.get_tutorial_room_by_depth(depth)
        else:
            room = self.biome.get_random_room()

        if depth % 5 == 0:
            room.encounter = loot_encounter.Loot(connection, characters)
        else:
            room.encounter = self.get_random_fight(characters, depth)

        return room

    def get_random_fight(self, characters: [Character], depth: int) -> Fight:
        enemy_group = []
        size = 2
        candidates = self.biome.enemy_tags[1]

        if depth >= 21:
            candidates += self.biome.enemy_tags[21]

        if len(characters) == 2:
            size = 4
        elif len(characters) == 3:
            size = 6
        elif len(characters) < 1 or len(characters) > 3:
            raise Exception(f'get_random_fight unexpected party size: {",".join([x.name for x in characters])}')

        for _ in range(1, size + 1):
            e_str = random.choice(candidates)
            e = copy.deepcopy(enemies.enemies[e_str])
            e.scale(depth)
            enemy_group.append(e)

        return Fight(enemy_group, characters)

    @staticmethod
    def get_restart_level(max_depth):
        return max(max_depth - (max_depth % 5) - 4, 1)


zones = [
    Zone('Boon Mine', 1, 'The first mineshaft discovered in the area, around which the encampment formed. New players begin their delving career here.', biome.biomes['generic']),
    Zone('Sulfur Pits', 10, 'This mineshaft reeks of brimstone and sulphur. Unpleasantly warm air wafts from the opening.', biome.biomes['infernal']),
]


def get_zone_list(char: Character):
    zone_list = '---------------MINES---------------\n'

    if char.has_completed_tutorial():
        i = 0
        for zone in zones:
            zone_list += '#{}: {} ({}) - {}\n'.format(i, zone.name, zone.level, zone.description)
            i += 1
    else:
        zone_list += '#0: {} ({}) - {}\n'.format(zones[0].name, zones[0].level, zones[0].description)

    zone_list += '-----------------------------------'
    return utilities.blue(zone_list)
