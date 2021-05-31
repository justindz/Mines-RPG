from item import Item, ItemType


class Armor(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Test Helmet'
        self.description = 'An RND helmet.'
        self.weight = 2
        self.type = ItemType.head
        self.bonus_strength = 0
        self.bonus_intelligence = 0
        self.bonus_dexterity = 0
        self.bonus_willpower = 0
        self.bonus_health = 0
        self.bonus_stamina = 0
        self.bonus_mana = 0
        self.bonus_init = 1
        self.bonus_carry = 0
        self.earth_res = 0.0
        self.fire_res = 0.0
        self.electricity_res = 0.0
        self.water_res = 0.0

    def get_bonuses_display_string(self):
        display_string = ''

        if self.bonus_strength != 0:
            display_string += '\nStrength {:+}'.format(self.bonus_strength)
        if self.bonus_intelligence != 0:
            display_string += '\nIntelligence {:+}'.format(self.bonus_intelligence)
        if self.bonus_dexterity != 0:
            display_string += '\nDexterity {:+}'.format(self.bonus_dexterity)
        if self.bonus_willpower != 0:
            display_string += '\nWillpower {:+}'.format(self.bonus_willpower)
        if self.bonus_health != 0:
            display_string += '\nHealth {:+}'.format(self.bonus_health)
        if self.bonus_stamina != 0:
            display_string += '\nStamina {:+}'.format(self.bonus_stamina)
        if self.bonus_mana != 0:
            display_string += '\nMana {:+}'.format(self.bonus_mana)
        if self.bonus_init != 0:
            display_string += '\nInitiative {:+}'.format(self.bonus_init)
        if self.bonus_carry != 0:
            display_string += '\nCarry {:+}'.format(self.bonus_carry)
        if self.earth_res != 0.0:
            display_string += '\nEarth Res {:+}'.format(self.earth_res)
        if self.fire_res != 0.0:
            display_string += '\nFire Res {:+}'.format(self.fire_res)
        if self.electricity_res != 0.0:
            display_string += '\nElectricity Res {:+}'.format(self.electricity_res)
        if self.water_res != 0.0:
            display_string += '\nWater Res {:+}'.format(self.water_res)

        return display_string
