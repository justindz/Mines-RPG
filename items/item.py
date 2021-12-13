from enum import Enum
from pymodm import EmbeddedMongoModel, fields
from pymongo import WriteConcern


class Item(EmbeddedMongoModel):
    name = fields.CharField(required=True)
    description = fields.CharField(required=True)
    level = fields.IntegerField(required=True)
    rarity = fields.IntegerField(required=True)
    weight = fields.IntegerField(required=True)
    itype = fields.IntegerField(required=True)
    value = fields.IntegerField(required=True)

    class Meta:
        write_concern = WriteConcern(j=True)


class ItemType(Enum):
    weapon = 1
    head = 2
    chest = 3
    belt = 4
    boots = 5
    gloves = 6
    amulet = 7
    ring = 8
    potion = 9
    book = 10
    gemstone = 11
    ingredient = 12


class Rarity(Enum):
    common = 1
    uncommon = 2
    rare = 3
