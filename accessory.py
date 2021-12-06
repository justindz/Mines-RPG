from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class Accessory(MongoModel):
    name = fields.CharField(primary_key=True, required=True)
    description = fields.CharField(required=True)
    level = fields.IntegerField(required=True)
    rarity = fields.IntegerField(required=True)
    weight = fields.IntegerField(required=True)
    itype = fields.IntegerField(required=True)
    bonus_strength = fields.IntegerField(required=True, default=0)
    bonus_intelligence = fields.IntegerField(required=True, default=0)
    bonus_dexterity = fields.IntegerField(required=True, default=0)
    bonus_willpower = fields.IntegerField(required=True, default=0)
    bonus_health = fields.IntegerField(required=True, default=0)
    bonus_health_regen = fields.IntegerField(required=True, default=0)
    bonus_stamina = fields.IntegerField(required=True, default=0)
    bonus_stamina_regen = fields.IntegerField(required=True, default=0)
    bonus_mana = fields.IntegerField(required=True, default=0)
    bonus_mana_regen = fields.IntegerField(required=True, default=0)
    bonus_init = fields.IntegerField(required=True, default=0)
    bonus_carry = fields.IntegerField(required=True, default=0)
    bonus_dot_res = fields.FloatField(required=True, default=0.0)
    bonus_dot_reduction = fields.IntegerField(required=True, default=0)
    bonus_dot_effect = fields.FloatField(required=True, default=0.0)
    bonus_dot_duration = fields.IntegerField(required=True, default=0)
    bonus_shock_limit = fields.IntegerField(required=True, default=0)
    bonus_confusion_limit = fields.IntegerField(required=True, default=0)
    value = fields.IntegerField(required=True, default=0)
    required_strength = fields.IntegerField(required=True, default=0)
    required_intelligence = fields.IntegerField(required=True, default=0)
    required_dexterity = fields.IntegerField(required=True, default=0)
    required_willpower = fields.IntegerField(required=True, default=0)

    class Meta:
        write_concern = WriteConcern(j=True)


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
    display_string += f'\nDamage Over Time Strength {item["bonus_dot_effect"]:+.0%}' if item['bonus_dot_effect'] != 0.0 else ''
    display_string += f'\nDamage Over Time Duration {item["bonus_dot_duration"]:+.0%}' if item['bonus_dot_duration'] != 0 else ''
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
    'Severe': {
        1: {'effect': 'bonus_dot_effect', 'value': 0.1}
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
    'Persistent': {
        1: {'effect': 'bonus_dot_duration', 'value': 1}
    },
    'Grounded': {
        1: {'effect': 'bonus_shock_limit', 'value': 1}
    },
    'Centered': {
        1: {'effect': 'bonus_confusion_limit', 'value': 1}
    },
}
