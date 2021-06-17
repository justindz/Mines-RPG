from enum import Enum
from mongokit_ng import Document

from item import ItemType
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
    }
    required_fields = ['name', 'description', 'level', 'weight', '_itype', 'bonus_strength', 'bonus_intelligence',
                       'bonus_dexterity', 'bonus_willpower', 'bonus_health', 'bonus_stamina', 'bonus_mana',
                       'bonus_init', 'base_crit_chance', 'damages']
    default_values = {
        'name': 'Test Sword',
        'description': 'An RND sword.',
        'level': 1,
        'weight': 3,
        '_itype': ItemType.weapon.value,
        '_weapon_type': WeaponType.sword.value,
        'bonus_strength': 1,
        'bonus_intelligence': 0,
        'bonus_dexterity': 0,
        'bonus_willpower': 0,
        'bonus_health': 0,
        'bonus_stamina': 0,
        'bonus_mana': 0,
        'bonus_init': 0,
        'base_crit_chance': 0.05,
        'damages': [
            [1, 4, Elements.earth.value]
        ],
    }
    use_dot_notation = True
    use_autorefs = True


def get_damages_display_string(item):
    display_string = ''

    for damage in item['damages']:
        display_string += '{}-{} {}\n'.format(damage[0], damage[1], Elements(damage[2]).name)

    return display_string


def get_bonuses_display_string(item):
    display_string = ''

    if item['bonus_strength'] != 0:
        display_string += '\nStrength {:+}'.format(item['bonus_strength'])
    if item['bonus_intelligence'] != 0:
        display_string += '\nIntelligence {:+}'.format(item['bonus_intelligence'])
    if item['bonus_dexterity'] != 0:
        display_string += '\nDexterity {:+}'.format(item['bonus_dexterity'])
    if item['bonus_willpower'] != 0:
        display_string += '\nWillpower {:+}'.format(item['bonus_willpower'])
    if item['bonus_health'] != 0:
        display_string += '\nHealth {:+}'.format(item['bonus_health'])
    if item['bonus_stamina'] != 0:
        display_string += '\nStamina {:+}'.format(item['bonus_stamina'])
    if item['bonus_mana'] != 0:
        display_string += '\nMana {:+}'.format(item['bonus_mana'])
    if item['bonus_init'] != 0:
        display_string += '\nInitiative {:+}'.format(item['bonus_init'])

    return display_string
