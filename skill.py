from elements import Elements
import ability
from ability import EffectType, Effect
from weapon import WeaponType


class Skill(ability.Ability):
    def __init__(self, _name, _description, _level, _cost, _effects, _activates, _consumes, _weapon_types,
                 _multiplier, _area=0, _area_modifiable=False):
        for eff in _effects:
            if eff.type in [EffectType.restore_health, EffectType.restore_stamina, EffectType.restore_mana]:
                raise Exception(f'Skill {_name} includes effect with unsupported type {eff.type}')

        super().__init__(_name, _description, _level, _cost, _effects, _activates, _consumes, _area, _area_modifiable)
        self.weapon_types = _weapon_types
        self.multiplier = _multiplier


skills = {  # Note: Element should always be None for Skill effects--they inherit the weapon element
    'slash': Skill('Slash', 'Slash skill description.', 1,
                   {'h': 0, 's': 5, 'm': 0},
                   [Effect(EffectType.damage_health, None),
                    Effect(EffectType.debuff, None, _status_effect_value=-5, _stat='health_regen',
                           _status_effect_name='Wounded', _status_effect_turns=2)],
                   [Elements.earth], [], [WeaponType.sword, WeaponType.dagger, WeaponType.axe, WeaponType.fist], 1.2,
                   _area=1, _area_modifiable=True),
}
