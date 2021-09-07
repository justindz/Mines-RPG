from enum import Enum
from mongokit_ng import Document

import utilities
from elements import Elements

valid_slots = ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring']


class WeaponType(Enum):
    hammer = 1
    sword = 2
    dagger = 3
    staff = 4
    axe = 5
    spear = 6
    flail = 7
    fist = 8
    magic = 9
    thrown = 10


class Weapon(Document):
    __database__ = 'delverpg'
    __collection__ = 'weapons'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'rarity': int,
        'weight': int,
        '_itype': int,
        '_weapon_type': int,
        'sockets': list,
        'bonus_strength': int,
        'bonus_intelligence': int,
        'bonus_dexterity': int,
        'bonus_willpower': int,
        'bonus_health': int,
        'bonus_stamina': int,
        'bonus_mana': int,
        'bonus_init': int,
        'base_crit_chance': float,
        'damages': None,
        'crit_damage': int,
        'value': int,
        'required_strength': int,
        'required_intelligence': int,
        'required_dexterity': int,
        'required_willpower': int,
        'earth_penetration': float,
        'fire_penetration': float,
        'electricity_penetration': float,
        'water_penetration': float,
    }
    required_fields = [
        'name',
        'description',
        'level',
        'rarity',
        'weight',
        '_itype',
        '_weapon_type',
        'sockets',
        'bonus_strength',
        'bonus_intelligence',
        'bonus_dexterity',
        'bonus_willpower',
        'bonus_health',
        'bonus_stamina',
        'bonus_mana',
        'bonus_init',
        'base_crit_chance',
        'damages',
        'crit_damage',
        'value',
        'required_strength',
        'required_intelligence',
        'required_dexterity',
        'required_willpower',
        'earth_penetration',
        'fire_penetration',
        'electricity_penetration',
        'water_penetration'
    ]
    default_values = {
        '_itype': 1,
        'bonus_strength': 0,
        'bonus_intelligence': 0,
        'bonus_dexterity': 0,
        'bonus_willpower': 0,
        'bonus_health': 0,
        'bonus_stamina': 0,
        'bonus_mana': 0,
        'bonus_init': 0,
        'required_strength': 0,
        'required_intelligence': 0,
        'required_dexterity': 0,
        'required_willpower': 0,
        'earth_penetration': 0.0,
        'fire_penetration': 0.0,
        'electricity_penetration': 0.0,
        'water_penetration': 0.0,
    }
    use_dot_notation = True
    use_autorefs = True


def get_damages_display_string(item):
    display_string = ''

    for damage in item['damages']:
        display_string += f'\n  {damage[0]}d{damage[1]} {utilities.get_elemental_symbol(Elements(damage[2]))}'

    return display_string


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
    display_string += f'\nEarth Penetration {item["earth_penetration"]:.0%}' if item['earth_penetration'] > 0 else ''
    display_string += f'\nFire Penetration {item["fire_penetration"]:.0%}' if item['fire_penetration'] > 0 else ''
    display_string += f'\nElectricity Penetration {item["electricity_penetration"]:.0%}' if item[
                                                                                                'electricity_penetration'] > 0 else ''
    display_string += f'\nWater Penetration {item["water_penetration"]:.0%}' if item['water_penetration'] > 0 else ''
    return display_string.lstrip('\n')


all_types = [WeaponType.hammer, WeaponType.sword, WeaponType.dagger, WeaponType.staff, WeaponType.axe, WeaponType.spear,
             WeaponType.flail, WeaponType.fist, WeaponType.magic, WeaponType.thrown]
melee_types = [WeaponType.hammer, WeaponType.sword, WeaponType.dagger, WeaponType.staff, WeaponType.axe,
               WeaponType.spear, WeaponType.flail, WeaponType.fist]
bladed_types = [WeaponType.sword, WeaponType.dagger, WeaponType.axe, WeaponType.fist]
blunt_types = [WeaponType.hammer, WeaponType.staff, WeaponType.flail]

prefixes = {
    'Honed': {
        1: {'effect': 'required_strength', 'value': -1}
    },
    'Intuitive': {
        1: {'effect': 'required_intelligence', 'value': -1}
    },
    'Balanced': {
        1: {'effect': 'required_dexterity', 'value': -1}
    },
    'Attuned': {
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
    'Unleashing': {
        1: {'effect': 'bonus_dexterity', 'value': 1}
    },
    'Inspiring': {
        1: {'effect': 'bonus_willpower', 'value': 1}
    },
    'Vigilant': {
        1: {'effect': 'bonus_init', 'value': 1}
    },
    'Wicked': {
        1: {'effect': 'base_crit_chance', 'value': 0.1},
        2: {'effect': 'base_crit_chance', 'value': 0.2},
        3: {'effect': 'base_crit_chance', 'value': 0.3},
    },
    'Powerful': {
        1: {'effect': 'dice_added', 'value': 1}
    },
    'Smoldering': {
        1: {'effect': 'damage_convert', 'value': Elements.fire.value},
    },
    'Sparking': {
        1: {'effect': 'damage_convert', 'value': Elements.electricity.value},
    },
    'Flowing': {
        1: {'effect': 'damage_convert', 'value': Elements.water.value},
    },
    'Shattering': {
        1: {'effect': 'earth_penetration', 'value': 0.05},
    },
    'Quenching': {
        1: {'effect': 'fire_penetration', 'value': 0.05},
    },
    'Grounding': {
        1: {'effect': 'electricity_penetration', 'value': 0.05},
    },
    'Absorbing': {
        1: {'effect': 'water_penetration', 'value': 0.05},
    },
}

suffixes = {
    'Gilded': {
        1: {'effect': 'value', 'value': 100}
    },
    'Sinful': {
        1: {'effect': 'crit_damage', 'value': 2}
    },
    'Volcanic': {
        1: {'effect': 'damage_mode', 'value': [1, 2, Elements.fire.value]}
    },
    'Charged': {
        1: {'effect': 'damage_mode', 'value': [1, 2, Elements.electricity.value]}
    },
    'Drenched': {
        1: {'effect': 'damage_mode', 'value': [1, 2, Elements.water.value]}
    },
    'True': {
        1: {'effect': 'damage_narrow'}
    },
    'Wild': {
        1: {'effect': 'damage_spread'}
    },
    'Peerless': {
        1: {'effect': 'socket'}
    },
}
