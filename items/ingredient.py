import random
from items.item import Item
from pymodm import fields

import utilities
from item_specs.ingredients import ingredients
from prefixes import level_prefixes


class Ingredient(Item):
    level = fields.IntegerField(required=True, default=1)
    weight = fields.IntegerField(required=True, default=1)
    itype = fields.IntegerField(required=True, default=12)
    value = fields.IntegerField(required=True, default=1)
    effect = fields.MongoBaseField(required=True, blank=True)


def get_ingredient(key: str, level: int) -> Ingredient:
    result = Ingredient()
    result.level = min(level, 1)

    for k, v in ingredients[key].items():
        setattr(result, k, v)

    result.name = f'{level_prefixes[utilities.clamp(level, 1, 17)]} {result.name}'
    return result


def get_random_ingredient(level: int, rarity=1):
    candidates = {k: v for k, v in ingredients.items() if v['rarity'] == rarity}

    if len(candidates) > 0:
        key = random.choice(list(candidates.keys()))
        return get_ingredient(key, level)
    else:
        print(f'Random ingredient generation at rarity {rarity} and level {level} found zero candidates.')

    return None
