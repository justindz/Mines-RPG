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
    'stalagmite': {'name': 'Tome: Stalagmite', 'description': 'TODO', 'level': 1, 'rarity': 2, 'btype': 1,
                   'key': 'stalagmite'},
    'ignite': {'name': 'Tome: Ignite', 'description': 'TODO', 'level': 1, 'rarity': 3, 'btype': 1,
               'key': 'ignite'},
    'mend_wounds': {'name': 'Tome: Mend Wounds', 'description': 'TODO', 'level': 1, 'rarity': 1, 'btype': 1,
                    'key': 'mend_wounds'},
    'regenerate': {'name': 'Tome: Regenerate', 'description': 'TODO', 'level': 1, 'rarity': 2, 'btype': 1,
                   'key': 'regenerate'},
    'summon_coal_golem': {'name': 'Tome: Summon Coal Golem', 'description': 'TODO', 'level': 1, 'rarity': 3, 'btype': 1,
                          'key': 'summon_coal_golem'},
    'slow': {'name': 'Tome: Slow', 'description': 'TODO', 'level': 2, 'rarity': 1, 'btype': 1, 'key': 'slow'},
    'haste': {'name': 'Tome: Haste', 'description': 'TODO', 'level': 2, 'rarity': 1, 'btype': 1, 'key': 'haste'},
    'weaken': {'name': 'Tome: Weaken', 'description': 'TODO', 'level': 2, 'rarity': 2, 'btype': 1, 'key': 'weaken'},
    'stupefy': {'name': 'Tome: Stupefy', 'description': 'TODO', 'level': 2, 'rarity': 2, 'btype': 1, 'key': 'stupefy'},
    'exhaust': {'name': 'Tome: Exhaust', 'description': 'TODO', 'level': 2, 'rarity': 2, 'btype': 1, 'key': 'exhaust'},
    'discourage': {'name': 'Tome: Discourage', 'description': 'TODO', 'level': 2, 'rarity': 2, 'btype': 1,
                   'key': 'discourage'},
    # Skills
    'slash': {'name': 'Manual: Slash', 'description': 'TODO', 'level': 1, 'rarity': 2, 'bytpe': 0, 'key': 'slash'},
    'lacerate': {'name': 'Manual: Lacerate', 'description': 'TODO', 'level': 1, 'rarity': 3, 'bytpe': 0,
                 'key': 'lacerate'},
    'jinx': {'name': 'Manual: Jinx', 'description': 'TODO', 'level': 2, 'rarity': 2, 'bytpe': 0, 'key': 'jinx'},
    'volley': {'name': 'Manual: Volley', 'description': 'TODO', 'level': 2, 'rarity': 2, 'bytpe': 0, 'key': 'volley'},
    'barrage': {'name': 'Manual: Barrage', 'description': 'TODO', 'level': 2, 'rarity': 3, 'bytpe': 0,
                'key': 'barrage'},
    'flurry': {'name': 'Manual: Flurry', 'description': 'TODO', 'level': 2, 'rarity': 3, 'bytpe': 0, 'key': 'flurry'},
}
