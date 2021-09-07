from mongokit_ng import Document


class Book(Document):
    __database__ = 'delverpg'
    __collection__ = 'books'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'rarity': int,
        'weight': int,
        '_itype': int,
        'btype': int,  # 0 = Skill Manual, 1 = Spell Tome
        'key': str,
        'value': int,
    }
    required_fields = [
        'name',
        'description',
        'level',
        'rarity',
        'weight',
        '_itype',
        'btype',
        'key',
        'value'
    ]
    default_values = {
        'weight': 1,
        '_itype': 11,
    }
    use_dot_notation = True
    use_autorefs = True


def get_ability_string(item) -> str:
    if item['btype'] == 0:
        return f'skill-{item["key"]}'
    else:
        return f'spell-{item["key"]}'


books = {
    # Spells
    # L1
    'stalagmite': {
        'name': 'Tome: Stalagmite',
        'description': 'TODO',
        'level': 1,
        'rarity': 2,
        'btype': 1,
        'key': 'stalagmite'
    },
    'mend_wounds': {
        'name': 'Tome: Mend Wounds',
        'description': 'TODO',
        'level': 1,
        'rarity': 1,
        'btype': 1,
        'key': 'mend_wounds'
    },
    'regenerate': {
        'name': 'Tome: Regenerate',
        'description': 'TODO',
        'level': 1,
        'rarity': 2,
        'btype': 1,
        'key': 'regenerate'
    },
    'ignite': {
        'name': 'Tome: Ignite',
        'description': 'TODO',
        'level': 1,
        'rarity': 3,
        'btype': 1,
        'key': 'ignite'
    },
    'summon_coal_golem': {
        'name': 'Tome: Summon Coal Golem',
        'description': 'TODO',
        'level': 1,
        'rarity': 3,
        'btype': 1,
        'key': 'summon_coal_golem'
    },
    # L2
    'slow': {
        'name': 'Tome: Slow',
        'description': 'TODO',
        'level': 2,
        'rarity': 1,
        'btype': 1,
        'key': 'slow'
    },
    'haste': {
        'name': 'Tome: Haste',
        'description': 'TODO',
        'level': 2,
        'rarity': 1,
        'btype': 1,
        'key': 'haste'
    },
    'weaken': {
        'name': 'Tome: Weaken',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'weaken'
    },
    'stupefy': {
        'name': 'Tome: Stupefy',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'stupefy'
    },
    'exhaust': {
        'name': 'Tome: Exhaust',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'exhaust'
    },
    'discourage': {
        'name': 'Tome: Discourage',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'discourage'
    },
    'empower': {
        'name': 'Tome: Empower',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'empower'
    },
    'enlighten': {
        'name': 'Tome: Enlighten',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'enlighten'
    },
    'unleash': {
        'name': 'Tome: Unleash',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'unleash'
    },
    'inspire': {
        'name': 'Tome: Inspire',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'btype': 1,
        'key': 'inspire'
    },
    # Skills
    # L1
    'slash': {
        'name': 'Manual: Slash',
        'description': 'TODO',
        'level': 1,
        'rarity': 2,
        'bytpe': 0,
        'key': 'slash'
    },
    'lacerate': {
        'name': 'Manual: Lacerate',
        'description': 'TODO',
        'level': 1,
        'rarity': 3,
        'bytpe': 0,
        'key': 'lacerate'
    },
    # L2
    'jinx': {
        'name': 'Manual: Jinx',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'bytpe': 0,
        'key': 'jinx'
    },
    'volley': {
        'name': 'Manual: Volley',
        'description': 'TODO',
        'level': 2,
        'rarity': 2,
        'bytpe': 0,
        'key': 'volley'
    },
    'barrage': {
        'name': 'Manual: Barrage',
        'description': 'TODO',
        'level': 2,
        'rarity': 3,
        'bytpe': 0,
        'key': 'barrage'
    },
    'flurry': {
        'name': 'Manual: Flurry',
        'description': 'TODO',
        'level': 2,
        'rarity': 3,
        'bytpe': 0,
        'key': 'flurry'
    },
}
