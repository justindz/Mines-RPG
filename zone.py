import loot_encounter
import utilities
import biome
from biome import Biome
import fight_encounter
from character import Character


class Zone(object):
    def __init__(self, name: str, level: int, description: str, _biome: Biome):
        self.name = name
        self.level = level
        self.description = description
        self.biome = _biome

    def get_next_room(self, connection, characters: [Character], depth: int):
        room = self.biome.get_random_room()

        if depth % 1 == 5:
            room.encounter = loot_encounter.Loot(connection, characters, depth)
        else:
            room.encounter = fight_encounter.get_random_fight(self.biome.enemy_tags, characters, depth)

        return room


zones = [
    Zone('Boon Mine', 1, 'The first mineshaft discovered in the area, around which the encampment formed. New players are recommended to begin here.', biome.biomes['generic']),
]


def get_zone_list():
    zone_list = '---------------MINES---------------\n'

    i = 0
    for zone in zones:
        zone_list += '#{}: {} ({}) - {}\n'.format(i, zone.name, zone.level, zone.description)
        i += 1
    zone_list += '-----------------------------------'
    return utilities.blue(zone_list)
