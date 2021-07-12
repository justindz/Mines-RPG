from elements import Elements
from character import Character


class Action:
    def __init__(self):
        self.name = 'Default Action'
        self.description = 'Report a bug and reference the enemy that used this ability!'
        self.effects = []
        self.cooldown = 0
        self.turns_remaining = 0
        self.state_requirements = []
        self.targets_players = False
        self.targets_allies = False
        self.area = 0
        self.area_modifiable = False
        self.summon = None

    def is_usable(self, states: [Elements], enemies: [Character]):
        if self.targets_allies and len(enemies) == 1:
            return False

        return not self.is_on_cooldown() and self.meets_state_requirements(states)

    def is_on_cooldown(self):
        if self.cooldown > 0 and self.turns_remaining > 0:
            return True

        return False

    def meets_state_requirements(self, states: [Elements]):
        if len(self.state_requirements) == 0:
            return True

        for state in self.state_requirements:
            if state not in states:
                return False

        return True
