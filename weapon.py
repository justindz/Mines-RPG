from enum import Enum
from mongokit_ng import Document

from elements import Elements

valid_slots = ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring']


class WeaponType(Enum):
    dagger = 1
    sword = 2
    spear = 3
    axe = 4
    mace = 5
    staff = 6


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
    }
    required_fields = ['name', 'description', 'level', 'rarity', 'weight', '_itype', '_weapon_type', 'bonus_strength',
                       'bonus_intelligence', 'bonus_dexterity', 'bonus_willpower', 'bonus_health', 'bonus_stamina',
                       'bonus_mana', 'bonus_init', 'base_crit_chance', 'damages', 'crit_damage', 'value',
                       'required_strength', 'required_intelligence', 'required_dexterity', 'required_willpower']
    use_dot_notation = True
    use_autorefs = True


def get_damages_display_string(item):
    display_string = ''

    for damage in item['damages']:
        display_string += '{}-{} {}\n'.format(damage[0], damage[1], Elements(damage[2]).name)

    return display_string


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
    return display_string


weapons = {
    'test_sword': {'name': 'RND Sword', 'description': 'Shite.', 'level': 1, 'weight': 3, '_itype': 1,
                   '_weapon_type': WeaponType.sword.value, 'bonus_strength': 1, 'bonus_intelligence': 0,
                   'bonus_dexterity': 0, 'bonus_willpower': 0, 'bonus_health': 0, 'bonus_stamina': 0, 'bonus_mana': 0,
                   'bonus_init': 0, 'base_crit_chance': 0.5, 'damages': [[1, 4, Elements.earth.value]], 'crit_damage': 0,
                   'required_strength': 0, 'required_intelligence': 0, 'required_dexterity': 0, 'required_willpower': 0}
}

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
    'Encouraging': {
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
        1: {'effect': 'damage_added', 'value': 0.2}
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
    'Consistent': {
        1: {'effect': 'damage_narrow', 'value': 10}
    },
    'Wild': {
        1: {'effect': 'damage_spread', 'value': 10}
    },
}
