from elements import Elements
from enemy import Enemy, Goal, GoalType
from ability import EffectType, Effect
from ai.single_target_attack import SingleTargetAttack
from ai.single_target_heal import SingleTargetHeal
from ai.status_effect import StatusEffect
from ai.summon_action import SummonAction
from ai.explode import Explode

enemies = {
    'slime': Enemy('Slime', [
        SingleTargetAttack('Headbutt', 0, 0.05,
                           [Effect(EffectType.damage_health, Elements.earth, _dice_value=4)]),
        SingleTargetHeal('Regenerate', 3,
                         [Effect(EffectType.restore_health, Elements.water, _dice_value=10)]),
        StatusEffect('Symbiosis', 4, [
            Effect(EffectType.buff, Elements.water, _dice_value=10, _stat='bonus_strength',
                   _status_effect_name='Reinforced', _effect_turns=3)])
    ], [Goal(GoalType.damage_opponent, 500),
        Goal(GoalType.heal_ally, 450),
        Goal(GoalType.buff_ally, 450)], init=0),

    'spider': Enemy('Spider', [
        SingleTargetAttack('Bite', 0, 0.06,
                           [Effect(EffectType.damage_health, Elements.earth, _dice_value=4)]),
        StatusEffect('Web', 3,
                     [Effect(EffectType.debuff, Elements.earth, _dice_value=10,
                             _stat='bonus_init', _status_effect_name='Slowed',
                             _effect_turns=2)], debuff=True),
    ], [Goal(GoalType.damage_opponent, 500),
        Goal(GoalType.debuff_opponent, 425)], init=2, init_growth=4),

    'scarab': Enemy('Scarab', [
        SingleTargetAttack('Bite', 0, 0.05,
                           [Effect(EffectType.damage_health, Elements.earth, _dice_value=6)]),
        SummonAction('Screech', 10, ['summoned_scarab'], 'The scarab cries for backup.'),
    ], [Goal(GoalType.summon, 500),
        Goal(GoalType.damage_opponent, 400)], health=7),

    'summoned_scarab': Enemy('Scarab', [SingleTargetAttack('Bite', 0, 0.05,
                                                           [Effect(EffectType.damage_health, Elements.earth,
                                                                   _dice_value=6)])],
                             [Goal(GoalType.damage_opponent, 400)], health=7),

    'imp': Enemy('Imp', [
        SingleTargetAttack('Mischevious Flame', 0, 0.05, [Effect(EffectType.damage_health, Elements.fire,
                                                                 _dice_value=3),
                                                          Effect(EffectType.burn, Elements.fire,
                                                                 _effect_turns=2,
                                                                 _dot_value=2)]),
    ], [Goal(GoalType.damage_opponent, 500)], fire_res=0.1, fire_res_growth=0.03),

    'bomb': Enemy('Bomb', [
        SingleTargetAttack('Bite', 0, 0.06, [Effect(EffectType.damage_health, Elements.fire,
                                                    _dice_value=8)]),
        Explode('Explode', [Effect(EffectType.damage_health, Elements.fire, _dice_value=10)])
    ], [Goal(GoalType.enrage, 0),
        Goal(GoalType.damage_opponent, 400)], health_growth=15, water_res_growth=0.01),
}
