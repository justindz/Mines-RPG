from elements import Elements
import ability
from ability import EffectType, Effect


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
                        [Effect(EffectType.damage_health, Elements.earth, _dice_value=4)], [], [Elements.earth],
                        _targets_enemies=True),
    'mend_wounds': Spell('Mend Wounds', 'Mend description.', 1, {'h': 0, 's': 0, 'm': 5},
                         [Effect(EffectType.restore_health, Elements.water, _dice_value=6),
                          Effect(EffectType.restore_stamina, Elements.water, _dice_value=6)],
                         [], [], _base_crit_chance=0.01, _targets_enemies=False),
    'slow': Spell('Slow', 'Slow description.', 1, {'h': 0, 's': 0, 'm': 8},
                  [Effect(EffectType.debuff, Elements.electricity, _status_effect_value=-5, _stat='bonus_init',
                          _status_effect_name='Slowed', _status_effect_turns=2)], [], []),
    'haste': Spell('Haste', 'Haste description.', 1, {'h': 0, 's': 0, 'm': 8},
                   [Effect(EffectType.buff, Elements.electricity, _status_effect_value=5, _stat='bonus_init',
                           _status_effect_name='Hasted', _status_effect_turns=2)], [], [], _targets_enemies=False),
    'summon_coal_golem': Spell('Summon Coal Golem', 'Summon Coal Golem description.', 1, {'h': 0, 's': 0, 'm': 8}, [],
                               [], [], _targets_enemies=False, _summon=['coal_golem']),
}
