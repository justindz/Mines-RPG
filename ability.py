from enum import Enum


class EffectType(Enum):
    damage_health = 1
    restore_health = 2
    restore_stamina = 3
    restore_mana = 4
    drain_health = 5
    buff_crit = 6
    debuff_crit = 7
    buff_damage = 8
    debuff_damage = 9
    buff_resist = 10
    debuff_resist = 11
    buff_area = 12
    debuff_area = 13


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
