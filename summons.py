from elements import Elements
from enemy import Goal, GoalType
from ability import EffectType, Effect
from ai.single_target_attack import SingleTargetAttack
from ai.single_target_heal import SingleTargetHeal
from ai.status_effect import StatusEffect
from summon import Summon
from ai.explode import Explode

summons = {
    'coal_golem':
        Summon('Coal Golem',
               {'h': 0, 's': 0, 'm': 8},
               [
                   SingleTargetAttack('Punch', 0, 0.05, [Effect(EffectType.damage_health, Elements.earth, _dice_value=4)]),
                   SingleTargetAttack('Slam', 3, 0.05, [Effect(EffectType.damage_health, Elements.earth, _dice_value=8)])
               ],
               [Goal(GoalType.damage_opponent, 400)],
               strength_growth=7,
               earth_res=0.1),

    'blood_golem':
        Summon('Blood Golem',
               {'h': 5, 's': 0, 'm': 0},
               [
                   SingleTargetAttack('Exsanguinate', 0, 0.05, [Effect(EffectType.bleed, Elements.earth, _effect_turns=1, _dot_value=2)]),
                   Explode('Blood Geyser', [Effect(EffectType.restore_health, Elements.water, _dice_value=4)])
               ],
               [
                   Goal(GoalType.enrage, 0),
                   Goal(GoalType.damage_opponent, 400)
               ],
               water_res=0.1,
               electricity_res_growth=0.01,
               dot_res=0.05,
               dot_res_growth=0.03,
               health_regen=1,
               health_regen_growth=1,
               shock_limit=3,
               confusion_limit=5),

    'wisp':
        Summon('Will-o-the-Wisp',
               {'h': 0, 's': 0, 'm': 5},
               [
                   StatusEffect('Misdirection', 3, [
                      Effect(EffectType.debuff, Elements.earth, _stat='bonus_strength', _dice_value=4, _effect_turns=2, _status_effect_name='Weakened'),
                      Effect(EffectType.debuff, Elements.fire, _stat='bonus_fire', _dice_value=4, _effect_turns=2, _status_effect_name='Stupefied'),
                      Effect(EffectType.debuff, Elements.electricity, _stat='bonus_dexterity', _dice_value=4, _effect_turns=2, _status_effect_name='Exhausted'),
                      Effect(EffectType.debuff, Elements.water, _stat='bonus_willpower', _dice_value=4, _effect_turns=2, _status_effect_name='Discouraged'),
                   ]),
                   SingleTargetAttack('Foolish Fire', 0, 0.08, [Effect(EffectType.damage_health, Elements.fire, _dice_value=2)]),
               ],
               [
                   Goal(GoalType.debuff_opponent, 450),
                   Goal(GoalType.damage_opponent, 400)
               ],
               health=7,
               health_growth=4),
}
