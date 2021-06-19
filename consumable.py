from mongokit_ng import Document


class Consumable(Document):
    __database__ = 'delverpg'
    __collection__ = 'consumables'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'weight': int,
        '_itype': int,
        'uses': int,
        'health': int,
        'stamina': int,
        'mana': int,
    }
    required_fields = ['name', 'description', 'level', 'weight', '_itype', 'uses', 'health', 'stamina', 'mana']
    use_dot_notation = True
    use_autorefs = True


consumables = {
    'test_potion': {'name': 'RND Potion', 'description': 'Shite.', 'level': 1, 'weight': 1,
                    '_itype': 10, 'uses': 1, 'health': 0, 'stamina': 0, 'mana': 5}
}

prefixes = {}

suffixes = {}
