from elements import Elements
from enemy import Enemy, Goal, GoalType
from ability import EffectType
from spell import SpellEffect
from ai.single_target_attack import SingleTargetAttack
from ai.single_target_heal import SingleTargetHeal
from ai.status_effect import StatusEffect
from ai.summon_action import SummonAction
from ai.explode import Explode

enemies = {
    'slime': Enemy('Slime',
                   # Stats
                   1, 0.3,
                   1, 0.3,
                   1, 0.3,
                   1, 0.3,
                   # Health
                   10, 0.1,
                   0, 0,
                   # Init
                   4, 0.2,
                   # Res
                   0.0, 0.0,
                   0.0, 0.0,
                   0.0, 0.0,
                   0.0, 0.0,
                   [
                       SingleTargetAttack('Headbutt', 0, 0.05,
                                          [SpellEffect(EffectType.damage_health, Elements.earth, 1, 4)]),
                       SingleTargetHeal('Regenerate', 3,
                                        [SpellEffect(EffectType.restore_health, Elements.water, 2, 5)]),
                       StatusEffect('Symbiosis', 4, [SpellEffect(EffectType.buff, Elements.water, 10,
                                                                 _stat='bonus_strength',
                                                                 _status_effect_name='Reinforced',
                                                                 _status_effect_turns=3)])
                   ],
                   [Goal(GoalType.damage_opponent, 500),
                    Goal(GoalType.heal_ally, 450),
                    Goal(GoalType.buff_ally, 450)]),

    'spider': Enemy('Spider',
                    # Stats
                    1, 0.3,
                    1, 0.3,
                    1, 0.3,
                    1, 0.3,
                    # Health
                    8, 0.1,
                    0, 0,
                    # Init
                    3, 0.2,
                    # Res
                    0.0, 0.0,
                    0.0, 0.0,
                    0.0, 0.0,
                    0.0, 0.0,
                    [
                        SingleTargetAttack('Bite', 0, 0.06,
                                           [SpellEffect(EffectType.damage_health, Elements.earth, 2, 4)]),
                        StatusEffect('Web', 3,
                                     [SpellEffect(EffectType.debuff, Elements.earth, -5, _stat='bonus_init',
                                                  _status_effect_name='Slowed', _status_effect_turns=2)], debuff=True),
                    ],
                    [Goal(GoalType.damage_opponent, 500),
                     Goal(GoalType.debuff_opponent, 425)]),

    'scarab': Enemy('Scarab',
                    # Stats
                    2, 0.3,
                    1, 0.3,
                    1, 0.3,
                    1, 0.3,
                    # Health
                    7, 0.1,
                    0, 0,
                    # Init
                    4, 0.2,
                    # Res
                    0.1, 0.0,
                    0.1, 0.0,
                    0.1, 0.0,
                    0.1, 0.0,
                    [
                        SingleTargetAttack('Bite', 0, 0.05,
                                           [SpellEffect(EffectType.damage_health, Elements.earth, 1, 6)]),
                        SummonAction('Screech', 10, ['summoned_scarab'], 'The scarab cries for backup.'),
                    ],
                    [Goal(GoalType.summon, 500),
                     Goal(GoalType.damage_opponent, 400)]),

    'summoned_scarab': Enemy('Scarab',
                             # Stats
                             2, 0.3,
                             1, 0.3,
                             1, 0.3,
                             1, 0.3,
                             # Health
                             7, 0.1,
                             0, 0,
                             # Init
                             4, 0.2,
                             # Res
                             0.1, 0.0,
                             0.1, 0.0,
                             0.1, 0.0,
                             0.1, 0.0,
                             [SingleTargetAttack('Bite', 0, 0.05,
                                                 [SpellEffect(EffectType.damage_health, Elements.earth, 1, 6)])],
                             [Goal(GoalType.damage_opponent, 400)]),

    'imp': Enemy('Imp',
                 # Stats
                 1, 0.3,
                 2, 0.4,
                 1, 0.3,
                 1, 0.3,
                 # Health
                 10, 0.1,
                 1, 1,
                 # Init
                 5, 0.2,
                 # Res
                 0.03, 0.01,
                 0.08, 0.03,
                 0.03, 0.01,
                 0.0, 0.01,
                 [
                     SingleTargetAttack('Claw', 0, 0.05, [SpellEffect(EffectType.damage_health, Elements.earth, 3, 6)]),
                 ],
                 [Goal(GoalType.damage_opponent, 500)]),

    'bomb': Enemy('Bomb',
                  # Stats
                  1, 0.3,
                  3, 0.3,
                  1, 0.3,
                  1, 0.3,
                  # Health
                  20, 0.1,
                  0, 0.0,
                  # Init
                  10, 0.3,
                  # Res
                  0.03, 0.01,
                  0.05, 0.03,
                  0.03, 0.01,
                  0.0, 0.01,
                  [
                      SingleTargetAttack('Bite', 0, 0.06, [SpellEffect(EffectType.damage_health, Elements.fire, 2, 4)]),
                      Explode('Explode', [SpellEffect(EffectType.damage_health, Elements.fire, 5, 10)])
                  ],
                  [Goal(GoalType.enrage, 0),
                   Goal(GoalType.damage_opponent, 400)]),
}
