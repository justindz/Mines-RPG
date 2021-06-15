import random

import room


class Biome(object):
    def __init__(self, name: str, enemy_tags: list[str], room_tags: list[str], encounter_tags: list[str]):
        self.name = name
        self.enemy_tags = enemy_tags
        self.room_tags = room_tags
        self.encounter_tags = encounter_tags

    def get_random_room(self):
        candidates = []

        for tag in self.room_tags:
            candidates.append(random.choice(room.rooms[tag]))

        return random.choice(candidates)


biomes = {
    'generic': Biome('generic', ['basic'], ['basic'], ['basic']),
    # Infernal - hot, magma, barbed stalagmites, devils, water weak
    # Verdant - damp, mossy, simians, exotic birds
    # Arcane - golems, animated workers (picks, carts, etc.), electric weak
    # Necromantic - undead workers, undead overseers, fire weak
    # Eldritch - weird angles, impossible loops, moving corridors, horrors (dust, insects), earth weak
    # Ancestral - ruins, evidence of civilization, ghosts, feral former domestic animals
    # Clockwork - gears, steam, mechanical robots
}
