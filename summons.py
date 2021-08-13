from elements import Elements
from enemy import Goal, GoalType
from ability import EffectType
from spell import SpellEffect
from ai.single_target_attack import SingleTargetAttack
from ai.single_target_heal import SingleTargetHeal
from ai.status_effect import StatusEffect
from summon import Summon
from ai.explode import Explode

summons = {
    'coal_golem': Summon('Coal Golem',
                         # Stats
                         2, 0.3,
                         1, 0.3,
                         1, 0.3,
                         1, 0.3,
                         # Health
                         5, 0.1,
                         1, 1,
                         # Init
                         0, 0.0,
                         # Res
                         0.1, 0.01,
                         0.0, 0.0,
                         0.1, 0.01,
                         0.0, 0.0,
                         [SingleTargetAttack('Punch', 0, 0.05,
                                             [SpellEffect(EffectType.damage_health, Elements.earth, 1, 3)]),
                          SingleTargetAttack('Slam', 3, 0.05,
                                             [SpellEffect(EffectType.damage_health, Elements.earth, 3, 5)])],
                         [Goal(GoalType.damage_opponent, 400)],
                         {'h': 0, 's': 0, 'm': 8}),
}
