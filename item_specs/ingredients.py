from enum import Enum


class IngredientType(Enum):
    moss = 1  # Health
    fungi = 2  # Stamina
    algae = 3  # Mana
    guano = 4  # Status
    neutral = 5  # Rarity


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