import random
from mongokit_ng import Document
from enum import Enum

import utilities
from prefixes import level_prefixes


class IngredientType(Enum):
    moss = 1  # Health
    fungi = 2  # Stamina
    algae = 3  # Mana
    guano = 4  # Status
    neutral = 5  # Rarity


class Ingredient(Document):
    __database__ = 'delverpg'
    __collection__ = 'ingredients'
    structure = {
        'name': str,
        'description': str,
        'type': int,
        'level': int,
        'rarity': int,
        'effect': None,
        'weight': int,
        '_itype': int,
        'value': int,
    }
    required_fields = [
        'name',
        'description',
        'type',
        'level',
        'rarity',
        # 'effect', This value is not in required fields, because it throws an error when the value is None
        'weight',
        '_itype',
        'value'
    ]
    default_values = {
        '_itype': 12,
        'level': 1,
        'weight': 1,
        'value': 1,
    }
    use_dot_notation = True
    use_autorefs = True


def get_ingredient(connection, key: str, level: int) -> Ingredient:
    result = connection.Ingredient()
    result.level = min(level, 1)

    for k, v in ingredients[key].items():
        result[k] = v

    result.name = f'{level_prefixes[utilities.clamp(level, 1, 17)]} {result.name}'
    result.save()
    return result


def get_random_ingredient(connection, level: int, rarity=1):
    candidates = {k: v for k, v in ingredients.items() if v['rarity'] == rarity}

    if len(candidates) > 0:
        key = random.choice(list(candidates.keys()))
        return get_ingredient(connection, key, level)
    else:
        print(f'Random ingredient generation at rarity {rarity} and level {level} found zero candidates.')

    return None


ingredients = {
    'moss': {
        'name': 'Moss',
        'description': 'Moss recovered from a mine. Soothing to the touch.',
        'type': IngredientType.moss.value,
        'rarity': 1,
        'effect': 'health',
    },
    'fungi': {
        'name': 'Fungi',
        'description': 'Fungi recovered from a mine. Hopefully, a stimulant variety.',
        'type': IngredientType.fungi.value,
        'rarity': 1,
        'effect': 'stamina',
    },
    'algae': {
        'name': 'Algae',
        'description': 'Algae recovered from a mine. It glows with an internal light.',
        'type': IngredientType.algae.value,
        'rarity': 1,
        'effect': 'mana',
    },
    'guano': {
        'name': 'Guano',
        'description': 'Guano scraped from the walls of a mine. Dried, thankfully, so the smell is minimal.',
        'type': IngredientType.guano.value,
        'rarity': 1,
        'effect': None,
    },
    'ash': {
        'name': 'Ash',
        'description': 'Ash recovered from a long-forgotten fire.',
        'type': IngredientType.neutral.value,
        'rarity': 2,
        'effect': None,
    },
    'salt': {
        'name': 'Salt',
        'description': 'Salt recovered from an underground deposit.',
        'type': IngredientType.neutral.value,
        'rarity': 3,
        'effect': None,
    },
    # 'bone': {
    #     'name': 'Bone',
    #     'description': '',
    #     'type': IngredientType.neutral.value,
    #     'rarity': Rarity.mythic.value?,
    #     'effect': None,
    # },
}
