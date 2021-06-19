from mongokit_ng import Document


class Armor(Document):
    __database__ = 'delverpg'
    __collection__ = 'armor'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'weight': int,
        '_itype': int,
        'bonus_strength': int,
        'bonus_intelligence': int,
        'bonus_dexterity': int,
        'bonus_willpower': int,
        'bonus_health': int,
        'bonus_stamina': int,
        'bonus_mana': int,
        'bonus_init': int,
        'bonus_carry': int,
        'earth_res': float,
        'fire_res': float,
        'electricity_res': float,
        'water_res': float,
    }
    required_fields = ['name', 'description', 'level', 'weight', '_itype', 'bonus_strength', 'bonus_intelligence',
                       'bonus_dexterity', 'bonus_willpower', 'bonus_health', 'bonus_stamina', 'bonus_mana',
                       'bonus_init', 'bonus_carry', 'earth_res', 'fire_res', 'electricity_res', 'water_res']
    use_dot_notation = True
    use_autorefs = True


def get_bonuses_display_string(item):
    display_string = ''

    if item['bonus_strength'] != 0:
        display_string += '\nStrength {:+}'.format(item['bonus_strength'])
    if item['bonus_intelligence'] != 0:
        display_string += '\nIntelligence {:+}'.format(item['bonus_intelligence'])
    if item['bonus_dexterity'] != 0:
        display_string += '\nDexterity {:+}'.format(item['bonus_dexterity'])
    if item['bonus_willpower'] != 0:
        display_string += '\nWillpower {:+}'.format(item['bonus_willpower'])
    if item['bonus_health'] != 0:
        display_string += '\nHealth {:+}'.format(item['bonus_health'])
    if item['bonus_stamina'] != 0:
        display_string += '\nStamina {:+}'.format(item['bonus_stamina'])
    if item['bonus_mana'] != 0:
        display_string += '\nMana {:+}'.format(item['bonus_mana'])
    if item['bonus_init'] != 0:
        display_string += '\nInitiative {:+}'.format(item['bonus_init'])
    if item['bonus_carry'] != 0:
        display_string += '\nCarry {:+}'.format(item['bonus_carry'])
    if item['earth_res'] != 0.0:
        display_string += '\nEarth Res {:+}'.format(item['earth_res'])
    if item['fire_res'] != 0.0:
        display_string += '\nFire Res {:+}'.format(item['fire_res'])
    if item['electricity_res'] != 0.0:
        display_string += '\nElectricity Res {:+}'.format(item['electricity_res'])
    if item['water_res'] != 0.0:
        display_string += '\nWater Res {:+}'.format(item['water_res'])

    return display_string


armors = {
    'test_helmet': {'name': 'RND Helmet', 'description': 'Shite.', 'level': 1, 'weight': 2, '_itype': 2,
                    'bonus_strength': 1, 'bonus_intelligence': 0, 'bonus_dexterity': 0, 'bonus_willpower': 0,
                    'bonus_health': 0, 'bonus_stamina': 0, 'bonus_mana': 0, 'bonus_init': 1, 'bonus_carry': 0,
                    'earth_res': 0.0, 'fire_res': 0.0, 'electricity_res': 0.0, 'water_res': 0.0}
}

prefixes = {}

suffixes = {}
