from items.item import Item
from pymodm import fields


class Book(Item):
    btype = fields.IntegerField(required=True)  # 0 = Skill Manual, 1 = Spell Tome
    key = fields.CharField(required=True)
    value = fields.IntegerField(required=True, default=0)


def get_ability_string(item) -> str:
    if item['btype'] == 0:
        return f'skill-{item["key"]}'
    else:
        return f'spell-{item["key"]}'
