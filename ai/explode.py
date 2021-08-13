from ability import EffectType
from spell import SpellEffect
from elements import Elements
from ai.action import Action


class Explode(Action):
    """targets_players and _allies are set to False, which prevents this from being chosen for non-enrage plans."""
    def __init__(self, name: str, effects: [SpellEffect]):
        for effect in effects:
            if effect.type not in [EffectType.damage_health, EffectType.debuff]:
                raise Exception(f'Explode action {name} has an unsupported effect type {effect.type}')

        super().__init__()
        self.name = name
        self.cooldown = 999
        self.effects = effects
        self.targets_opponents = False
        self.targets_allies = False
        self.area = 2
        self.area_modifiable = False
        self.base_crit_chance = 0.0

    def do(self, user, target, fight):
        """target parameter is unused, since Explode is designed to always target all characters"""
        out = f'Enraged {user.name} used {self.name}.'
        targets = super().get_aoe_targets(fight, fight.characters[0])

        for target in targets:
            for effect in self.effects:
                if effect.type == EffectType.damage_health:
                    dmgs = target.take_damage(user.deal_damage(effect, critical=False), user.ele_pens)

                    for dmg in dmgs:
                        out += f'\n{target.name} suffered {dmg[0]} {Elements(dmg[1]).name} damage.'
                elif effect.type == EffectType.debuff:
                    overwrite = target.apply_status_effect(effect.status_effect_name, effect.stat, effect.min,
                                                           effect.status_effect_turns)
                    out += f'\n{target.name} has been affected by {effect.status_effect_name}.'

                    if overwrite is not None:
                        out += f' The existing {overwrite} was replaced.'

        fight.enemies.remove(user)
        out += f'\n{user.name} suffered {user.current_health} damage and died.'
        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
