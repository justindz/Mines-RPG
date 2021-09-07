from mongokit_ng import Document


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
        'health': 0,
        'stamina': 0,
        'mana': 0,
        'burn': 0,
        'bleed': 0,
        'shock': 0,
        'confusion': 0,
        'weight': 1,
    }
    use_dot_notation = True
    use_autorefs = True


consumables = {
    'pico_potion': {
        'name': 'Pico Potion',
        'description': 'TODO',
        'level': 1,
        '_itype': 10,
        'uses': 1,
        'mana': 10
    },
    'moldy_hardtack': {
        'name': 'Moldy Hardtack',
        'description': 'TODO',
        'level': 1,
        '_itype': 9,
        'uses': 1,
        'stamina': 10
    },
    'wilted_herbs': {
        'name': 'Wilted Medicinal Herbs',
        'description': 'TODO',
        'level': 1,
        '_itype': 9,
        'uses': 1,
        'health': 10
    },
    'pico_elixir': {
        'name': 'Pico Elixir',
        'description': 'TODO',
        'level': 1,
        '_itype': 10,
        'uses': 1,
        'health': 5,
        'stamina': 5,
        'mana': 5
    },
    'nano_potion': {
        'name': 'Nano Potion',
        'description': 'TODO',
        'level': 2,
        '_itype': 10,
        'uses': 1,
        'mana': 10
    },
    'hardtack': {
        'name': 'Hardtack',
        'description': 'TODO',
        'level': 2,
        '_itype': 9,
        'uses': 2,
        'stamina': 10
    },
    'bitter_herbs': {
        'name': 'Bitter Medicinal Herbs',
        'description': 'TODO',
        'level': 2,
        '_itype': 9,
        'uses': 2,
        'health': 10
    },
    'nano_elixir': {
        'name': 'Nano Elixir',
        'description': 'TODO',
        'level': 2,
        '_itype': 10,
        'uses': 2,
        'health': 6,
        'stamina': 6,
        'mana': 6
    },
    'smelling_salts': {
        'name': 'Smelling Salts',
        'description': 'TODO',
        'level': 3,
        '_itype': 10,
        'uses': 1,
        'burn': 2,
        'bleed': 2,
        'shock': 2,
        'confusion': 2
    }
}

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
