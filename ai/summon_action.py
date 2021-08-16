from ability import EffectType, Effect
from elements import Elements
from ai.action import Action


class SummonAction(Action):
    def __init__(self, name: str, cooldown: int, enemy_strs: [str], description: str):
        if len(enemy_strs) == 0:
            raise Exception(f'Incorrect enemies and levels lists provided to summon action {name}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.effects = [Effect(EffectType.summon, Elements.earth, _status_effect_value=1)]  # required for planner to pick up the action
        self.enemy_strs = enemy_strs
        self.description = description

    def do(self, user, target, fight):
        """The 'target' parameter is required, but unused for the summon action."""
        out = f'{user.name} used {self.name}\n{self.description}'

        for enemy_str in self.enemy_strs:
            name = fight.add_enemy(enemy_str)
            out += f'\n{name} appeared!'

        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
