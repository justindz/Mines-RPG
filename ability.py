from enum import Enum


class EffectType(Enum):
    damage_health = 1
    damage_stamina = 2
    damage_mana = 3
    restore_health = 4
    restore_stamina = 5
    restore_mana = 6
    drain_health = 7
    drain_stamina = 8
    drain_mana = 9
    buff_crit = 10
    debuff_crit = 11
    buff_damage = 12
    debuff_damage = 13
    buff_resist = 14
    debuff_resist = 15
    buff_area = 16
    debuff_area = 17


class Ability:
    def __init__(self, _name, _description, _level, _cost, _effects, _area, _area_modifiable):
        self.name = _name
        self.description = _description
        self.level = _level
        self.cost = _cost
        self.effects = _effects
        self.area = _area
        self.area_modifiable = _area_modifiable
