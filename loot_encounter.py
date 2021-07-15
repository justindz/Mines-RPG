import random
import utilities
from item import generate_random_item, Rarity
from character import Character


class Loot:
    def __init__(self, connection, characters: [Character], depth: int):
        self.connection = connection
        self.characters = characters
        self.description = 'You discover an equipment cache!'
        self.roll_item = generate_random_item(connection, depth, rarity=Rarity.rare)
        self.roll_list = []
        self.has_rolled = []

        for character in self.characters:
            item = generate_random_item(connection, depth, rarity=None)
            character.add_to_inventory(item, True)
            self.description += f'\n {character["name"]} found: {item["name"]} {utilities.get_rarity_symbol(item["rarity"])}'

    def add_to_roll_list(self, name: str):
        if name not in self.has_rolled:
            self.has_rolled.append(name)
            roll = random.randint(1, 100)
            self.roll_list.append((name, roll))
            return roll

        return False

    def choose_winner(self):
        if len(self.roll_list) < 1:
            return None

        winner = sorted(self.roll_list, key=lambda x: x[1], reverse=True)[0][0]
        return winner