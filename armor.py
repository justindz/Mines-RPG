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
        'earth_res': float,
        'fire_res': float,
        'electricity_res': float,
        'water_res': float,
        'value': int,
        'required_strength': int,
        'required_intelligence': int,
        'required_dexterity': int,
        'required_willpower': int,
    }
    required_fields = ['name', 'description', 'level', 'rarity', 'weight', '_itype', 'bonus_strength',
                       'bonus_intelligence', 'bonus_dexterity', 'bonus_willpower', 'bonus_health', 'bonus_stamina',
                       'bonus_mana', 'bonus_init', 'bonus_carry', 'earth_res', 'fire_res', 'electricity_res',
                       'water_res', 'value', 'required_strength', 'required_intelligence', 'required_dexterity',
                       'required_willpower']
    use_dot_notation = True
    use_autorefs = True


def get_bonuses_display_string(item):
    display_string = ''
    display_string += '\nStrength {:+}'.format(item['bonus_strength']) if item['bonus_strength'] != 0 else ''
    display_string += '\nIntelligence {:+}'.format(item['bonus_intelligence']) if item['bonus_intelligence'] != 0 else ''
    display_string += '\nDexterity {:+}'.format(item['bonus_dexterity']) if item['bonus_dexterity'] != 0 else ''
    display_string += '\nWillpower {:+}'.format(item['bonus_willpower']) if item['bonus_willpower'] != 0 else ''
    display_string += '\nHealth {:+}'.format(item['bonus_health']) if item['bonus_health'] != 0 else ''
    display_string += '\nStamina {:+}'.format(item['bonus_stamina']) if item['bonus_stamina'] != 0 else ''
    display_string += '\nMana {:+}'.format(item['bonus_mana']) if item['bonus_mana'] != 0 else ''
    display_string += '\nInitiative {:+}'.format(item['bonus_init']) if item['bonus_init'] != 0 else ''
    display_string += '\nCarry {:+}'.format(item['bonus_carry']) if item['bonus_carry'] != 0 else ''
    display_string += '\nEarth Res {:+}'.format(item['earth_res']) if item['earth_res'] != 0.0 else ''
    display_string += '\nFire Res {:+}'.format(item['fire_res']) if item['fire_res'] != 0.0 else ''
    display_string += '\nElectricity Res {:+}'.format(item['electricity_res']) if item['electricity_res'] != 0.0 else ''
    display_string += '\nWater Res {:+}'.format(item['water_res']) if item['water_res'] != 0.0 else ''
    return display_string


armors = {
    'test_helmet': {'name': 'RND Helmet', 'description': 'Shite.', 'level': 1, 'weight': 2, '_itype': 2,
                    'bonus_strength': 1, 'bonus_intelligence': 0, 'bonus_dexterity': 0, 'bonus_willpower': 0,
                    'bonus_health': 0, 'bonus_stamina': 0, 'bonus_mana': 0, 'bonus_init': 1, 'bonus_carry': 0,
                    'earth_res': 0.0, 'fire_res': 0.0, 'electricity_res': 0.0, 'water_res': 0.0, 'required_strength': 0,
                    'required_intelligence': 0, 'required_dexterity': 0, 'required_willpower': 0}
}

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
        1: {'effect': 'earth_res', 'value': 0.1}
    },
    'Insulated': {
        1: {'effect': 'fire_res', 'value': 0.1}
    },
    'Grounded': {
        1: {'effect': 'electricity_res', 'value': 0.1}
    },
    'Sealed': {
        1: {'effect': 'water_res', 'value': 0.1}
    },
}

suffixes = {
    'Gilded': {
        1: {'effect': 'value', 'value': 100}
    },
    'Reinforcing': {
        1: {'effect': 'earth_res', 'value': 0.15}
    },
    'Chilling': {
        1: {'effect': 'fire_res', 'value': 0.15}
    },
    'Conducting': {
        1: {'effect': 'electricity_res', 'value': 0.15}
    },
    'Absorbing': {
        1: {'effect': 'water_res', 'value': 0.15}
    },
}
