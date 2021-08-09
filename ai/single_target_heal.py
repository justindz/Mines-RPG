from ai.action import Action
from spell import SpellEffect
from ability import EffectType

import random


class SingleTargetHeal(Action):
    def __init__(self, name: str, cooldown: int, effects: [SpellEffect]):
        for effect in effects:
            if effect.type != EffectType.restore_health:
                raise Exception(f'SingleTargetHeal {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.effects = effects
        self.targets_players = False
        self.targets_allies = True
        self.area = 0
        self.area_modifiable = False

    def do(self, user, target, fight):
        out = f'{user.name} used {self.name} on {target.name}.'
        targets = super().get_aoe_targets(fight.enemies, target)

        for target in targets:
            for effect in self.effects:
                heal = target.restore_health(random.randint(effect.min, effect.max), user)
                out += f'\n{target.name} regained {heal} health.'

        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
