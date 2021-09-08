import random
from mongokit_ng import Document

import utilities


class Gemstone(Document):
    __database__ = 'delverpg'
    __collection__ = 'gemstones'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'rarity': int,
        'weight': int,
        '_itype': int,
        'effect': str,
        'amount': None,
        'value': int,
    }
    required_fields = [
        'name',
        'description',
        'level',
        'rarity',
        'weight',
        '_itype',
        'effect',
        'amount',
        'value',
    ]
    default_values = {
        'weight': 1,
        '_itype': 11,
    }
    use_dot_notation = True
    use_autorefs = True


def get_gemstone(connection, key: str, level: int) -> Gemstone:
    level = utilities.clamp(level, 1, 9) - 1
    base = gemstones[key]
    gemstone = connection.Gemstone()
    gemstone.name = base['name'] + f' {base["tiers"][level]["name"]}'
    gemstone.description = base['description']
    gemstone.level = level + 1
    gemstone.effect = base['effect']
    gemstone.amount = base['tiers'][level]['amount']
    return gemstone


def get_random_gemstone(connection, level: int) -> Gemstone:
    chance = random.random()

    if chance <= 0.1:
        g = get_gemstone(connection, random.choice(['emerald', 'ruby', 'topaz', 'sapphire', 'diamond']), level)
        g.rarity = 3
        g.value = g.level * 3 + (g.level * 10)
    elif chance <= 0.3:
        g = get_gemstone(connection, random.choice(['quartz', 'beryl', 'opal', 'sunstone', 'serpentine', 'fire_agate',
                                                    'zircon', 'fluorite']), level)
        g.rarity = 2
        g.value = g.level * 3 + (g.level * 5)
    else:
        g = get_gemstone(connection, random.choice([
            'tourmaline', 'garnet', 'citrine', 'lapis', 'marble', 'obsidian', 'amethyst', 'hematite', 'moonstone']), level)
        g.rarity = 1
        g.value = g.level * 3

    g.save()
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
    ] and item['_itype'] == 1:
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
    ] and item['_itype'] in [2, 3, 5, 6]:
        return True

    return False


gemstones = {
    'tourmaline': {'name': 'Tourmaline',
                   'description': 'A hexagonal piece of translucent green boron silicate.',
                   'effect': 'bonus_strength',
                   'tiers': [
                       {'name': 'Mote', 'amount': 1},
                       {'name': 'Speck', 'amount': 2},
                       {'name': 'Sliver', 'amount': 3},
                       {'name': 'Shard', 'amount': 5},
                       {'name': 'Fragment', 'amount': 8},
                       {'name': 'Round', 'amount': 13},
                       {'name': 'Square', 'amount': 21},
                       {'name': 'Oval', 'amount': 34},
                       {'name': 'Marquise', 'amount': 55},
                   ]},
    'garnet': {'name': 'Garnet',
               'description': 'A cubic piece of translucent dark red almandine.',
               'effect': 'bonus_intelligence',
               'tiers': [
                   {'name': 'Mote', 'amount': 1},
                   {'name': 'Speck', 'amount': 2},
                   {'name': 'Sliver', 'amount': 3},
                   {'name': 'Shard', 'amount': 5},
                   {'name': 'Fragment', 'amount': 8},
                   {'name': 'Round', 'amount': 13},
                   {'name': 'Square', 'amount': 21},
                   {'name': 'Oval', 'amount': 34},
                   {'name': 'Marquise', 'amount': 55},
               ]},
    'citrine': {'name': 'Citrine',
                'description': 'A faceted piece of transparent yellow-orange quartz.',
                'effect': 'bonus_dexterity',
                'tiers': [
                    {'name': 'Mote', 'amount': 1},
                    {'name': 'Speck', 'amount': 2},
                    {'name': 'Sliver', 'amount': 3},
                    {'name': 'Shard', 'amount': 5},
                    {'name': 'Fragment', 'amount': 8},
                    {'name': 'Round', 'amount': 13},
                    {'name': 'Square', 'amount': 21},
                    {'name': 'Oval', 'amount': 34},
                    {'name': 'Marquise', 'amount': 55},
                ]},
    'lapis': {'name': 'Lapis',
              'description': 'A smooth piece of ultramarine blue metamorphic stone.',
              'effect': 'bonus_willpower',
              'tiers': [
                  {'name': 'Mote', 'amount': 1},
                  {'name': 'Speck', 'amount': 2},
                  {'name': 'Sliver', 'amount': 3},
                  {'name': 'Shard', 'amount': 5},
                  {'name': 'Fragment', 'amount': 8},
                  {'name': 'Round', 'amount': 13},
                  {'name': 'Square', 'amount': 21},
                  {'name': 'Oval', 'amount': 34},
                  {'name': 'Marquise', 'amount': 55},
              ]},
    'marble': {'name': 'Marble',
               'description': 'A smooth piece of faceted milky white metamorphic rock.',
               'effect': 'bonus_health',
               'tiers': [
                   {'name': 'Mote', 'amount': 1},
                   {'name': 'Speck', 'amount': 2},
                   {'name': 'Sliver', 'amount': 3},
                   {'name': 'Shard', 'amount': 5},
                   {'name': 'Fragment', 'amount': 8},
                   {'name': 'Round', 'amount': 13},
                   {'name': 'Square', 'amount': 21},
                   {'name': 'Oval', 'amount': 34},
                   {'name': 'Marquise', 'amount': 55},
               ]},
    'obsidian': {'name': 'Obsidian',
                 'description': 'A sharp-edged piece of black volcanic glass with conchoidal fractures.',
                 'effect': 'bonus_stamina',
                 'tiers': [
                     {'name': 'Mote', 'amount': 1},
                     {'name': 'Speck', 'amount': 2},
                     {'name': 'Sliver', 'amount': 3},
                     {'name': 'Shard', 'amount': 5},
                     {'name': 'Fragment', 'amount': 8},
                     {'name': 'Round', 'amount': 13},
                     {'name': 'Square', 'amount': 21},
                     {'name': 'Oval', 'amount': 34},
                     {'name': 'Marquise', 'amount': 55},
                 ]},
    'amethyst': {'name': 'Amethyst',
                 'description': 'A hexagonal piece of translucent deep purple quartz.',
                 'effect': 'bonus_mana',
                 'tiers': [
                     {'name': 'Mote', 'amount': 1},
                     {'name': 'Speck', 'amount': 2},
                     {'name': 'Sliver', 'amount': 3},
                     {'name': 'Shard', 'amount': 5},
                     {'name': 'Fragment', 'amount': 8},
                     {'name': 'Round', 'amount': 13},
                     {'name': 'Square', 'amount': 21},
                     {'name': 'Oval', 'amount': 34},
                     {'name': 'Marquise', 'amount': 55},
                 ]},
    'quartz': {'name': 'Quartz',
               'description': 'A hexagonal piece of translucent white quartz.',
               'effect': 'bonus_health_regen',
               'tiers': [
                   {'name': 'Mote', 'amount': 1},
                   {'name': 'Speck', 'amount': 2},
                   {'name': 'Sliver', 'amount': 3},
                   {'name': 'Shard', 'amount': 4},
                   {'name': 'Fragment', 'amount': 5},
                   {'name': 'Round', 'amount': 6},
                   {'name': 'Square', 'amount': 7},
                   {'name': 'Oval', 'amount': 8},
                   {'name': 'Marquise', 'amount': 9},
               ]},
    'beryl': {'name': 'Beryl',
              'description': 'A hexagonal piece of transparent greenish yellow silicate mineral.',
              'effect': 'bonus_stamina_regen',
              'tiers': [
                  {'name': 'Mote', 'amount': 1},
                  {'name': 'Speck', 'amount': 2},
                  {'name': 'Sliver', 'amount': 3},
                  {'name': 'Shard', 'amount': 4},
                  {'name': 'Fragment', 'amount': 5},
                  {'name': 'Round', 'amount': 6},
                  {'name': 'Square', 'amount': 7},
                  {'name': 'Oval', 'amount': 8},
                  {'name': 'Marquise', 'amount': 9},
              ]},
    'opal': {'name': 'Opal',
             'description': 'A delicate piece of blue and violet crystal mineraloid that plays with the light.',
             'effect': 'bonus_mana_regen',
             'tiers': [
                 {'name': 'Mote', 'amount': 1},
                 {'name': 'Speck', 'amount': 2},
                 {'name': 'Sliver', 'amount': 3},
                 {'name': 'Shard', 'amount': 4},
                 {'name': 'Fragment', 'amount': 5},
                 {'name': 'Round', 'amount': 6},
                 {'name': 'Square', 'amount': 7},
                 {'name': 'Oval', 'amount': 8},
                 {'name': 'Marquise', 'amount': 9},
             ]},
    'hematite': {'name': 'Hematite',
                 'description': 'A metallic piece of opaque black and steel-gray mineral.',
                 'effect': 'bonus_carry',
                 'tiers': [
                     {'name': 'Mote', 'amount': 2},
                     {'name': 'Speck', 'amount': 4},
                     {'name': 'Sliver', 'amount': 8},
                     {'name': 'Shard', 'amount': 16},
                     {'name': 'Fragment', 'amount': 32},
                     {'name': 'Round', 'amount': 64},
                     {'name': 'Square', 'amount': 128},
                     {'name': 'Oval', 'amount': 256},
                     {'name': 'Marquise', 'amount': 512},
                 ]},
    'moonstone': {'name': 'Moonstone',
                  'description': 'A smooth piece of adularescent white feldspar.',
                  'effect': 'bonus_init',
                  'tiers': [
                      {'name': 'Mote', 'amount': 1},
                      {'name': 'Speck', 'amount': 2},
                      {'name': 'Sliver', 'amount': 3},
                      {'name': 'Shard', 'amount': 5},
                      {'name': 'Fragment', 'amount': 8},
                      {'name': 'Round', 'amount': 13},
                      {'name': 'Square', 'amount': 21},
                      {'name': 'Oval', 'amount': 34},
                      {'name': 'Marquise', 'amount': 55},
                  ]},
    'emerald': {'name': 'Emerald',
                'description': 'A hexagonal piece of transparent green precious beryl.',
                'effect': 'bonus_earth_res',
                'tiers': [
                    {'name': 'Mote', 'amount': 0.01},
                    {'name': 'Speck', 'amount': 0.02},
                    {'name': 'Sliver', 'amount': 0.03},
                    {'name': 'Shard', 'amount': 0.04},
                    {'name': 'Fragment', 'amount': 0.05},
                    {'name': 'Round', 'amount': 0.06},
                    {'name': 'Square', 'amount': 0.07},
                    {'name': 'Oval', 'amount': 0.08},
                    {'name': 'Marquise', 'amount': 0.09},
                ]},
    'ruby': {'name': 'Ruby',
             'description': 'A hexagonal piece of striking red corundum.',
             'effect': 'bonus_fire_res',
             'tiers': [
                 {'name': 'Mote', 'amount': 0.01},
                 {'name': 'Speck', 'amount': 0.02},
                 {'name': 'Sliver', 'amount': 0.03},
                 {'name': 'Shard', 'amount': 0.04},
                 {'name': 'Fragment', 'amount': 0.05},
                 {'name': 'Round', 'amount': 0.06},
                 {'name': 'Square', 'amount': 0.07},
                 {'name': 'Oval', 'amount': 0.08},
                 {'name': 'Marquise', 'amount': 0.09},
             ]},
    'topaz': {'name': 'Topaz',
              'description': 'An orthorhombic piece of transparent yellow-orange silicate.',
              'effect': 'bonus_electricity_res',
              'tiers': [
                  {'name': 'Mote', 'amount': 0.01},
                  {'name': 'Speck', 'amount': 0.02},
                  {'name': 'Sliver', 'amount': 0.03},
                  {'name': 'Shard', 'amount': 0.04},
                  {'name': 'Fragment', 'amount': 0.05},
                  {'name': 'Round', 'amount': 0.06},
                  {'name': 'Square', 'amount': 0.07},
                  {'name': 'Oval', 'amount': 0.08},
                  {'name': 'Marquise', 'amount': 0.09},
              ]},
    'sapphire': {'name': 'Sapphire',
                 'description': 'A hexagonal piece of striking blue corundum.',
                 'effect': 'bonus_water_res',
                 'tiers': [
                     {'name': 'Mote', 'amount': 0.01},
                     {'name': 'Speck', 'amount': 0.02},
                     {'name': 'Sliver', 'amount': 0.03},
                     {'name': 'Shard', 'amount': 0.04},
                     {'name': 'Fragment', 'amount': 0.05},
                     {'name': 'Round', 'amount': 0.06},
                     {'name': 'Square', 'amount': 0.07},
                     {'name': 'Oval', 'amount': 0.08},
                     {'name': 'Marquise', 'amount': 0.09},
                 ]},
    'diamond': {'name': 'Diamond',
                'description': 'A crystal of clear, lustrous, transparent carbon.',
                'effect': 'base_crit_chance',
                'tiers': [
                    {'name': 'Mote', 'amount': 0.01},
                    {'name': 'Speck', 'amount': 0.01},
                    {'name': 'Sliver', 'amount': 0.01},
                    {'name': 'Shard', 'amount': 0.02},
                    {'name': 'Fragment', 'amount': 0.02},
                    {'name': 'Round', 'amount': 0.02},
                    {'name': 'Square', 'amount': 0.03},
                    {'name': 'Oval', 'amount': 0.03},
                    {'name': 'Marquise', 'amount': 0.03},
                ]},
    'sunstone': {'name': 'Sunstone',
                 'description': 'A piece of translucent, creamy pink, aventurescent feldspar.',
                 'effect': 'crit_damage',
                 'tiers': [
                     {'name': 'Mote', 'amount': 1},
                     {'name': 'Speck', 'amount': 2},
                     {'name': 'Sliver', 'amount': 3},
                     {'name': 'Shard', 'amount': 5},
                     {'name': 'Fragment', 'amount': 8},
                     {'name': 'Round', 'amount': 13},
                     {'name': 'Square', 'amount': 21},
                     {'name': 'Oval', 'amount': 34},
                     {'name': 'Marquise', 'amount': 55},
                 ]},
    'serpentine': {'name': 'Serpentine',
                   'description': 'A piece of waxy, opaque green silicate.',
                   'effect': 'earth_penetration',
                   'tiers': [
                       {'name': 'Mote', 'amount': 0.01},
                       {'name': 'Speck', 'amount': 0.02},
                       {'name': 'Sliver', 'amount': 0.03},
                       {'name': 'Shard', 'amount': 0.04},
                       {'name': 'Fragment', 'amount': 0.05},
                       {'name': 'Round', 'amount': 0.06},
                       {'name': 'Square', 'amount': 0.07},
                       {'name': 'Oval', 'amount': 0.08},
                       {'name': 'Marquise', 'amount': 0.09},
                   ]},
    'fire_agate': {'name': 'Fire Agate',
                   'description': 'A piece of brown agate containing hemispheres of red, orange, and yellow flash.',
                   'effect': 'fire_penetration',
                   'tiers': [
                       {'name': 'Mote', 'amount': 0.01},
                       {'name': 'Speck', 'amount': 0.02},
                       {'name': 'Sliver', 'amount': 0.03},
                       {'name': 'Shard', 'amount': 0.04},
                       {'name': 'Fragment', 'amount': 0.05},
                       {'name': 'Round', 'amount': 0.06},
                       {'name': 'Square', 'amount': 0.07},
                       {'name': 'Oval', 'amount': 0.08},
                       {'name': 'Marquise', 'amount': 0.09},
                   ]},
    'zircon': {'name': 'Zircon',
               'description': 'A tetragonal piece of golden yellow, translucent silicate.',
               'effect': 'electricity_penetration',
               'tiers': [
                   {'name': 'Mote', 'amount': 0.01},
                   {'name': 'Speck', 'amount': 0.02},
                   {'name': 'Sliver', 'amount': 0.03},
                   {'name': 'Shard', 'amount': 0.04},
                   {'name': 'Fragment', 'amount': 0.05},
                   {'name': 'Round', 'amount': 0.06},
                   {'name': 'Square', 'amount': 0.07},
                   {'name': 'Oval', 'amount': 0.08},
                   {'name': 'Marquise', 'amount': 0.09},
               ]},
    'fluorite': {'name': 'Fluorite',
                 'description': 'A perfectly octohedronal piece of translucent, sky blue halide.',
                 'effect': 'water_penetration',
                 'tiers': [
                     {'name': 'Mote', 'amount': 0.01},
                     {'name': 'Speck', 'amount': 0.02},
                     {'name': 'Sliver', 'amount': 0.03},
                     {'name': 'Shard', 'amount': 0.04},
                     {'name': 'Fragment', 'amount': 0.05},
                     {'name': 'Round', 'amount': 0.06},
                     {'name': 'Square', 'amount': 0.07},
                     {'name': 'Oval', 'amount': 0.08},
                     {'name': 'Marquise', 'amount': 0.09},
                 ]},
}
