from items import weapon
from elements import Elements
import ability
from ability import EffectType, Effect
from items.weapon import all_types, bladed_types, melee_types


class Skill(ability.Ability):
    def __init__(self, _name, _description, _cost, _effects, _activates, _consumes, _weapon_types, _multiplier, _area=0,
                 _area_modifiable=False):
        for eff in _effects:
            if eff.type in [EffectType.restore_health, EffectType.restore_stamina, EffectType.restore_mana]:
                raise Exception(f'Skill {_name} includes effect with unsupported type {eff.type}')

        super().__init__(_name, _description, _cost, _effects, _activates, _consumes, _area, _area_modifiable)
        self.weapon_types = _weapon_types
        self.multiplier = _multiplier


skills = {
    'strike': Skill(
        'Strike',
        'Strike skill description.',
        {'h': 0, 's': 5, 'm': 0},
        [Effect(EffectType.damage_health, None)],
        [],
        [],
        all_types,
        1.2),
    'slash': Skill(
        'Slash',
        'Slash skill description.',
        {'h': 0, 's': 8, 'm': 0},
        [
            Effect(EffectType.damage_health, None),
            Effect(EffectType.debuff, None, _dice_value=4, _stat='health_regen', _status_effect_name='Wounded',
                   _effect_turns=2)
        ],
        [Elements.earth],
        [],
        bladed_types,
        1.0,
        _area=1,
        _area_modifiable=True),
    'lacerate': Skill(
        'Lacerate',
        'Slash skill description.',
        {'h': 0, 's': 8, 'm': 0},
        [
            Effect(EffectType.damage_health, None),
            Effect(EffectType.bleed, None, _dot_value=1, _effect_turns=2)
        ],
        [],
        [],
        bladed_types,
        0.8,
        _area=0,
        _area_modifiable=True),
    'jinx': Skill(
        'Jinx',
        'Jinx skill description.',
        {'h': 0, 's': 5, 'm': 0},
        [
            Effect(EffectType.debuff, None, _dice_value=10, _stat='intelligence', _status_effect_name='Stupefied',
                   _effect_turns=3)
        ],
        [Elements.fire],
        [],
        [weapon.WeaponType.magic],
        1.0,
        _area=1,
        _area_modifiable=True),
    'volley': Skill(
        'Volley',
        'Volley skill description.',
        {'h': 0, 's': 8, 'm': 0},
        [Effect(EffectType.damage_health, None)],
        [],
        [],
        [weapon.WeaponType.thrown],
        0.8,
        _area=2,
        _area_modifiable=True),
    'barrage': Skill(
        'Barrage',
        'Barrage skill description.',
        {'h': 0, 's': 20, 'm': 0},
        [
            Effect(EffectType.damage_health, None),
            Effect(EffectType.damage_health, None),
            Effect(EffectType.damage_health, None)
        ],
        [],
        [],
        [weapon.WeaponType.thrown],
        0.4),
    'flurry': Skill(
        'Flurry',
        'Flurry skill description.',
        {'h': 0, 's': 20, 'm': 0},
        [
            Effect(EffectType.damage_health, None),
            Effect(EffectType.damage_health, None),
            Effect(EffectType.damage_health, None)
        ],
        [],
        [],
        [melee_types],
        0.4),
}
