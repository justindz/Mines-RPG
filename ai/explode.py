from ability import EffectType, Effect
from ai.action import Action


class Explode(Action):
    """targets_players and _allies are set to False, which prevents this from being chosen for non-enrage plans."""
    def __init__(self, name: str, effects: [Effect]):
        for effect in effects:
            if effect.type not in [EffectType.damage_health, EffectType.burn, EffectType.bleed, EffectType.debuff,
                                   EffectType.restore_health]:
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
        targets = super().get_aoe_targets(fight.characters, fight.characters[0])
        out = self.deal_damage(False, fight, out, targets, user)
        fight.enemies.remove(user)
        out += f'\n{user.name} suffered {user.current_health} damage and died.'
        out += self.handle_elements(fight)
        self.check_cooldown()
        return out
