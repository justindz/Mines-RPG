from item import Item
from pymodm import fields


class Armor(Item):
    value = fields.IntegerField(required=True, default=0)
    sockets = fields.ListField(required=True)
    bonus_strength = fields.IntegerField(required=True, default=0)
    bonus_intelligence = fields.IntegerField(required=True, default=0)
    bonus_dexterity = fields.IntegerField(required=True, default=0)
    bonus_willpower = fields.IntegerField(required=True, default=0)
    bonus_health = fields.IntegerField(required=True, default=0)
    bonus_health_regen = fields.IntegerField(required=True, default=0)
    bonus_stamina = fields.IntegerField(required=True, default=0)
    bonus_stamina_regen = fields.IntegerField(required=True, default=0)
    bonus_mana = fields.IntegerField(required=True, default=0)
    bonus_mana_regen = fields.IntegerField(required=True, default=0)
    bonus_init = fields.IntegerField(required=True, default=0)
    bonus_carry = fields.IntegerField(required=True, default=0)
    bonus_earth_res = fields.FloatField(required=True, default=0.0)
    bonus_fire_res = fields.FloatField(required=True, default=0.0)
    bonus_electricity_res = fields.FloatField(required=True, default=0.0)
    bonus_water_res = fields.FloatField(required=True, default=0.0)


def get_bonuses_display_string(item):
    display_string = ''
    display_string += f'\nStrength {item["bonus_strength"]:+}' if item['bonus_strength'] != 0 else ''
    display_string += f'\nIntelligence {item["bonus_intelligence"]:+}' if item['bonus_intelligence'] != 0 else ''
    display_string += f'\nDexterity {item["bonus_dexterity"]:+}' if item['bonus_dexterity'] != 0 else ''
    display_string += f'\nWillpower {item["bonus_willpower"]:+}' if item['bonus_willpower'] != 0 else ''
    display_string += f'\nHealth {item["bonus_health"]:+}' if item['bonus_health'] != 0 else ''
    display_string += f'\nHealth Regen {item["bonus_health_regen"]:+}' if item['bonus_health_regen'] != 0 else ''
    display_string += f'\nStamina {item["bonus_stamina"]:+}' if item['bonus_stamina'] != 0 else ''
    display_string += f'\nStamina Regen {item["bonus_stamina_regen"]:+}' if item['bonus_stamina_regen'] != 0 else ''
    display_string += f'\nMana {item["bonus_mana"]:+}' if item['bonus_mana'] != 0 else ''
    display_string += f'\nMana Regen {item["bonus_mana_regen"]:+}' if item['bonus_mana_regen'] != 0 else ''
    display_string += f'\nInitiative {item["bonus_init"]:+}' if item['bonus_init'] != 0 else ''
    display_string += f'\nCarry {item["bonus_carry"]:+}' if item['bonus_carry'] != 0 else ''
    display_string += f'\nEarth Res {item["bonus_earth_res"]:+.0%}' if item['bonus_earth_res'] != 0.0 else ''
    display_string += f'\nFire Res {item["bonus_fire_res"]:+.0%}' if item['bonus_fire_res'] != 0.0 else ''
    display_string += f'\nElectricity Res {item["bonus_electricity_res"]:+.0%}' if item['bonus_electricity_res'] != 0.0 else ''
    display_string += f'\nWater Res {item["bonus_water_res"]:+.0%}' if item['bonus_water_res'] != 0.0 else ''
    return display_string.lstrip('\n')


prefixes = {
    'Collectible': {
        1: {'effect': 'value', 'value': 30}
    },
    'Lightweight': {
        1: {'effect': 'weight', 'value': -1}
    },
    'Empowering': {
        1: {'effect': 'bonus_strength', 'value': 1}
    },
    'Enlightening': {
        1: {'effect': 'bonus_intelligence', 'value': 1}
    },
    'Unleashing': {
        1: {'effect': 'bonus_dexterity', 'value': 1}
    },
    'Inspiring': {
        1: {'effect': 'bonus_willpower', 'value': 1}
    },
    'Modular': {
        1: {'effect': 'bonus_carry', 'value': 10}
    },
    'Vigilant': {
        1: {'effect': 'bonus_init', 'value': 1}
    },
    'Hardened': {
        1: {'effect': 'bonus_earth_res', 'value': 0.05}
    },
    'Insulated': {
        1: {'effect': 'bonus_fire_res', 'value': 0.05}
    },
    'Grounded': {
        1: {'effect': 'bonus_electricity_res', 'value': 0.05}
    },
    'Sealed': {
        1: {'effect': 'bonus_water_res', 'value': 0.05}
    },
}

suffixes = {
    'Gilded': {
        1: {'effect': 'value', 'value': 100}
    },
    'Reinforcing': {
        1: {'effect': 'bonus_earth_res', 'value': 0.05}
    },
    'Chilling': {
        1: {'effect': 'bonus_fire_res', 'value': 0.05}
    },
    'Conducting': {
        1: {'effect': 'bonus_electricity_res', 'value': 0.05}
    },
    'Absorbing': {
        1: {'effect': 'bonus_water_res', 'value': 0.05}
    },
    'Medicinal': {
        1: {'effect': 'bonus_health_regen', 'value': 1}
    },
    'Stimulant': {
        1: {'effect': 'bonus_stamina_regen', 'value': 1}
    },
    'Arcane': {
        1: {'effect': 'bonus_mana_regen', 'value': 1}
    },
    'Peerless': {
        1: {'effect': 'socket'}
    },
}
