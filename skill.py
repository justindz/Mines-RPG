from elements import Elements
import ability
from ability import EffectType
from weapon import WeaponType


class SkillEffect:
    def __init__(self, _type, _damage_scaling):
        self.type = _type
        self.damage_scaling = _damage_scaling  # Scales on equipped weapon base damage


class Skill(ability.Ability):
    def __init__(self, _name, _description, _level, _cost, _effects, _activates, _consumes, _weapon_types, _area=0, _area_modifiable=False):
        super().__init__(_name, _description, _level, _cost, _effects, _activates, _consumes, _area, _area_modifiable)
        self.weapon_types = _weapon_types


skills = {
    'slash': Skill('Slash', 'Slash skill description.', 1,
                   {'h': 0, 's': 5, 'm': 0},
                   [SkillEffect(EffectType.damage_health, 1.0)],
                   [Elements.earth], [], [WeaponType.sword, WeaponType.dagger, WeaponType.axe, WeaponType.fist], 1,
                   _area_modifiable=True),
}
