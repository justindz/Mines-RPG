from enum import Enum


class EffectType(Enum):
    damage_health = 1
    restore_health = 2
    restore_stamina = 3
    restore_mana = 4
    buff = 5
    debuff = 6


class Ability:
    def __init__(self, _name, _description, _level, _cost, _effects, _activates, _consumes, _area, _area_modifiable):
        self.name = _name
        self.description = _description
        self.level = _level
        self.cost = _cost
        self.effects = _effects
        self.activates = _activates
        self.consumes = _consumes
        self.area = _area
        self.area_modifiable = _area_modifiable

    def ability_cost_to_str(self) -> str:
        out = ''

        if self.cost['h'] != 0:
            out += f'{self.cost["h"]}h '

        if self.cost['s'] != 0:
            out += f'{self.cost["s"]}s '

        if self.cost['m'] != 0:
            out += f'{self.cost["m"]}m '

        return out.rstrip(' ')
