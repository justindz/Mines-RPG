from enum import Enum

from item import Item, ItemType
from elements import Elements

valid_slots = ['weapon', 'head', 'chest', 'belt', 'boots', 'gloves', 'amulet', 'ring']


class WeaponType(Enum):
    dagger = 1
    sword = 2
    spear = 3
    axe = 4
    mace = 5
    staff = 6


class Weapon(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Test Sword'
        self.description = 'An RND sword.'
        self.weight = 3
        self.type = ItemType.weapon
        self.weapon_type = WeaponType.sword
        self.bonus_strength = 1
        self.bonus_intelligence = 0
        self.bonus_dexterity = 0
        self.bonus_willpower = 0
        self.bonus_health = 0
        self.bonus_stamina = 0
        self.bonus_mana = 0
        self.bonus_init = 0
        self.base_crit_chance = 0.05
        self.damages = [
            [1, 4, Elements.earth]
        ]

    def get_damages_display_string(self):
        display_string = ''

        for damage in self.damages:
            display_string += '{}-{} {}\n'.format(damage[0], damage[1], damage[2])

        return display_string

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

        return display_string
