from ai.action import Action
from ability import EffectType, Effect


class StatusEffect(Action):
    def __init__(self, name: str, cooldown: int, effects: [Effect], debuff=True):
        for effect in effects:
            if effect.type not in [EffectType.buff, EffectType.debuff]:
                raise Exception(f'StatusEffect {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.effects = effects

        if debuff:
            self.targets_opponents = True
            self.targets_allies = False
        else:
            self.targets_opponents = False
            self.targets_allies = True

        self.area = 0
        self.area_modifiable = False

    def do(self, user, target, fight):
        out = f'{user.name} used {self.name} on {target.name}.'
        targets = super().get_aoe_targets(fight, target)

        for target in targets:
            for effect in self.effects:
                overwrite = target.apply_status_effect(effect.status_effect_name, effect.stat, effect.status_effect_value,
                                                       effect.status_effect_turns)
                out += f'\n{target.name} has been affected by {effect.status_effect_name}.'

                if overwrite is not None:
                    out += f' The existing {overwrite} was replaced.'

        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
