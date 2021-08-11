from elements import Elements
from ability import EffectType
import utilities

import random
from enum import Enum


class GoalType(Enum):
    damage_player = 1
    debuff_player = 2
    heal_ally = 3
    buff_ally = 4
    summon = 5  # intended for use basically whenever off cooldown
    enrage = 6  # goal value weighted by % current health threshold


class Goal:
    def __init__(self, goal_type: GoalType, value: int):
        self.goal_type = goal_type
        self.value = value

    @staticmethod
    def get_contributor_effects_by_goal_type(goal_type: GoalType):
        if goal_type == GoalType.damage_player:
            contribs = [EffectType.damage_health]
        elif goal_type == GoalType.debuff_player:
            contribs = [EffectType.debuff]
        elif goal_type == GoalType.heal_ally:
            contribs = [EffectType.restore_health]
        elif goal_type == GoalType.buff_ally:
            contribs = [EffectType.buff]
        elif goal_type == GoalType.summon:
            contribs = [EffectType.summon]
        elif goal_type == GoalType.enrage:
            contribs = [EffectType.damage_health, EffectType.debuff, EffectType.buff, EffectType.restore_health,
                        EffectType.summon]
        else:
            raise Exception(f'GoalType {goal_type} has no configured contributing effects')

        return contribs


class Plan:
    def __init__(self):
        self.action = None
        self.debug = ''
        self.score = 0


class Enemy:
    def __init__(self, name, strength, strength_growth, intelligence, intelligence_growth, dexterity, dexterity_growth,
                 willpower, willpower_growth, health, health_growth, health_regen, health_regen_growth,
                 init, init_growth, earth_res, earth_res_growth, fire_res, fire_res_growth,
                 electricity_res, electricity_res_growth, water_res, water_res_growth, actions, goals):
        self.name = name
        self.level = 1

        # Stats
        self.strength = strength
        self.strength_growth = strength_growth
        self.intelligence = intelligence
        self.intelligence_growth = intelligence_growth
        self.dexterity = dexterity
        self.dexterity_growth = dexterity_growth
        self.willpower = willpower
        self.willpower_growth = willpower_growth
        self.health = self.current_health = health
        self.health_growth = health_growth
        self.current_health = self.health
        self.health_regen = health_regen
        self.health_regen_growth = health_regen_growth
        self.init = init
        self.init_growth = init_growth
        self.bonus_init = 0  # exists for the purpose of init sorting in fight encounters with characters
        self.status_effects = []  # list of dicts w/ keys = name, stat, value, turns_remaining

        # Resistances
        self.earth_res = earth_res
        self.earth_res_growth = earth_res_growth
        self.fire_res = fire_res
        self.fire_res_growth = fire_res_growth
        self.electricity_res = electricity_res
        self.electricity_res_growth = electricity_res_growth
        self.water_res = water_res
        self.water_res_growth = water_res_growth

        # AI
        self.actions = actions
        self.goals = goals

    def scale(self, depth):
        self.level = depth
        gap = depth - 1
        self.strength += round(self.strength_growth * gap)
        self.intelligence += round(self.intelligence_growth * gap)
        self.dexterity += round(self.dexterity_growth * gap)
        self.willpower += round(self.willpower_growth * gap)
        self.health += round(self.health_growth * gap)
        self.current_health = self.health
        self.health_regen += round(self.health_regen_growth * gap)
        self.init += round(self.init_growth * gap)
        self.name = prefixes[utilities.clamp(int(depth / 10), 1, len(prefixes))] + " " + self.name

    def apply_status_effect(self, name: str, stat: str, value: int, turns_remaining: int):
        remove = None
        ret = None

        for se in self.status_effects:
            if se['name'] == name:
                remove = se
                break

        if remove is not None:
            self.remove_status_effect(remove)

        self.status_effects.append({'name': name, 'stat': stat, 'value': value, 'turns_remaining': turns_remaining})
        setattr(self, stat, getattr(self, stat) + value)

        if remove is not None:
            ret = remove['name']

        return ret

    def remove_status_effect(self, se):
        try:
            setattr(self, se['stat'], getattr(self, se['stat']) - se['value'])
            self.status_effects.remove(se)
        except KeyError:
            raise Exception(f'remove_status_effect failed for {self.name}: {se["name"]}, {se["stat"]}')

    def countdown_status_effects(self):
        removes = []
        out = ''

        for se in self.status_effects:
            if se['turns_remaining'] > 1:
                se['turns_remaining'] -= 1
            else:
                removes.append(se)

        if len(removes) > 0:
            for se in removes:
                out += f'{se["name"]} expired on {self.name}\n'
                self.remove_status_effect(se)

        return out

    def list_active_effects(self):
        out = ''

        for se in self.status_effects:
            out += se['name'] + ', '

        return out.rstrip(', ')

    def end_of_turn(self):
        out = ''

        if self.health_regen > 0 and self.current_health < self.health:
            self.current_health += int(self.health_regen)
            out = f'{self.name} regenerated {int(self.health_regen)} health.\n'

        for action in self.actions:
            if action.turns_remaining > 0:
                action.turns_remaining -= 1

        return out + self.countdown_status_effects()

    def take_a_turn(self, fight):
        plans = self.get_action_plans(fight)

        if len(plans) > 0:
            print(f'{self.name}\'s plans:')
            for plan in plans:
                print(': ' + plan.debug)

            plans.sort(key=lambda x: x.score, reverse=True)
            the_plan = plans[0]
            print(f'The chosen plan is: --{the_plan.debug}-- w/ score {the_plan.score}')
            return the_plan.action()
        else:
            return f'{self.name} took no action.'

    def get_action_plans(self, fight):
        plans = self.get_kill_player_plans(fight)

        if len(plans) > 0:
            return plans

        # damage_player goal
        goal = [x for x in self.goals if x.goal_type == GoalType.damage_player]

        if len(goal) > 0:
            plans += self.get_damage_player_plans(goal[0], fight)

        # debuff_player goal
        goal = [x for x in self.goals if x.goal_type == GoalType.debuff_player]

        if len(goal) > 0:
            plans += self.get_debuff_player_plans(goal[0], fight)

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

        # TODO enrage goal

        return plans

    def get_kill_player_plans(self, fight):
        plans = []

        for action in self.actions:
            if action.targets_players and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.damage_health, action.effects))

                if len(effects) > 0:
                    for character in fight.characters:
                        dmg = character.estimate_damage_from_enemy_action(self, action)

                        if dmg >= character.current_health:
                            plan = Plan()
                            plan.score = 9999999
                            plan.action = lambda action=action, character=character: action.do(self, character, fight)
                            plan.debug = f'kill {character.name} w/ {action.name} score {plan.score}'
                            plans.append(plan)

        return plans

    def get_damage_player_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_players and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.damage_health, action.effects))

                if len(effects) > 0:
                    for character in fight.characters:
                        dmg = character.estimate_damage_from_enemy_action(self, action)
                        plan = Plan()
                        plan.score = goal.value + 100 - int(max(character.current_health - dmg, 1) / (character.current_health + character.bonus_health) * 100)
                        plan.action = lambda action=action, character=character: action.do(self, character, fight)
                        plan.debug = f'damage {character.name} w/ {action.name} score {plan.score}'
                        plans.append(plan)

        return plans

    def get_debuff_player_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_players and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.debuff, action.effects))

                if len(effects) > 0:
                    for character in fight.characters:
                        plan = Plan()
                        plan.score = goal.value + 100 - (25 * len(character.status_effects))
                        plan.action = lambda action=action, character=character: action.do(self, character, fight)
                        plan.debug = f'debuff {character.name} w/ {action.name} score {plan.score}'
                        plans.append(plan)

        return plans

    def get_heal_ally_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_allies and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.restore_health, action.effects))

                if len(effects) > 0:
                    for enemy in fight.enemies:
                        plan = Plan()
                        plan.score = goal.value + 100 - int(enemy.current_health / enemy.health * 100)
                        plan.action = lambda action=action, enemy=enemy: action.do(self, enemy, fight)
                        plan.debug = f'heal {enemy.name} w/ {action.name} score {plan.score}'
                        plans.append(plan)

        return plans

    def get_buff_ally_plans(self, goal, fight):
        plans = []

        for action in self.actions:
            if action.targets_allies and action.is_usable(fight.states):
                effects = list(filter(lambda effect: effect.type == EffectType.buff, action.effects))

                if len(effects) > 0:
                    for enemy in fight.enemies:
                        plan = Plan()
                        plan.score = goal.value + (25 * len(enemy.status_effects))
                        plan.action = lambda action=action, enemy=enemy: action.do(self, enemy, fight)
                        plan.debug = f'buff {enemy.name} w/ {action.name} score {plan.score}'
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

    def get_element_scaling(self, element: Elements):
        if element == Elements.earth:
            stat = self.strength
        elif element == Elements.fire:
            stat = self.intelligence
        elif element == Elements.electricity:
            stat = self.dexterity
        elif element == Elements.water:
            stat = self.willpower
        else:
            raise Exception(f'{self.name} called enemy get_element_scaling with invalid element {element.name}')

        return 1.0 + (stat / 1000)

    def deal_damage(self, effect, critical=False):
        dmgs = []

        if effect.type == EffectType.damage_health:
            element_scaling = self.get_element_scaling(effect.element)
            min = effect.min
            max = effect.max

            if critical:
                dmgs.append((int(max * element_scaling), effect.element))
            else:
                dmgs.append((int(random.randint(min, max) * element_scaling), effect.element))
        else:
            raise Exception(f'{self.name} called enemy deal damage with invalid effect type {type(effect)}')

        return dmgs

    def take_damage(self, dmgs: list, ele_pens: tuple) -> list:
        for dmg in dmgs:
            amt = dmg[0]

            if dmg[1] == Elements.earth:
                amt *= (1.0 - self.earth_res + min(ele_pens[0], self.earth_res))
            elif dmg[1] == Elements.fire:
                amt *= (1.0 - self.fire_res + min(ele_pens[1], self.fire_res))
            elif dmg[1] == Elements.electricity:
                amt *= (1.0 - self.electricity_res + min(ele_pens[2], self.electricity_res))
            elif dmg[1] == Elements.water:
                amt *= (1.0 - self.water_res + min(ele_pens[3], self.water_res))

            self.current_health -= round(amt)
            self.current_health = max(0, self.current_health)

        return dmgs

    def restore_health(self, amount: int, source=None):
        start = self.current_health

        if source is not None and isinstance(source, Enemy):
            self.current_health += int(amount * source.get_element_scaling(Elements.water))
        else:
            self.current_health += amount

        if self.current_health > self.health:
            self.current_health = self.health

        return self.current_health - start


prefixes = {
    1: 'Pico',
    2: 'Nano',
    3: 'Micro',
    4: 'Milli',
    5: 'Centi',
    6: 'Deci',
    7: 'Nomi',
    8: 'Deca',
    9: 'Hecto',
    10: 'Kilo',
    11: 'Mega',
    12: 'Giga',
    13: 'Tera',
    14: 'Peta',
    15: 'Exa',
    16: 'Zetta',
    17: 'Yotta'
}
