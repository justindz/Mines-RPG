import random

from items import accessory, weapon, armor, gemstone, ingredient
from item_specs.accessories import accessories
from item_specs.armors import armors
from items.book import Book
from item_specs.books import books
from item_specs.gemstones import gemstones
from item_specs.ingredients import ingredients
from items.item import Rarity, ItemType
from item_specs.weapons import weapons


def generate_item(key: str, selection: dict, level: int, rarity=None, lucky=False):
    value = 0

    try:
        base = selection[key]
        base['level'] = level

        if selection == weapons:
            item = weapon.Weapon()
            item.sockets = [None, None, None]
            value += 5 * base['level']
        elif selection == accessories:
            item = accessory.Accessory()
            value += 5 * base['level']
        else:
            item = armor.Armor()
            item.sockets = [None, None, None]
            value += 5 * base['level']
    except KeyError:
        print(f'generate_item failed on KeyError for key: {key}')
        return None

    for k, v in base.items():
        setattr(item, k, v)

    if rarity is None:
        roll = random.randint(1, 100)

        if roll > 95:
            rarity = Rarity.rare
            item.rarity = Rarity.rare.value
        elif roll > 70:
            rarity = Rarity.uncommon
            item.rarity = Rarity.uncommon.value
        else:
            rarity = Rarity.common
            item.rarity = Rarity.common.value
    else:
        item.rarity = rarity.value

    if rarity == Rarity.rare:
        value += 10 * item.level
    elif rarity == rarity.uncommon:
        value += 5 * item.level

    item.value = value

    if rarity in [Rarity.uncommon, Rarity.rare]:
        if selection == weapons:
            prefixes = weapon.prefixes
            suffixes = weapon.suffixes
        elif selection == accessories:
            prefixes = accessory.prefixes
            suffixes = accessory.suffixes
        else:
            prefixes = armor.prefixes
            suffixes = armor.suffixes

        if rarity == Rarity.rare:
            key = random.choice(list(suffixes.keys()))
            item = add_affix(item, key, suffixes[key], level)

        key = random.choice(list(prefixes.keys()))
        item = add_affix(item, key, prefixes[key], level)

    # item.save()
    return item


def generate_random_item(level: int, item_type=None, rarity=None, lucky=False):
    selection = weapons
    lvl_check = [level - 1, level, level + 1]

    if item_type is None:
        selection = random.choice([armors, weapons, gemstones, ingredients])

        if selection == gemstones:
            return gemstone.get_random_gemstone(random.choice(lvl_check))
        elif selection == ingredients:
            return ingredient.get_random_ingredient(random.choice(lvl_check),
                                                    rarity=(1 if rarity is None else rarity.value))
    else:
        if item_type == ItemType.weapon:
            selection = weapons
        elif item_type in [ItemType.amulet, ItemType.ring, ItemType.belt]:
            selection = accessories
        elif item_type in [ItemType.head, ItemType.chest, ItemType.gloves, ItemType.boots]:
            selection = armors
        elif item_type == ItemType.gemstone:
            return gemstone.get_random_gemstone(random.choice(lvl_check))

    candidates = {k: v for k, v in selection.items() if v['level'] in lvl_check}

    if len(candidates) > 0:
        key = random.choice(list(candidates.keys()))
        return generate_item(key, selection, level, rarity=rarity, lucky=lucky)
    else:
        print(f'Random item generation for {item_type} at rarity {rarity} and level {level} found zero candidates.')

    return None


def generate_book(key: str, rarity=None, lucky=False):
    value = 0

    try:
        base = books[key]
        item = Book()
        value += 10 * base['level']

        for k, v in base.items():
            setattr(item, k, v)

        if rarity is None:
            roll = random.randint(1, 100)

            if roll > 95:
                rarity = Rarity.rare
                item.rarity = Rarity.rare.value
            elif roll > 70:
                rarity = Rarity.uncommon
                item.rarity = Rarity.uncommon.value
            else:
                rarity = Rarity.common
                item.rarity = Rarity.common.value
        else:
            item.rarity = rarity.value

        if rarity == Rarity.rare:
            value += 10 * item.level
        elif rarity == rarity.uncommon:
            value += 5 * item.level

        item.value = value
        # item.save()
        return item
    except KeyError:
        print(f'generate_book failed on KeyError for key: {key}')
        return None


def generate_random_book(level: int, rarity=None, lucky=False):
    lvl_check = [level - 1, level, level + 1]

    if not lucky:
        lvl_check.append(level - 2)

    candidates = {k: v for k, v in books.items() if v['level'] in lvl_check}

    if len(candidates) > 0:
        key = random.choice(list(candidates.keys()))
        return generate_book(key, rarity=rarity, lucky=lucky)
    else:
        print(f'Random book generation at rarity {rarity} and level {level} found zero candidates.')

    return None


def add_affix(item, name, affix, level):
    while True:
        try:
            affix = affix[level]
            break
        except KeyError:
            print(f'No {level} affix tier for {name}, trying {level - 1} next...')
            level -= 1

    item.name = f'{name} {item.name}'

    if affix['effect'] in dir(item):
        print(f'Applying base stat affix {name} to {item.name}')
        # item[affix['effect']] += affix['value']
        setattr(item, affix['effect'], getattr(item, affix['effect'] + affix['value']))
    elif affix['effect'] == 'damage_convert':
        item.damages[0][2] = affix['value']
    elif affix['effect'] == 'dice_added':
        item.damages[0][0] += affix['value']
    elif affix['effect'] == 'damage_mode':
        item.damages.append(affix['value'])
    elif affix['effect'] == 'damage_narrow':
        item.damages[0][0] *= 2
        item.damages[0][1] = round(item.damages[0][1] / 2)
    elif affix['effect'] == 'damage_spread':
        item.damages[0][0] = round(item.damages[0][0] / 2)
        item.damages[0][1] *= 2
    elif affix['effect'] == 'socket':
        item.sockets.append(None)
    else:
        print(f'Unknown affix {name} with effect {affix["effect"]} attempted to add to item {item.name}')

    return item


def socket_gemstone(item, gemstone):
    i = 0

    for socket in item.sockets:
        if socket is not None:
            i += 1
        else:
            item.sockets[i] = gemstone['name']
            setattr(item, gemstone['effect'], getattr(item, gemstone['effect'] + gemstone['amount']))
            return True

    return False
