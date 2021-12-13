import random

import room


class Biome(object):
    def __init__(self, name: str, room_tags: list[str], enemy_tags: dict):
        self.name = name
        self.room_tags = room_tags
        self.enemy_tags = enemy_tags

    def get_random_room(self, depth: int) -> room.Room:
        candidates = []

        for tag in self.room_tags:
            candidates.append(random.choice(room.rooms[tag][1]))

            if depth >= 21:
                candidates.append(random.choice(room.rooms[tag][21]))

        return random.choice(candidates)

    @staticmethod
    def get_tutorial_room_by_depth(depth: int):
        return room.rooms['basic'][1][depth - 1]


biomes = {
    'generic': Biome('generic',
                     ['basic'],
                     {
                         1: ['slime', 'scarab', 'spider'],
                         21: [],
                     }),
    'infernal': Biome('infernal',
                      ['infernal'],
                      {
                          1: ['imp', 'bomb', 'ash_devil', 'damned_soul'],
                          21: ['cinder_demon', 'lust_demon'],
                      }),
    # Arcane - golems, animated workers (picks, carts, etc.), electric weak
    # Necromantic - undead workers, undead overseers, fire weak
    # Eldritch - weird angles, impossible loops, moving corridors, horrors (dust, insects), earth weak
    # Verdant - damp, mossy, simians, exotic birds - map only
    # Ancestral - ruins, evidence of civilization, ghosts, feral former domestic animals - map only
    # Clockwork - gears, steam, mechanical robots - map only
}
