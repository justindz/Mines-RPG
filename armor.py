from mongokit_ng import Document


class Armor(Document):
    __database__ = 'delverpg'
    __collection__ = 'armor'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'rarity': int,
        'weight': int,
        '_itype': int,
        'bonus_strength': int,
        'bonus_intelligence': int,
        'bonus_dexterity': int,
        'bonus_willpower': int,
        'bonus_health': int,
        'bonus_stamina': int,
        'bonus_mana': int,
        'bonus_init': int,
        'bonus_carry': int,
        'bonus_earth_res': float,
        'bonus_fire_res': float,
        'bonus_electricity_res': float,
        'bonus_water_res': float,
        'value': int,
        'required_strength': int,
        'required_intelligence': int,
        'required_dexterity': int,
        'required_willpower': int,
    }
    required_fields = ['name', 'description', 'level', 'rarity', 'weight', '_itype', 'bonus_strength',
                       'bonus_intelligence', 'bonus_dexterity', 'bonus_willpower', 'bonus_health', 'bonus_stamina',
                       'bonus_mana', 'bonus_init', 'bonus_carry', 'bonus_earth_res', 'bonus_fire_res', 'bonus_electricity_res',
                       'bonus_water_res', 'value', 'required_strength', 'required_intelligence', 'required_dexterity',
                       'required_willpower']
    use_dot_notation = True
    use_autorefs = True


def get_bonuses_display_string(item):
    display_string = ''
    display_string += f'\nStrength {item["bonus_strength"]:+}' if item['bonus_strength'] != 0 else ''
    display_string += f'\nIntelligence {item["bonus_intelligence"]:+}' if item['bonus_intelligence'] != 0 else ''
    display_string += f'\nDexterity {item["bonus_dexterity"]:+}' if item['bonus_dexterity'] != 0 else ''
    display_string += f'\nWillpower {item["bonus_willpower"]:+}' if item['bonus_willpower'] != 0 else ''
    display_string += f'\nHealth {item["bonus_health"]:+}' if item['bonus_health'] != 0 else ''
    display_string += f'\nStamina {item["bonus_stamina"]:+}' if item['bonus_stamina'] != 0 else ''
    display_string += f'\nMana {item["bonus_mana"]:+}' if item['bonus_mana'] != 0 else ''
    display_string += f'\nInitiative {item["bonus_init"]:+}' if item['bonus_init'] != 0 else ''
    display_string += f'\nCarry {item["bonus_carry"]:+}' if item['bonus_carry'] != 0 else ''
    display_string += f'\nEarth Res {item["bonus_earth_res"]:+.0%}' if item['bonus_earth_res'] != 0.0 else ''
    display_string += f'\nFire Res {item["bonus_fire_res"]:+.0%}' if item['bonus_fire_res'] != 0.0 else ''
    display_string += f'\nElectricity Res {item["bonus_electricity_res"]:+.0%}' if item['bonus_electricity_res'] != 0.0 else ''
    display_string += f'\nWater Res {item["bonus_water_res"]:+.0%}' if item['bonus_water_res'] != 0.0 else ''
    return display_string.lstrip('\n')


prefixes = {
    'Streamlined': {
        1: {'effect': 'required_strength', 'value': -1}
    },
    'Striking': {
        1: {'effect': 'required_intelligence', 'value': -1}
    },
    'Fitted': {
        1: {'effect': 'required_dexterity', 'value': -1}
    },
    'Pious': {
        1: {'effect': 'required_willpower', 'value': -1}
    },
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
    'Encouraging': {
        1: {'effect': 'bonus_dexterity', 'value': 1}
    },
    'Inspiring': {
        1: {'effect': 'bonus_willpower', 'value': 1}
    },
    'Cargo': {
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
}
