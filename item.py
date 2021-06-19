import random
from enum import Enum
from mongokit_ng import RequireFieldError

from armor import armors
from consumable import consumables
from weapon import weapons


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


def generate_item(connection, key: str, selection: dict, rarities=None, lucky=False):
    if rarities is None:
        rarities = ['c', 'u', 'r']
    elif not isinstance(rarities, list):
        raise Exception('generate_item rarities parameter must be a list of rarity characters: c, u, r')

    try:
        base = selection[key]

        if selection == weapons:
            item = connection.Weapon()
        elif selection == consumables:
            item = connection.Consumable()
        else:
            item = connection.Armor()
    except KeyError:
        return None

    for k, v in base.items():
        item[k] = v

    # randomly select rarity from [rarities] and then apply affixes accordingly

    try:
        item.save()
        return item
    except RequireFieldError:
        print(f'generate_item failed on required fields for key: {key}')
        return None


def generate_random_item(connection, level: int, item_type=None, rarities=None, lucky=False):
    selection = weapons
    lvl_check = [level - 1, level, level + 1]

    if not lucky:
        lvl_check.append(level - 2)

    if item_type is None:
        selection = random.choice([armors, consumables, weapons])
    else:
        if item_type == ItemType.weapon:
            selection = weapons
        elif item_type in [ItemType.potion, ItemType.food]:
            selection = consumables
        elif item_type in [ItemType.head, ItemType.chest, ItemType.gloves, ItemType.belt, ItemType.boots,
                           ItemType.amulet, ItemType.ring]:
            selection = armors

    candidates = {k: v for k, v in selection.items() if v['level'] in lvl_check}

    if len(candidates) > 0:
        key = random.choice(list(candidates.keys()))
        return generate_item(connection, key, selection, rarities=rarities, lucky=lucky)

    return None
