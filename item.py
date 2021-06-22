import random
from enum import Enum
from mongokit_ng import RequireFieldError

import armor
import consumable
import weapon
from armor import armors
from consumable import consumables
from weapon import weapons
from elements import Elements


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


class Rarity(Enum):
    common = 1
    uncommon = 2
    rare = 3


def generate_item(connection, key: str, selection: dict, rarity=None, lucky=False):
    value = 0

    try:
        base = selection[key]

        if selection == weapons:
            item = connection.Weapon()
            value += 5 * base['level']
        elif selection == consumables:
            item = connection.Consumable()
            value += 1 * base['level']
        else:
            item = connection.Armor()
            value += 5 * base['level']
    except KeyError:
        print(f'generate_item failed on KeyError for key: {key}')
        return None

    for k, v in base.items():
        item[k] = v

    if rarity is None:
        roll = random.randint(1, 100)

        if roll > 95:
            rarity = Rarity.rare
            item['rarity'] = Rarity.rare.value
        elif roll > 70:
            rarity = Rarity.uncommon
            item['rarity'] = Rarity.uncommon.value
        else:
            rarity = Rarity.common
            item['rarity'] = Rarity.common.value
    else:
        item['rarity'] = rarity.value

    if rarity == Rarity.rare:
        value += 10 * item['level']
    elif rarity == rarity.uncommon:
        value += 5 * item['level']

    item['value'] = value

    if rarity in [Rarity.uncommon, Rarity.rare]:
        if selection == weapons:
            prefixes = weapon.prefixes
            suffixes = weapon.suffixes
        elif selection == consumables:
            prefixes = consumable.prefixes
            suffixes = consumable.suffixes
        else:
            prefixes = armor.prefixes
            suffixes = armor.suffixes

        if rarity == Rarity.rare:
            key = random.choice(list(suffixes.keys()))
            item = add_affix(item, key, suffixes[key])

        key = random.choice(list(prefixes.keys()))
        item = add_affix(item, key, prefixes[key])

    try:
        item.save()
        return item
    except RequireFieldError:
        print(f'generate_item failed on RequireFieldError for key: {key}')
        return None


def generate_random_item(connection, level: int, item_type=None, rarity=None, lucky=False):
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
        return generate_item(connection, key, selection, rarity=rarity, lucky=lucky)
    else:
        print(f'Random item generation for {item_type} at rarity {rarity} and level {level} found zero candidates.')

    return None


def add_affix(item, name, affix):
    affix = affix[1]  # TODO select the appropriate tier based on depth level

    item['name'] = f'{name} {item["name"]}'

    if affix['effect'] in item.keys():
        print(f'Applying base stat affix {name} to {item["name"]}')
        item[affix['effect']] += affix['value']
    elif affix['effect'] == 'damage_convert':
        item['damages'][0][2] = affix['value']
    elif affix['effect'] == 'damage_added':
        added_min = int(affix['value'] * float(item['damages'][0][0]))
        added_max = int(affix['value'] * float(item['damages'][0][1]))
        item['damages'][0][0] += added_min
        item['damages'][0][1] += added_max
    elif affix['effect'] == 'damage_mode':
        item['damages'].append(affix['value'])
    elif affix['effect'] == 'damage_narrow':
        from_max = int(affix['value'] * float(item['damages'][0][1]))
        from_max = max(from_max, 1)
        item['damages'][0][0] += from_max
        item['damages'][0][1] -= from_max
        item['damages'][0][1] = max(item['damages'][0][1], item['damages'][0][0])
    elif affix['effect'] == 'damage_spread':
        from_min = int(affix['value'] * float(item['damages'][0][0]))
        from_min = max(from_min, 1)
        item['damages'][0][0] -= from_min
        item['damages'][0][1] += from_min
        item['damages'][0][0] = max(item['damages'][0][0], 1)
    else:
        print(f'Unknown affix {name} with effect {affix["effect"]} attempted to add to item {item["name"]}')

    return item
