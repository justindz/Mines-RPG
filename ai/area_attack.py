from ai.action import Action
from ability import EffectType, Effect

import random


class AreaAttack(Action):
    def __init__(self, name: str, cooldown: int, area: int, base_crit_chance: float, effects: [Effect]):
        for effect in effects:
            if effect.type not in [EffectType.damage_health, EffectType.burn, EffectType.bleed]:
                raise Exception(f'AreaAttack {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.base_crit_chance = base_crit_chance
        self.effects = effects
        self.targets_opponents = True
        self.targets_allies = False
        self.area = area
        self.area_modifiable = True

    def do(self, user, target, fight):
        out = f'{user.name} used {self.name} on {target.name}.'
        crit = False
        targets = super().get_aoe_targets(fight.characters, target)

        if random.random() <= self.base_crit_chance:
            crit = True
            out += f' CRITICAL HIT!'

        out = self.deal_damage(crit, fight, out, targets, user)
        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
