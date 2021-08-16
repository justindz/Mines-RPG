from ai.action import Action
from ability import EffectType, Effect
import dice


class SingleTargetHeal(Action):
    def __init__(self, name: str, cooldown: int, effects: [Effect]):
        for effect in effects:
            if effect.type != EffectType.restore_health:
                raise Exception(f'SingleTargetHeal {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.effects = effects
        self.targets_opponents = False
        self.targets_allies = True
        self.area = 0
        self.area_modifiable = False

    def do(self, user, target, fight):
        out = f'{user.name} used {self.name} on {target.name}.'
        targets = super().get_aoe_targets(fight, target)

        for target in targets:
            for effect in self.effects:
                heal = target.restore_health(dice.roll(dice.count(user.level), effect.dice_value), user)
                out += f'\n{target.name} regained {heal} health.'

        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
