from item import Item, ItemType


class Consumable(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Test Healing Potion'
        self.weight = 1
        self.type = ItemType.potion
        self.uses = 1
        self.health = 0
        self.stamina = 0
        self.mana = 5

        if self.uses == 1:
            self.description = f'A phial containing a foul-tasting liquid. {self.uses} use remains.'
        else:
            self.description = f'A phial containing a foul-tasting liquid. {self.uses} uses remain.'

        self.name = 'Test Potion (Pico)'
        # TODO Add effects
