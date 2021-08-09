from elements import Elements
from enemy import Enemy, Goal, GoalType
from ability import EffectType
from spell import SpellEffect
from ai.single_target_attack import SingleTargetAttack
from ai.single_target_heal import SingleTargetHeal
from ai.status_effect import StatusEffect

enemies = {
    'slime': Enemy('Slime', 1, 0.3, 1, 0.3, 1, 0.3, 1, 0.3, 10, 0.1, 4, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   [SingleTargetAttack('Headbutt', 0, 0.05,
                                       [SpellEffect(EffectType.damage_health, Elements.earth, 1, 4)]),
                    SingleTargetHeal('Regenerate', 3,
                                     [SpellEffect(EffectType.restore_health, Elements.water, 2, 5)]),
                    StatusEffect('Slime', 3,
                                 [SpellEffect(EffectType.debuff, Elements.water, -10, _stat='bonus_strength',
                                              _status_effect_name='Soaked', _status_effect_turns=2)], debuff=True),
                    StatusEffect('Symbiosis', 4,
                                 [SpellEffect(EffectType.buff, Elements.water, 10, _stat='bonus_strength',
                                              _status_effect_name='Reinforced', _status_effect_turns=3)]),
                    ],
                   [Goal(GoalType.damage_player, 500), Goal(GoalType.heal_ally, 450), Goal(GoalType.debuff_player, 425),
                    Goal(GoalType.buff_ally, 450)]),

    'imp': Enemy('Imp', 1, 0.3, 2, 0.4, 1, 0.3, 1, 0.3, 10, 0.1, 5, 0.2, 0.03, 0.01, 0.08, 0.03, 0.03, 0.01, 0.0, 0.01,
                 [SingleTargetAttack('Claw', 0, 0.05,
                                     [SpellEffect(EffectType.damage_health, Elements.earth, 2, 4)])],
                 [Goal(GoalType.damage_player, 500)]),
}
