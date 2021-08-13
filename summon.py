from enemy import Enemy, GoalType, Plan
from ability import EffectType


class Summon(Enemy):
    def __init__(self, name, strength, strength_growth, intelligence, intelligence_growth, dexterity,
                 dexterity_growth,
                 willpower, willpower_growth, health, health_growth, health_regen, health_regen_growth,
                 init, init_growth, earth_res, earth_res_growth, fire_res, fire_res_growth,
                 electricity_res, electricity_res_growth, water_res, water_res_growth, actions, goals, cost, ele_pens):
        super().__init__(name, strength, strength_growth, intelligence, intelligence_growth, dexterity,
                         dexterity_growth,
                         willpower, willpower_growth, health, health_growth, health_regen, health_regen_growth,
                         init, init_growth, earth_res, earth_res_growth, fire_res, fire_res_growth,
                         electricity_res, electricity_res_growth, water_res, water_res_growth, actions, goals)
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
                effects = list(filter(lambda effect: effect.type == EffectType.damage_health, action.effects))

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
                effects = list(filter(lambda effect: effect.type in [EffectType.damage_health, EffectType.debuff,
                                                                     EffectType.buff, EffectType.restore_health,
                                                                     EffectType.summon], action.effects))

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
