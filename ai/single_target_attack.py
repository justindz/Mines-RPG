from ai.action import Action
from character import Character
from elements import Elements
from spell import SpellEffect
from ability import EffectType

import random


class SingleTargetAttack(Action):
    def __init__(self, name: str, cooldown: int, base_crit_chance: float, effects: [SpellEffect]):
        for effect in effects:
            if effect.type != EffectType.damage_health:
                raise Exception(f'SingleTargetAttack {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.base_crit_chance = base_crit_chance
        self.effects = effects
        self.targets_players = True
        self.targets_allies = False
        self.area = 0
        self.area_modifiable = False

    def do(self, user, target: Character, fight):
        out = f'{user.name} used {self.name} on {target.name}.'
        crit = False
        targets = super().get_aoe_targets(fight.characters, target)

        if random.random() <= self.base_crit_chance:
            crit = True
            out += f' CRITICAL HIT!'

        for target in targets:
            for effect in self.effects:
                dmgs = target.take_damage(user.deal_damage(effect, critical=crit))

                for dmg in dmgs:
                    out += f'\n{target.name} suffered {dmg[0]} {Elements(dmg[1]).name} damage.'

        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
