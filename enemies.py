from elements import Elements
from enemy import Enemy, Goal, GoalType
from ability import EffectType, Effect
from ai.single_target_attack import SingleTargetAttack
from ai.single_target_heal import SingleTargetHeal
from ai.status_effect import StatusEffect
from ai.summon_action import SummonAction
from ai.explode import Explode

enemies = {
    'slime': Enemy('Slime',
                   # Stats
                   1, 3,
                   1, 3,
                   1, 3,
                   1, 3,
                   # Health
                   10, 3,
                   0, 0,
                   # Init
                   4, 2,
                   # Res
                   0.0, 0.02,
                   0.0, 0.02,
                   0.0, 0.02,
                   0.0, 0.02,
                   0.0, 0.02,
                   0,
                   0.0, 0.02,
                   0,
                   [
                       SingleTargetAttack('Headbutt', 0, 0.05,
                                          [Effect(EffectType.damage_health, Elements.earth, _dice_value=4)]),
                       SingleTargetHeal('Regenerate', 3,
                                        [Effect(EffectType.restore_health, Elements.water, _dice_value=10)]),
                       StatusEffect('Symbiosis', 4, [
                           Effect(EffectType.buff, Elements.water, _status_effect_value=10, _stat='bonus_strength',
                                  _status_effect_name='Reinforced', _status_effect_turns=3)])
                   ],
                   [Goal(GoalType.damage_opponent, 500),
                    Goal(GoalType.heal_ally, 450),
                    Goal(GoalType.buff_ally, 450)]),

    'spider': Enemy('Spider',
                    # Stats
                    1, 3,
                    1, 3,
                    1, 3,
                    1, 3,
                    # Health
                    8, 2,
                    0, 0,
                    # Init
                    3, 2,
                    # Res
                    0.0, 0.02,
                    0.0, 0.02,
                    0.0, 0.02,
                    0.0, 0.02,
                    0.0, 0.02,
                    0,
                    0.0, 0.02,
                    0,
                    [
                        SingleTargetAttack('Bite', 0, 0.06,
                                           [Effect(EffectType.damage_health, Elements.earth, _dice_value=4)]),
                        StatusEffect('Web', 3,
                                     [Effect(EffectType.debuff, Elements.earth, _status_effect_value=-5,
                                             _stat='bonus_init', _status_effect_name='Slowed',
                                             _status_effect_turns=2)], debuff=True),
                    ],
                    [Goal(GoalType.damage_opponent, 500),
                     Goal(GoalType.debuff_opponent, 425)]),

    'scarab': Enemy('Scarab',
                    # Stats
                    2, 3,
                    1, 3,
                    1, 3,
                    1, 3,
                    # Health
                    7, 2,
                    0, 0,
                    # Init
                    4, 3,
                    # Res
                    0.1, 0.02,
                    0.1, 0.02,
                    0.1, 0.02,
                    0.1, 0.02,
                    0.1, 0.02,
                    0,
                    0.0, 0.02,
                    0,
                    [
                        SingleTargetAttack('Bite', 0, 0.05,
                                           [Effect(EffectType.damage_health, Elements.earth, _dice_value=6)]),
                        SummonAction('Screech', 10, ['summoned_scarab'], 'The scarab cries for backup.'),
                    ],
                    [Goal(GoalType.summon, 500),
                     Goal(GoalType.damage_opponent, 400)]),

    'summoned_scarab': Enemy('Scarab',
                             # Stats
                             2, 3,
                             1, 3,
                             1, 3,
                             1, 3,
                             # Health
                             7, 2,
                             0, 0,
                             # Init
                             4, 3,
                             # Res
                             0.1, 0.02,
                             0.1, 0.02,
                             0.1, 0.02,
                             0.1, 0.02,
                             0.1, 0.02,
                             0,
                             0.0, 0.02,
                             0,
                             [SingleTargetAttack('Bite', 0, 0.05,
                                                 [Effect(EffectType.damage_health, Elements.earth, _dice_value=6)])],
                             [Goal(GoalType.damage_opponent, 400)]),

    'imp': Enemy('Imp',
                 # Stats
                 1, 3,
                 2, 4,
                 1, 3,
                 1, 2,
                 # Health
                 10, 3,
                 1, 0.5,
                 # Init
                 5, 2,
                 # Res
                 0.03, 0.02,
                 0.08, 0.03,
                 0.03, 0.02,
                 0.0, 0.01,
                 0.3, 0.02,
                 0,
                 0.3, 0.02,
                 0,
                 [
                     SingleTargetAttack('Mischevious Flame', 0, 0.05, [Effect(EffectType.damage_health, Elements.fire,
                                                                              _dice_value=3),
                                                                       Effect(EffectType.burn, Elements.fire,
                                                                              _status_effect_turns=2,
                                                                              _status_effect_value=2)]),
                 ],
                 [Goal(GoalType.damage_opponent, 500)]),

    'bomb': Enemy('Bomb',
                  # Stats
                  1, 3,
                  3, 3,
                  1, 3,
                  1, 3,
                  # Health
                  20, 2,
                  0, 0,
                  # Init
                  10, 3,
                  # Res
                  0.03, 0.01,
                  0.05, 0.03,
                  0.03, 0.01,
                  0.0, 0.01,
                  0.3, 0.02,
                  0,
                  0.0, 0.02,
                  0,
                  [
                      SingleTargetAttack('Bite', 0, 0.06, [Effect(EffectType.damage_health, Elements.fire,
                                                                  _dice_value=8)]),
                      Explode('Explode', [Effect(EffectType.damage_health, Elements.fire, _dice_value=10)])
                  ],
                  [Goal(GoalType.enrage, 0),
                   Goal(GoalType.damage_opponent, 400)]),
}
