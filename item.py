from enum import Enum


class ItemType(Enum):
    weapon = 1
    head = 2
    chest = 3
    belt = 4
    boots = 5
    gloves = 6
    amulet = 7
    ring = 8
    food = 9
    potion = 10


class Item:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.level = 1
        self.weight = 0
