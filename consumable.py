from mongokit_ng import Document
import random

from ingredient import IngredientType
from item import add_affix
from prefixes import level_prefixes


class Consumable(Document):
    __database__ = 'delverpg'
    __collection__ = 'consumables'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'rarity': int,
        'weight': int,
        '_itype': int,
        'uses': int,
        'health': int,
        'stamina': int,
        'mana': int,
        'burn': int,
        'bleed': int,
        'shock': int,
        'confusion': int,
        'value': int,
    }
    required_fields = [
        'name',
        'description',
        'level',
        'rarity',
        'weight',
        '_itype',
        'uses',
        'health',
        'stamina',
        'mana',
        'burn',
        'bleed',
        'shock',
        'confusion',
        'value'
    ]
    default_values = {
        '_itype': 9,
    }
    use_dot_notation = True
    use_autorefs = True


def create_consumable(connection, ingredients: list):
    if len(ingredients) > 3 or len(ingredients) < 1:
        return False

    result = connection.Consumable()
    result['level'] = max(round(sum([x['level'] for x in ingredients if x['type'] != IngredientType.neutral.value]) / len(ingredients)), 1)
    result['name'] = f'{level_prefixes[min(result["level"], 17)]} Potion'
    result['description'] = 'A consumable potion brewed by |.'
    result['rarity'] = max(x['rarity'] for x in ingredients)
    result['health'] = 0
    result['stamina'] = 0
    result['mana'] = 0
    result['burn'] = 0
    result['bleed'] = 0
    result['shock'] = 0
    result['confusion'] = 0
    result['uses'] = 1
    result['weight'] = 1
    result['value'] = 0

    for ingredient in ingredients:
        if ingredient['effect'] is not None:
            result[ingredient['effect']] += hsm_level_values[result['level']]
        elif ingredient['type'] == IngredientType.guano.value:
            result['burn'] = result['bleed'] = result['shock'] = result['confusion'] = status_level_values[result['level']]

        result['value'] += ingredient['level'] * ingredient['rarity']

    if result['rarity'] in [2, 3]:
        if result['rarity'] == 3:
            key = random.choice(list(suffixes.keys()))
            result = add_affix(result, key, suffixes[key], result['level'])

        key = random.choice(list(prefixes.keys()))
        result = add_affix(result, key, prefixes[key], result['level'])

    result.save()
    return result


hsm_level_values = [
    0,  # Skipped
    5,
    8,
    12,
    17,
    23,
    30,
    38,
    57,
    67,
    78,
    90,
    0,
    0,
    0,
    0,
    0,
    0,
]


status_level_values = [
    0,  # Skipped
    -1,
    -1,
    -2,
    -2,
    -2,
    -3,
    -3,
    -3,
    -3,
    -3,
    -3,
    -3,
    -3,
    -3,
    -3,
    -3,
    -3,
]


prefixes = {
    'Collectible': {
        1: {'effect': 'value', 'value': 10},
        3: {'effect': 'value', 'value': 20},
    },
    'Lightweight': {
        1: {'effect': 'weight', 'value': -1}
    },
    'Revitalizing': {
        1: {'effect': 'health', 'value': 2},
        3: {'effect': 'health', 'value': 5},
    },
    'Recharging': {
        1: {'effect': 'stamina', 'value': 2},
        3: {'effect': 'stamina', 'value': 5},
    },
    'Replenishing': {
        1: {'effect': 'mana', 'value': 2},
        3: {'effect': 'mana', 'value': 5},
    },
}

suffixes = {
    'Gilded': {
        1: {'effect': 'value', 'value': 20},
        3: {'effect': 'value', 'value': 40},
    },
    'Infused': {
        1: {'effect': 'uses', 'value': 1}
    },
    'Cooling': {
        1: {'effect': 'burn', 'value': -2}
    },
    'Staunching': {
        1: {'effect': 'bleed', 'value': -2}
    },
    'Grounding': {
        1: {'effect': 'shock', 'value': -2}
    },
    'Reorienting': {
        1: {'effect': 'confusion', 'value': -2}
    },
}
