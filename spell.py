from elements import Elements
import ability
from ability import EffectType, Effect


class Spell(ability.Ability):
    def __init__(self, _name, _description, _cost, _effects, _activates, _consumes, _area=0, _area_modifiable=False,
                 _base_crit_chance=0.05, _targets_enemies=True, _summon=None):
        super().__init__(_name, _description, _cost, _effects, _activates, _consumes, _area, _area_modifiable)

        if _summon is None:
            _summon = []

        self.base_crit_chance = _base_crit_chance
        self.targets_enemies = _targets_enemies
        self.summon = _summon


spells = {
    # Damage
    'stalagmite': Spell('Stalagmite', 'Stalagmite description.', {'h': 0, 's': 0, 'm': 5},
                        [Effect(EffectType.damage_health, Elements.earth, _dice_value=4)], [], [Elements.earth],
                        _targets_enemies=True),
    # Healing
    'regenerate': Spell('Regenerate', 'Regenerate description.', {'h': 0, 's': 0, 'm': 10},
                        [Effect(EffectType.buff, Elements.water, _status_effect_value=2, _stat='health_regen',
                                _status_effect_name='Mending', _status_effect_turns=4)], [], [], _base_crit_chance=0.01,
                        _targets_enemies=False),
    'mend_wounds': Spell('Mend Wounds', 'Mend Wounds description.', {'h': 0, 's': 0, 'm': 5},
                         [Effect(EffectType.restore_health, Elements.water, _dice_value=6),
                          Effect(EffectType.restore_stamina, Elements.water, _dice_value=6)], [], [],
                         _base_crit_chance=0.01, _targets_enemies=False),
    # Debuffs
    'slow': Spell('Slow', 'Slow description.', {'h': 0, 's': 0, 'm': 8},
                  [Effect(EffectType.debuff, Elements.electricity, _status_effect_value=-5, _stat='bonus_init',
                          _status_effect_name='Slowed', _status_effect_turns=2)], [], []),
    'haste': Spell('Haste', 'Haste description.', {'h': 0, 's': 0, 'm': 8},
                   [Effect(EffectType.buff, Elements.electricity, _status_effect_value=5, _stat='bonus_init',
                           _status_effect_name='Hasted', _status_effect_turns=2)], [], [], _targets_enemies=False),
    'weaken': Spell('Weaken', 'Weaken description.', {'h': 0, 's': 0, 'm': 8},
                    [Effect(EffectType.debuff, Elements.earth, _status_effect_value=-5, _stat='strength',
                            _status_effect_name='Weakened', _status_effect_turns=3)], [Elements.earth], []),
    'stupefy': Spell('Stupefy', 'Stupefy description.', {'h': 0, 's': 0, 'm': 8},
                     [Effect(EffectType.debuff, Elements.fire, _status_effect_value=-5, _stat='intelligence',
                             _status_effect_name='Stupefied', _status_effect_turns=3)], [Elements.fire], []),
    'exhaust': Spell('Exhaust', 'Exhaust description.', {'h': 0, 's': 0, 'm': 8},
                     [Effect(EffectType.debuff, Elements.electricity, _status_effect_value=-5, _stat='dexterity',
                             _status_effect_name='Exhausted', _status_effect_turns=3)], [Elements.electricity], []),
    'discourage': Spell('Discourage', 'Discourage description.', {'h': 0, 's': 0, 'm': 8},
                        [Effect(EffectType.debuff, Elements.water, _status_effect_value=-5, _stat='willpower',
                                _status_effect_name='Discouraged', _status_effect_turns=3)], [Elements.water], []),
    # Summons
    'summon_coal_golem': Spell('Summon Coal Golem', 'Summon Coal Golem description.', {'h': 0, 's': 0, 'm': 8}, [], [],
                               [], _targets_enemies=False, _summon=['coal_golem']),
    # Combo Spells
}
