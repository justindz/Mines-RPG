import random

#local
from character import Character
import utilities
#

def get_random_challenge(tags: [str]):
    candidates = []

    for tag in tags:
        candidates.append(random.choice(challenges[tag]))

    return random.choice(candidates)

class Challenge(object):
    def __init__(self, description: str, stats: [str], difficulty: int, scaling: float, success: str, failure: str):
        self.description = description
        self.stats = stats
        self.difficulty = difficulty
        self.scaling = scaling
        self.success = success
        self.failure = failure

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

challenges = {
    'basic': [
        Challenge('The tunnel deeper into the mine has been blocked by rubble from a cave-in.', ['strength'], 1, 0.3, '{} tosses aside the rubble like used wineskins, and the party is able to move on quickly.', 'With the rest of the party on lookout, {} struggles to clear the rubble, succeeding after some time.'),
    ],
}
