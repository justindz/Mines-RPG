import random

#local
from character import Character
from elements import Elements
import utilities
#

def get_random_trap(tags: [str]):
    candidates = []

    for tag in tags:
        candidates.append(random.choice(traps[tag]))

    return random.choice(candidates)

class Trap(object):
    def __init__(self, description: str, stats: [str], difficulty: int, scaling: float, success: str, failure: str, element: Elements):
        self.description = description
        self.stats = stats
        self.difficulty = difficulty
        self.scaling = scaling
        self.success = success
        self.failure = failure
        self.element = element

    def get_result(self, character: Character, depth: int):
        total = 0

        if 'strength' in self.stats:
            total += character.strength
        if 'intelligence' in self.stats:
            total += character.intelligence
        if 'dexterity' in self.stats:
            total += character.dexterity
        if 'willpower' in self.stats:
            total += character.willpower

        return utilities.stat_check(total, self.difficulty, self.scaling, depth)

traps = {
    'basic': [
        Trap('As the party enters the room, a faint clicking sound is audible.', ['dexterity'], 1, 0.3, '{} reacts in time, dodging a needle barrage.', '{} gets hit by a barrage of needles, suffering {} damage.', Elements.earth),
    ],
}
