import random

#local
import room
#

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
}
