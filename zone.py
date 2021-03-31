import discord
import random

#local
import utilities
import biome
from biome import Biome
from room import Room
import challenge_encounter
import trap_encounter
import fight_encounter
from character import Character
#

class Zone(object):
    def __init__(self, name: str, level: int, description: str, fight_chance: int, trap_chance: int, loot_chance: int, challenge_chance: int, gather_chance: int, biome: Biome):
        self.name = name
        self.level = level
        self.description = description

        if (fight_chance + trap_chance + loot_chance + challenge_chance + gather_chance != 100):
            raise Exception('Zone {} encounter chances do not add up to 100%.'.format(self.name))
        else:
            self.fight_chance = fight_chance
            self.trap_chance = trap_chance + fight_chance
            self.loot_chance = loot_chance + trap_chance
            self.challenge_chance = challenge_chance + loot_chance
            self.gather_chance = gather_chance + challenge_chance

        self.biome = biome

    def get_next_room(self, characters: [Character], depth: int):
        room = self.biome.get_random_room()
        chance = random.randint(1, 100)

        if chance <= self.fight_chance:
            room.encounter = fight_encounter.get_random_fight(self.biome.enemy_tags, characters, depth)
        elif chance <= self.trap_chance:
            room.encounter = trap_encounter.get_random_trap(self.biome.encounter_tags)
        elif chance <= self.loot_chance:
            room.encounter = None
        elif chance <= self.challenge_chance:
            room.encounter = challenge_encounter.get_random_challenge(self.biome.encounter_tags)
        elif chance <= self.gather_chance:
            room.encounter = None

        return room

zones = [
    Zone('Boon Mine', 1, 'The first mineshaft discovered in the area, around which the encampment formed. New players are recommended to begin here.',
            40, 20, 10, 10, 20, biome.biomes['generic']),
]

def get_zone_list():
    list = '---------------MINES---------------\n'

    i = 0
    for zone in zones:
        list += '#{}: {} ({}) - {}\n'.format(i, zone.name, zone.level, zone.description)
        i += 1
    list += '-----------------------------------'
    return utilities.blue(list)
