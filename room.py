class Room(object):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.encounter = None


rooms = {
    'basic': [
        Room('Boon Mine (aka, Tutorial)', 'Welcome to Boon Mine. Most rooms contain enemies that must be defeated before you can \\proceed further into the mine. They will attack automatically upon entering the room, after a brief delay.'),
        Room('Another Fight', 'As you delve deeper, you will encounter increasingly challenging enemies, but also higher value rewards. Use \\depth to check your current depth level in the mine.'),
        Room('More Commands', 'Unless you are in a fight, you can \\exit the mine at any point if you are low on time, or low on health and at risk of dying. You will be able to re-enter near the maximum depth you have achieved. You can also use \\look to re-display the current room description.'),
        Room('Partying', 'You can form a party with up to two other players. This will increase the difficulty of fights proportionally.'),
        Room('Loot', 'Every five* depth tiers you reach in a mine will reward the party with loot. While inside a mine, but not fighting, you can change around your equipment. If you found an upgrade, now might be the time to equip it!'),
        Room('Leveling Up', 'You may have noticed in the last room that you gained a level. Unlike many RPGs which award xp for fights, in DelveRPG, levels are achieved by reaching specific depths in any mine, either solo or in a party. Use the \\level command after the fight to claim your level up reward.'),
        Room('Death', 'Should you die during a delve, your character will survive, but your equipped gear and inventory will be lost. The delve will end automatically when the last party member dies.'),
        Room('Professions', 'Upon reaching a specific level, you will select a profession. Professions are optional, but can aid in your progression directly or indirectly.'),
        Room('Maps', 'In your journey, you may acquire maps. These allow you to enter specific mines, including some not accessible from the encampment. They also apply modifiers which change the risk/reward of the delve.'),
        Room('Congratulations', 'Reaching this depth means you have successfully completed Boon Mine. In addition to the knowledge, levels, and loot you have gained, reaching this point unlocks new mines for you to explore. You are free to repeat Boon Mine as many times as you like, but you will not gain further levels here.'),
    ],
    'infernal': [
        Room('Infernal Room', 'Description'),
    ]
}
