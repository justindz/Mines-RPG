import random
from enum import Enum
from mongokit_ng import RequireFieldError

import armor
import consumable
import weapon
from armor import armors
from consumable import consumables
from weapon import weapons
from book import books
import dice


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
    book = 11


class Rarity(Enum):
    common = 1
    uncommon = 2
    rare = 3


def generate_item(connection, key: str, selection: dict, level: int, rarity=None, lucky=False):
    value = 0

    try:
        base = selection[key]
        base['level'] = level

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
        if k == 'damages':
            item['damages'] = []

            for _ in v:
                item['damages'].append([dice.count(level), v[1], v[2]])
        else:
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
            item = add_affix(item, key, suffixes[key], level)

        key = random.choice(list(prefixes.keys()))
        item = add_affix(item, key, prefixes[key], level)

    try:
        item.save()
        return item
    except RequireFieldError:
        print(f'generate_item failed on RequireFieldError for key: {key}')
        return None


def generate_random_item(connection, level: int, item_type=None, rarity=None, lucky=False):
    selection = weapons
    lvl_check = [level - 1, level, level + 1]

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
        return generate_item(connection, key, selection, level, rarity=rarity, lucky=lucky)
    else:
        print(f'Random item generation for {item_type} at rarity {rarity} and level {level} found zero candidates.')

    return None


def generate_book(connection, key: str, rarity=None, lucky=False):
    value = 0

    try:
        base = books[key]
        item = connection.Book()
        value += 10 * base['level']

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

        try:
            item.save()
            return item
        except RequireFieldError:
            print(f'generate_item failed on RequireFieldError for key: {key}')
            return None
    except KeyError:
        print(f'generate_book failed on KeyError for key: {key}')
        return None


def generate_random_book(connection, level: int, rarity=None, lucky=False):
    lvl_check = [level - 1, level, level + 1]

    if not lucky:
        lvl_check.append(level - 2)

    candidates = {k: v for k, v in books.items() if v['level'] in lvl_check}

    if len(candidates) > 0:
        key = random.choice(list(candidates.keys()))
        return generate_book(connection, key, rarity=rarity, lucky=lucky)
    else:
        print(f'Random book generation at rarity {rarity} and level {level} found zero candidates.')

    return None


def delete_item(connection, item):
    _id = item['_id']

    if item['_itype'] in [ItemType.head.value, ItemType.boots.value, ItemType.amulet.value, ItemType.belt.value,
                          ItemType.gloves.value, ItemType.chest.value, ItemType.ring.value]:
        connection.delverpg.armor.remove(_id)
    elif item['_itype'] == ItemType.weapon.value:
        connection.delverpg.weapons.remove(_id)
    elif item['_itype'] == ItemType.potion.value or item['_itype'] == ItemType.food.value:
        connection.delverpg.consumables.remove(_id)
    elif item['_itype'] == ItemType.book.value:
        connection.delverpg.books.remove(_id)
    else:
        raise Exception(f'delete_item called on unknown item type {item["_itype"]} w/ id {_id}')


def add_affix(item, name, affix, level):
    while True:
        try:
            affix = affix[level]
            break
        except KeyError:
            print(f'No {level} affix tier for {name}, trying {level - 1} next...')
            level -= 1

    item['name'] = f'{name} {item["name"]}'

    if affix['effect'] in item.keys():
        print(f'Applying base stat affix {name} to {item["name"]}')
        item[affix['effect']] += affix['value']
    elif affix['effect'] == 'damage_convert':
        item['damages'][0][2] = affix['value']
    elif affix['effect'] == 'dice_added':
        item['damages'][0][0] += affix['value']
    elif affix['effect'] == 'damage_mode':
        item['damages'].append(affix['value'])
    elif affix['effect'] == 'damage_narrow':
        item['damages'][0][0] *= 2
        item['damages'][0][1] = round(item['damages'][0][1] / 2)
    elif affix['effect'] == 'damage_spread':
        item['damages'][0][0] = round(item['damages'][0][0] / 2)
        item['damages'][0][1] *= 2
    else:
        print(f'Unknown affix {name} with effect {affix["effect"]} attempted to add to item {item["name"]}')

    return item
