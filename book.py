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
    required_fields = ['name', 'description', 'level', 'rarity', 'weight', '_itype', 'btype', 'key', 'value']
    use_dot_notation = True
    use_autorefs = True


def get_ability_string(item) -> str:
    if item['btype'] == 0:
        return f'skill-{item["key"]}'
    else:
        return f'spell-{item["key"]}'


books = {
    'mend_wounds': {'name': 'Tome: Mend Wounds', 'description': 'Shite.', 'level': 1, 'rarity': 1,
                    'weight': 1, '_itype': 11, 'btype': 1, 'key': 'mend_wounds'},
}
