from enemy import Enemy, GoalType, Plan
from ability import EffectType


class Summon(Enemy):
    def __init__(self, name, cost, actions, goals, strength=0, strength_growth=5, intelligence=0, intelligence_growth=5,
                 dexterity=0, dexterity_growth=5, willpower=0, willpower_growth=5, health=10, health_growth=10,
                 health_regen=0, health_regen_growth=0, init=0, init_growth=2, earth_res=0.0, earth_res_growth=0.02,
                 fire_res=0, fire_res_growth=0.02, electricity_res=0.0, electricity_res_growth=0.02, water_res=0.0,
                 water_res_growth=0.02, dot_res=0.0, dot_res_growth=0.02, dot_reduction=0, dot_effect=0.0,
                 dot_effect_growth=0.02, dot_duration=0, shock_limit=4, shock_limit_growth=0.2, confusion_limit=4,
                 confusion_limit_growth=0.2, ele_pens=(0.0, 0.0, 0.0, 0.0)):
        super().__init__(name, actions, goals, strength, strength_growth, intelligence, intelligence_growth, dexterity,
                         dexterity_growth, willpower, willpower_growth, health, health_growth, health_regen,
                         health_regen_growth, init, init_growth, earth_res, earth_res_growth, fire_res, fire_res_growth,
                         electricity_res, electricity_res_growth, water_res, water_res_growth, dot_res, dot_res_growth,
                         dot_reduction, dot_effect, dot_effect_growth, dot_duration, shock_limit, shock_limit_growth,
                         confusion_limit, confusion_limit_growth)
        self.cost = cost
        self.owner = ''
        self.bonus_health = 0  # used in planners by enemies who may target the summon like a player
        self.ele_pens = ele_pens

    def get_action_plans(self, fight):
        plans = []

        # damage_enemy goal
        goal = [x for x in self.goals if x.goal_type == GoalType.damage_opponent]

        if len(goal) > 0:
            plans += self.get_damage_enemy_plans(goal[0], fight)

        # debuff_player goal
        goal = [x for x in self.goals if x.goal_type == GoalType.debuff_opponent]

        if len(goal) > 0:
            plans += self.get_debuff_enemy_plans(goal[0], fight)

        # heal_ally goal
        goal = [x for x in self.goals if x.goal_type == GoalType.heal_ally]

        if len(goal) > 0:
            plans += self.get_heal_ally_plans(goal[0], fight)

        # buff_ally goal
        goal = [x for x in self.goals if x.goal_type == GoalType.buff_ally]

        if len(goal) > 0:
            plans += self.get_buff_ally_plans(goal[0], fight)

        # summon goal
        goal = [x for x in self.goals if x.goal_type == GoalType.summon]

        if len(goal) > 0:
            plans += self.get_summon_plans(goal[0], fight)

        # enrage goal
        goal = [x for x in self.goals if x.goal_type == GoalType.enrage]

        if len(goal) > 0:
            plans += self.get_enrage_plans(goal[0], fight)

        return plans

    def get_damage_enemy_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_opponents and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type in [EffectType.damage_health, EffectType.burn,
                                                                     EffectType.bleed], action.effects))

                if len(effects) > 0:
                    for enemy in fight.enemies:
                        dmg = enemy.estimate_damage_from_enemy_action(self, action)
                        plan = Plan()
                        plan.score = goal.value + 100 - int(max(enemy.current_health - dmg, 1) / enemy.current_health * 100)
                        plan.action = lambda action=action, enemy=enemy: action.do(self, enemy, fight)
                        plan.debug = f'damage {enemy.name} w/ {action.name} score {plan.score}'
                        plans.append(plan)

        return plans

    def get_debuff_enemy_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_opponents and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.debuff, action.effects))

                if len(effects) > 0:
                    for enemy in fight.enemies:
                        plan = Plan()
                        plan.score = goal.value + 100 - (25 * len(enemy.status_effects))
                        plan.action = lambda action=action, enemy=enemy: action.do(self, enemy, fight)
                        plan.debug = f'debuff {enemy.name} w/ {action.name} score {plan.score}'
                        plans.append(plan)

        return plans

    def get_heal_ally_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_allies and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.restore_health, action.effects))

                if len(effects) > 0:
                    for character in [x for x in fight.characters if not isinstance(x, Summon)]:
                        plan = Plan()
                        plan.score = goal.value + 100 - int(character.current_health / character.health * 100)
                        plan.action = lambda action=action, character=character: action.do(self, character, fight)
                        plan.debug = f'heal {character.name} w/ {action.name} score {plan.score}'
                        plans.append(plan)

        return plans

    def get_buff_ally_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_allies and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.buff, action.effects))

                if len(effects) > 0:
                    for character in [x for x in fight.characters if not isinstance(x, Summon)]:
                        plan = Plan()
                        plan.score = goal.value + (25 * len(character.status_effects))
                        plan.action = lambda action=action, character=character: action.do(self, character, fight)
                        plan.debug = f'buff {character.name} w/ {action.name} score {plan.score}'
                        plans.append(plan)

        return plans

    def get_summon_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.summon, action.effects))

                if len(effects) > 0:
                    plan = Plan()
                    plan.score = goal.value
                    plan.action = lambda action=action: action.do(self, None, fight)
                    plan.debug = f'summon {action.name} w/ score {plan.score}'
                    plans.append(plan)

        return plans

    def get_enrage_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.is_usable(fight.states) and not action.targets_opponents and not action.targets_allies:
                effects = list(filter(lambda effect: effect.type in [EffectType.damage_health, EffectType.burn,
                                                                     EffectType.debuff, EffectType.buff,
                                                                     EffectType.restore_health, EffectType.summon],
                                      action.effects))

                if len(effects) > 0:
                    plan = Plan()

                    if self.current_health / self.health <= 0.2:
                        plan.score = 9999999
                    else:
                        plan.score = 0

                    plan.action = lambda action=action: action.do(self, fight.enemies[0], fight)
                    plan.debug = f'enrage {action.name} w/ score {plan.score}'
                    plans.append(plan)

        return plans
