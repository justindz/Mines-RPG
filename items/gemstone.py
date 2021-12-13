import random
from items.item import Item
from pymodm import fields

import utilities
from item_specs.gemstones import gemstones


class Gemstone(Item):
    itype = fields.IntegerField(required=True, default=11)
    effect = fields.CharField(required=True)
    amount = fields.MongoBaseField(required=True)


def get_gemstone(key: str, level: int) -> Gemstone:
    level = utilities.clamp(level, 1, 9) - 1
    base = gemstones[key]
    gemstone = Gemstone()
    gemstone.name = base['name'] + f' {base["tiers"][level]["name"]}'
    gemstone.description = base['description']
    gemstone.level = level + 1
    gemstone.effect = base['effect']
    gemstone.amount = base['tiers'][level]['amount']
    gemstone.weight = 1
    return gemstone


def get_random_gemstone(level: int) -> Gemstone:
    chance = random.random()

    if chance <= 0.1:
        g = get_gemstone(random.choice(['emerald', 'ruby', 'topaz', 'sapphire', 'diamond']), level)
        g.rarity = 3
        g.value = g.level * 3 + (g.level * 10)
    elif chance <= 0.3:
        g = get_gemstone(random.choice(['quartz', 'beryl', 'opal', 'sunstone', 'serpentine', 'fire_agate', 'zircon',
                                        'fluorite']), level)
        g.rarity = 2
        g.value = g.level * 3 + (g.level * 5)
    else:
        g = get_gemstone(random.choice([
            'tourmaline', 'garnet', 'citrine', 'lapis', 'marble', 'obsidian', 'amethyst', 'hematite', 'moonstone']),
            level)
        g.rarity = 1
        g.value = g.level * 3

    return g


def usable_in(gemstone, item) -> bool:
    if gemstone['effect'] in [
        'bonus_strength',
        'bonus_intelligence',
        'bonus_dexterity',
        'bonus_willpower',
        'bonus_health',
        'bonus_stamina',
        'bonus_mana',
        'bonus_init',
    ]:
        return True
    elif gemstone['effect'] in [
        'base_crit_chance',
        'crit_damage',
        'earth_penetration',
        'fire_penetration',
        'electricity_penetration',
        'water_penetration',
    ] and item['itype'] == 1:
        return True
    elif gemstone['effect'] in [
        'bonus_health_regen',
        'bonus_stamina_regen',
        'bonus_mana_regen',
        'bonus_carry',
        'bonus_earth_res',
        'bonus_fire_res',
        'bonus_electricity_res',
        'bonus_water_res',
    ] and item['itype'] in [2, 3, 5, 6]:
        return True

    return False
