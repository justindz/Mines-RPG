from enum import Enum


class EffectType(Enum):
    damage_health = 1
    restore_health = 2
    restore_stamina = 3
    restore_mana = 4
    buff = 5
    debuff = 6
    summon = 7
    burn = 8
    bleed = 9


class Ability:
    def __init__(self, _name, _description, _cost, _effects, _activates, _consumes, _area, _area_modifiable):
        self.name = _name
        self.description = _description
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


class Effect:
    def __init__(self, _type, _element, _dice_value=None, _status_effect_value=None, _stat=None,
                 _status_effect_name=None, _status_effect_turns=None):
        if _type in [EffectType.restore_health, EffectType.restore_stamina,
                     EffectType.restore_mana] and _dice_value is None:
            raise Exception(f'Malformed dice value for SpellEffect: {_type}, {_element}, {_dice_value}')
        if _type in [EffectType.buff, EffectType.debuff] and (_status_effect_name is None or _stat is None or
                                                              _status_effect_turns is None):
            raise Exception(f'Malformed status effect for SpellEffect: {_type}, {_element}, {_status_effect_value}')

        self.type = _type
        self.element = _element
        self.status_effect_value = _status_effect_value
        self.dice_value = _dice_value  # unused for status effects (buff, debuff)
        self.status_effect_name = _status_effect_name
        self.stat = _stat
        self.status_effect_turns = _status_effect_turns
