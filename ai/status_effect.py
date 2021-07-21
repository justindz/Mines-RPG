from ai.action import Action
from spell import SpellEffect
from ability import EffectType


class StatusEffect(Action):
    def __init__(self, name: str, cooldown: int, effects: [SpellEffect], debuff=True):
        for effect in effects:
            if effect.type not in [EffectType.buff, EffectType.debuff]:
                raise Exception(f'StatusEffect {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = cooldown
        self.effects = effects

        if debuff:
            self.targets_players = True
            self.targets_allies = False
        else:
            self.targets_players = False
            self.targets_allies = True

        self.area = 0
        self.area_modifiable = False

    def do(self, user, target, fight):
        out = f'{user.name} used {self.name} on {target.name}.'
        targets = [target]

        if self.area > 0:
            i = self.area

            while i > 0:
                if fight.enemies.index(target) + i <= len(fight.enemies) - 1:
                    targets.append(fight[fight.enemies.index(target) + i])

                if fight.enemies.index(target) - i > 0:
                    targets.insert(0, fight[fight.enemies.index(target) - i])

                i -= 1

        for target in targets:
            for effect in self.effects:
                overwrite = target.apply_status_effect(effect.status_effect_name, effect.stat, effect.min,
                                                       effect.status_effect_turns)
                out += f'\n{target.name} has been affected by {effect.status_effect_name}.'

                if overwrite is not None:
                    out += f' The existing {overwrite} was replaced.'

        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
