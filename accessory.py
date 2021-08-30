from mongokit_ng import Document


class Accessory(Document):
    __database__ = 'delverpg'
    __collection__ = 'accessory'
    structure = {
        'name': str,
        'description': str,
        'level': int,
        'rarity': int,
        'weight': int,
        '_itype': int,
        'bonus_strength': int,
        'bonus_intelligence': int,
        'bonus_dexterity': int,
        'bonus_willpower': int,
        'bonus_health': int,
        'bonus_health_regen': int,
        'bonus_stamina': int,
        'bonus_stamina_regen': int,
        'bonus_mana': int,
        'bonus_mana_regen': int,
        'bonus_init': int,
        'bonus_carry': int,
        'bonus_dot_res': float,
        'bonus_dot_reduction': int,
        'value': int,
        'required_strength': int,
        'required_intelligence': int,
        'required_dexterity': int,
        'required_willpower': int,
    }
    required_fields = [
        'name',
        'description',
        'level',
        'rarity',
        'weight',
        '_itype',
        'bonus_strength',
        'bonus_intelligence',
        'bonus_dexterity',
        'bonus_willpower',
        'bonus_health',
        'bonus_health_regen',
        'bonus_stamina',
        'bonus_stamina_regen',
        'bonus_mana',
        'bonus_mana_regen',
        'bonus_init',
        'bonus_carry',
        'bonus_dot_res',
        'bonus_dot_reduction',
        'value',
        'required_strength',
        'required_intelligence',
        'required_dexterity',
        'required_willpower'
    ]
    use_dot_notation = True
    use_autorefs = True


def get_bonuses_display_string(item):
    display_string = ''
    display_string += f'\nStrength {item["bonus_strength"]:+}' if item['bonus_strength'] != 0 else ''
    display_string += f'\nIntelligence {item["bonus_intelligence"]:+}' if item['bonus_intelligence'] != 0 else ''
    display_string += f'\nDexterity {item["bonus_dexterity"]:+}' if item['bonus_dexterity'] != 0 else ''
    display_string += f'\nWillpower {item["bonus_willpower"]:+}' if item['bonus_willpower'] != 0 else ''
    display_string += f'\nHealth {item["bonus_health"]:+}' if item['bonus_health'] != 0 else ''
    display_string += f'\nHealth Regen {item["bonus_health_regen"]:+}' if item['bonus_health_regen'] != 0 else ''
    display_string += f'\nStamina {item["bonus_stamina"]:+}' if item['bonus_stamina'] != 0 else ''
    display_string += f'\nStamina Regen {item["bonus_stamina_regen"]:+}' if item['bonus_stamina_regen'] != 0 else ''
    display_string += f'\nMana {item["bonus_mana"]:+}' if item['bonus_mana'] != 0 else ''
    display_string += f'\nMana Regen {item["bonus_mana_regen"]:+}' if item['bonus_mana_regen'] != 0 else ''
    display_string += f'\nInitiative {item["bonus_init"]:+}' if item['bonus_init'] != 0 else ''
    display_string += f'\nCarry {item["bonus_carry"]:+}' if item['bonus_carry'] != 0 else ''
    display_string += f'\nDamage Over Time Resistance {item["bonus_dot_res"]:+.0%}' if item['bonus_dot_res'] != 0.0 else ''
    display_string += f'\nDamage Over Time Reduction {item["bonus_dot_reduction"]:+.0%}' if item['bonus_dot_reduction'] != 0 else ''
    return display_string.lstrip('\n')


prefixes = {
    'Streamlined': {
        1: {'effect': 'required_strength', 'value': -1}
    },
    'Striking': {
        1: {'effect': 'required_intelligence', 'value': -1}
    },
    'Fitted': {
        1: {'effect': 'required_dexterity', 'value': -1}
    },
    'Pious': {
        1: {'effect': 'required_willpower', 'value': -1}
    },
    'Collectible': {
        1: {'effect': 'value', 'value': 30}
    },
    'Lightweight': {
        1: {'effect': 'weight', 'value': -1}
    },
    'Empowering': {
        1: {'effect': 'bonus_strength', 'value': 1}
    },
    'Enlightening': {
        1: {'effect': 'bonus_intelligence', 'value': 1}
    },
    'Unleashing': {
        1: {'effect': 'bonus_dexterity', 'value': 1}
    },
    'Inspiring': {
        1: {'effect': 'bonus_willpower', 'value': 1}
    },
    'Modular': {
        1: {'effect': 'bonus_carry', 'value': 5}
    },
    'Heightening': {
        1: {'effect': 'bonus_init', 'value': 1}
    },
    'Hardy': {
        1: {'effect': 'bonus_dot_res', 'value': 0.1}
    },
}

suffixes = {
    'Gilded': {
        1: {'effect': 'value', 'value': 100}
    },
    'Medicinal': {
        1: {'effect': 'bonus_health_regen', 'value': 1}
    },
    'Stimulant': {
        1: {'effect': 'bonus_stamina_regen', 'value': 1}
    },
    'Arcane': {
        1: {'effect': 'bonus_mana_regen', 'value': 1}
    },
    'Resilient': {
        1: {'effect': 'bonus_dot_reduction', 'value': 1}
    },
}
