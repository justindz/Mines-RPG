from elements import Elements
import ability
from ability import EffectType


class SpellEffect:
    def __init__(self, _type, _element, _dice_value=None, _status_effect_value=None, _stat=None,
                 _status_effect_name=None, _status_effect_turns=None):
        if _type in [EffectType.damage_health, EffectType.restore_health, EffectType.restore_stamina,
                     EffectType.restore_mana] and _dice_value is None:
            raise Exception(f'Malformed dice value for SpellEffect: {_type}, {_element}, {_dice_value}')
        if _type in [EffectType.buff, EffectType.debuff] and (_status_effect_name is None or _stat is None or
                                                              _status_effect_turns is None):
            raise Exception(f'Malformed status effect for SpellEffect: {_type}, {_element}, {_status_effect_value}')

        self.type = _type
        self.element = _element
        self.status_effect_value = _status_effect_value
        self.dice_value = _dice_value  # unused for status effects (buff, debuff)
        self.status_effect_name = _status_effect_name
        self.stat = _stat
        self.status_effect_turns = _status_effect_turns


class Spell(ability.Ability):
    def __init__(self, _name, _description, _level, _cost, _effects, _activates, _consumes, _area=0,
                 _area_modifiable=False, _base_crit_chance=0.05, _targets_enemies=True, _summon=None):
        super().__init__(_name, _description, _level, _cost, _effects, _activates, _consumes, _area, _area_modifiable)

        if _summon is None:
            _summon = []

        self.base_crit_chance = _base_crit_chance
        self.targets_enemies = _targets_enemies
        self.summon = _summon


spells = {
    'stalagmite': Spell('Stalagmite', 'Stalagmite description.', 1, {'h': 0, 's': 0, 'm': 5},
                        [SpellEffect(EffectType.damage_health, Elements.earth, _dice_value=4)], [], [Elements.earth],
                        _targets_enemies=True),
    'mend_wounds': Spell('Mend Wounds', 'Mend description.', 1, {'h': 0, 's': 0, 'm': 5},
                         [SpellEffect(EffectType.restore_health, Elements.water, _dice_value=6),
                          SpellEffect(EffectType.restore_stamina, Elements.water, _dice_value=6)],
                         [], [], _base_crit_chance=0.01, _targets_enemies=False),
    'slow': Spell('Slow', 'Slow description.', 1, {'h': 0, 's': 0, 'm': 8},
                  [SpellEffect(EffectType.debuff, Elements.electricity, _status_effect_value=-5, _stat='bonus_init',
                               _status_effect_name='Slowed', _status_effect_turns=2)], [], []),
    'haste': Spell('Haste', 'Haste description.', 1, {'h': 0, 's': 0, 'm': 8},
                   [SpellEffect(EffectType.buff, Elements.electricity, _status_effect_value=5, _stat='bonus_init',
                                _status_effect_name='Hasted', _status_effect_turns=2)], [], [], _targets_enemies=False),
    'summon_coal_golem': Spell('Summon Coal Golem', 'Summon Coal Golem description.', 1, {'h': 0, 's': 0, 'm': 8}, [],
                               [], [], _targets_enemies=False, _summon=['coal_golem']),
}
