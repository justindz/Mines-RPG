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
    'stalagmite': Spell(
        'Stalagmite',
        'Stalagmite description.',
        {'h': 0, 's': 0, 'm': 5},
        [Effect(EffectType.damage_health, Elements.earth, _dice_value=8)],
        [],
        [Elements.earth],
        _targets_enemies=True
    ),
    'ignite': Spell(
        'Ignite',
        'Ignite description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.damage_health, Elements.fire, _dice_value=2),
            Effect(EffectType.burn, Elements.fire, _dot_value=2, _effect_turns=2)
        ],
        [],
        [Elements.fire],
        _targets_enemies=True
    ),
    'spark': Spell(
        'Spark',
        'Spark description.',
        {'h': 0, 's': 0, 'm': 6},
        [Effect(EffectType.damage_health, Elements.electricity, _dice_value=6)],
        [Elements.electricity],
        [],
        _targets_enemies=True
    ),
    'wave': Spell(
        'Wave',
        'Wave description.',
        {'h': 0, 's': 0, 'm': 7},
        [Effect(EffectType.damage_health, Elements.earth, _dice_value=6)],
        [Elements.water],
        [],
        _targets_enemies=True
    ),
    # Healing
    'regenerate': Spell(
        'Regenerate',
        'Regenerate description.',
        {'h': 0, 's': 0, 'm': 10},
        [
            Effect(EffectType.buff, Elements.water, _dice_value=2, _stat='health_regen', _status_effect_name='Mending',
                   _effect_turns=4)
        ],
        [],
        [],
        _base_crit_chance=0.01,
        _targets_enemies=False
    ),
    'mend_wounds': Spell(
        'Mend Wounds',
        'Mend Wounds description.',
        {'h': 0, 's': 0, 'm': 5},
        [
            Effect(EffectType.restore_health, Elements.water, _dice_value=6),
            Effect(EffectType.restore_stamina, Elements.water, _dice_value=6)
        ],
        [],
        [],
        _base_crit_chance=0.01,
        _targets_enemies=False
    ),
    # Debuffs
    'slow': Spell(
        'Slow',
        'Slow description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.debuff, Elements.electricity, _dice_value=5, _stat='bonus_init',
                   _status_effect_name='Slowed', _effect_turns=2)
        ],
        [],
        []
    ),
    'weaken': Spell(
        'Weaken',
        'Weaken description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.debuff, Elements.earth, _dice_value=10, _stat='strength', _status_effect_name='Weakened',
                   _effect_turns=3)
        ],
        [Elements.earth],
        []
    ),
    'stupefy': Spell(
        'Stupefy',
        'Stupefy description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.debuff, Elements.fire, _dice_value=10, _stat='intelligence',
                   _status_effect_name='Stupefied', _effect_turns=3)
        ],
        [Elements.fire],
        []
    ),
    'exhaust': Spell(
        'Exhaust',
        'Exhaust description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.debuff, Elements.electricity, _dice_value=10, _stat='dexterity',
                   _status_effect_name='Exhausted', _effect_turns=3)
        ],
        [Elements.electricity],
        []
    ),
    'discourage': Spell(
        'Discourage',
        'Discourage description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.debuff, Elements.water, _dice_value=10, _stat='willpower',
                   _status_effect_name='Discouraged', _effect_turns=3)
        ],
        [Elements.water],
        []
    ),
    # Buffs
    'haste': Spell(
        'Haste',
        'Haste description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.electricity, _dice_value=10, _stat='bonus_init',
                   _status_effect_name='Hasted', _effect_turns=2)
        ],
        [],
        [],
        _targets_enemies=False
    ),
    'empower': Spell(
        'Empower',
        'Empower description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.earth, _dice_value=10, _stat='strength', _status_effect_name='Empowered',
                   _effect_turns=3)
        ],
        [Elements.earth],
        []
    ),
    'enlighten': Spell(
        'Enlighten',
        'Enlighten description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.fire, _dice_value=10, _stat='intelligence',
                   _status_effect_name='Enlightened', _effect_turns=3)
        ],
        [Elements.fire],
        []
    ),
    'unleash': Spell(
        'Unleash',
        'Unleash description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.electricity, _dice_value=10, _stat='dexterity',
                   _status_effect_name='Unleashed', _effect_turns=3)
        ],
        [Elements.electricity],
        []
    ),
    'inspire': Spell(
        'Inspire',
        'Inspire description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.water, _dice_value=10, _stat='willpower', _status_effect_name='Inspired',
                   _effect_turns=3)
        ],
        [Elements.water],
        []
    ),
    'focused_empower': Spell(
        'Focused Empower',
        'Focused Empower description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.earth, _dice_value=30, _stat='strength', _status_effect_name='Empowered',
                   _effect_turns=2)
        ],
        [Elements.earth],
        []
    ),
    'focused_enlighten': Spell(
        'Focused Enlighten',
        'Focused Enlighten description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.fire, _dice_value=30, _stat='intelligence',
                   _status_effect_name='Enlightened', _effect_turns=2)
        ],
        [Elements.fire],
        []
    ),
    'focused_unleash': Spell(
        'Focused Unleash',
        'Focused Unleash description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.electricity, _dice_value=30, _stat='dexterity',
                   _status_effect_name='Unleashed', _effect_turns=2)
        ],
        [Elements.electricity],
        []
    ),
    'focused_inspire': Spell(
        'Focused Inspire',
        'Focused Inspire description.',
        {'h': 0, 's': 0, 'm': 8},
        [
            Effect(EffectType.buff, Elements.water, _dice_value=30, _stat='willpower', _status_effect_name='Inspired',
                   _effect_turns=2)
        ],
        [Elements.water],
        []
    ),
    # Summons
    'summon_coal_golem': Spell(
        'Summon Coal Golem',
        'Summon Coal Golem description.',
        {'h': 0, 's': 0, 'm': 8},
        [],
        [],
        [],
        _targets_enemies=False,
        _summon=['coal_golem']
    ),
    # Combo Spells
}
