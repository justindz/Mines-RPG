from mongokit_ng import Document

from item import ItemType


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
    default_values = {
        'name': 'Test Potion (Pico)',
        'description': 'A phial containing a foul-tasting liquid. 1 use remains.',
        'level': 1,
        'weight': 1,
        '_itype': ItemType.potion.value,
        'uses': 1,
        'health': 0,
        'stamina': 0,
        'mana': 5,
    }
    use_dot_notation = True
    use_autorefs = True
