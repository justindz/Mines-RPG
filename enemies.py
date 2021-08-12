from elements import Elements
from enemy import Enemy, Goal, GoalType
from ability import EffectType
from spell import SpellEffect
from ai.single_target_attack import SingleTargetAttack
from ai.single_target_heal import SingleTargetHeal
from ai.status_effect import StatusEffect
from ai.summon import Summon
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
                       SingleTargetAttack('Headbutt', 0, 0.05, [SpellEffect(EffectType.damage_health, Elements.earth, 1, 4)]),
                       SingleTargetHeal('Regenerate', 3, [SpellEffect(EffectType.restore_health, Elements.water, 2, 5)]),
                       StatusEffect('Slime', 3, [SpellEffect(EffectType.debuff, Elements.water, -10, _stat='bonus_strength',
                                                 _status_effect_name='Soaked', _status_effect_turns=2)], debuff=True),
                       StatusEffect('Symbiosis', 4, [SpellEffect(EffectType.buff, Elements.water, 10,
                                                     _stat='bonus_strength', _status_effect_name='Reinforced',
                                                                 _status_effect_turns=3)])
                   ],
                   [Goal(GoalType.damage_player, 500),
                    Goal(GoalType.heal_ally, 450),
                    Goal(GoalType.debuff_player, 425),
                    Goal(GoalType.buff_ally, 450)]),

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
                     SingleTargetAttack('Claw', 0, 0.05, [SpellEffect(EffectType.damage_health, Elements.earth, 2, 4)]),
                     Summon('Loogie', 99, ['slime'], 'The imp hocks up a disgusting, sentient wad of spit.')
                 ],
                 [Goal(GoalType.damage_player, 500)]),

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
                   Goal(GoalType.damage_player, 400)]),
}
