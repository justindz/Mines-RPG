from ai.action import Action
from character import Character
from elements import Elements
from ability import EffectType, Effect

import random


class SingleTargetAttack(Action):
    def __init__(self, name: str, cooldown: int, base_crit_chance: float, effects: [Effect]):
        for effect in effects:
            if effect.type not in [EffectType.damage_health, EffectType.burn]:
                raise Exception(f'SingleTargetAttack {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.base_crit_chance = base_crit_chance
        self.effects = effects
        self.targets_opponents = True
        self.targets_allies = False
        self.area = 0
        self.area_modifiable = False

    def do(self, user, target, fight):
        out = f'{user.name} used {self.name} on {target.name}.'
        crit = False
        targets = super().get_aoe_targets(fight, target)

        if random.random() <= self.base_crit_chance:
            crit = True
            out += f' CRITICAL HIT!'

        for target in targets:
            for effect in self.effects:
                if effect.type == EffectType.damage_health:
                    dmgs = target.take_damage(user.deal_damage(effect, critical=crit), user.ele_pens)

                    for dmg in dmgs:
                        out += f'\n{target.name} suffered {dmg[0]} {Elements(dmg[1]).name} damage.'
                elif effect.type == EffectType.burn:
                    if target.apply_burn(effect.effect_turns, effect.dot_value,
                                         user.dot_effect, user.dot_duration):
                        out += f'\n{target.name} is burning.'
                    else:
                        out += f'\n{target.name} is already seriously burning.'
                elif effect.type == EffectType.bleed:
                    if target.apply_bleed(effect.effect_turns, effect.dot_value,
                                          user.dot_effect, user.dot_duration):
                        out += f'\n{target.name} is bleeding.'
                    else:
                        out += f'\n{target.name} is bleeding more severely.'

        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
