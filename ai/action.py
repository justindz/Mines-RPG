from elements import Elements


class Action:
    def __init__(self):
        self.name = 'Default Action'
        self.description = 'Report a bug and reference the enemy that used this ability!'
        self.effects = []
        self.cooldown = 0
        self.turns_remaining = 0
        self.activates = []
        self.consumes = []
        self.targets_players = False
        self.targets_allies = False
        self.area = 0
        self.area_modifiable = False
        self.summon = None

    def is_usable(self, states: [Elements]):
        return not self.is_on_cooldown() and self.meets_state_requirements(states)

    def check_cooldown(self):
        if self.cooldown > 0 and self.turns_remaining == 0:
            self.turns_remaining += self.cooldown

    def is_on_cooldown(self):
        if self.cooldown > 0 and self.turns_remaining > 0:
            return True

        return False

    def meets_state_requirements(self, states: [Elements]):
        if len(self.consumes) == 0:
            return True

        for state in self.consumes:
            if state not in states:
                return False

        return True

    def handle_elements(self, fight) -> str:
        out = ''

        for state in self.consumes:
            fight.consume(state)
            out += f'\n{state.name.capitalize()} has been consumed.'

        for state in self.activates:
            fight.activate(state)
            out += f'\n{state.name.capitalize()} has been infused.'

        return out
