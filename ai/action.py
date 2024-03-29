from ability import EffectType
from elements import Elements


class Action:
    def __init__(self):
        self.name = 'Default Action'
        self.description = 'Report a bug and reference the enemy that used this ability!'
        self.effects = []
        self.cooldown = 0
        self.turns_remaining = 0
        self.activates = []
        self.consumes = []
        self.targets_opponents = False
        self.targets_allies = False
        self.area = 0
        self.area_modifiable = False
        self.summon = None

    def is_usable(self, states: [Elements]):
        return not self.is_on_cooldown() and self.meets_state_requirements(states)

    def check_cooldown(self):
        if self.cooldown > 0 and self.turns_remaining == 0:
            self.turns_remaining += self.cooldown

    def is_on_cooldown(self):
        if self.cooldown > 0 and self.turns_remaining > 0:
            return True

        return False

    def meets_state_requirements(self, states: [Elements]):
        if len(self.consumes) == 0:
            return True

        for state in self.consumes:
            if state not in states:
                return False

        return True

    def handle_elements(self, fight) -> str:
        out = ''

        for state in self.consumes:
            fight.consume(state)
            out += f'\n{state.name.capitalize()} has been consumed.'

        for state in self.activates:
            fight.activate(state)
            out += f'\n{state.name.capitalize()} has been infused.'

        return out

    def get_aoe_targets(self, group: list, target) -> list:
        targets = [target]

        if self.area > 0:
            i = self.area

            while i > 0:
                if group.index(target) + i <= len(group) - 1:
                    targets.append(group[group.index(target) + i])

                if group.index(target) - i >= 0:
                    targets.insert(0, group[group.index(target) - i])

                i -= 1

        return targets

    def deal_damage(self, crit: bool, fight, out: str, targets, user):
        for target in targets:
            for effect in self.effects:
                if effect.type == EffectType.damage_health:
                    dmgs = target.take_damage(user.deal_damage(effect, critical=crit), user.ele_pens)
                    shock = False
                    confusion = False

                    for dmg in dmgs:
                        ele = Elements(dmg[1])
                        out += f'\n{target.name} suffered {dmg[0]} {Elements(dmg[1]).name} damage.'
                        shock = True if ele == Elements.electricity else False
                        confusion = True if ele == Elements.water else False

                    if shock:
                        target.shock += 1
                    if confusion:
                        target.confusion += 1
                elif effect.type == EffectType.burn:
                    if target.apply_burn(effect.effect_turns, effect.dot_value,
                                         user.dot_effect, user.dot_duration):
                        out += f'\n{target.name} is burning.'
                    else:
                        out += f'\n{target.name} is already seriously burning.'
                elif effect.type == EffectType.bleed:
                    if target.apply_bleed(effect.effect_turns, effect.dot_value,
                                          user.dot_effect, user.dot_duration):
                        out += f'\n{target.name} is bleeding.'
                    else:
                        out += f'\n{target.name} is bleeding more severely.'
        out += self.handle_elements(fight)
        return out
