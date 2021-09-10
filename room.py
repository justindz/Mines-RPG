class Room(object):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.encounter = None


rooms = {
    'basic': {
        1: [
            Room('Boon Mine (aka, Tutorial)', 'Welcome to Boon Mine. Most rooms contain enemies that must be defeated before you can \\proceed further into the mine. They will attack automatically upon entering the room, after a brief delay.'),
            Room('Another Fight', 'As you delve deeper, you will encounter increasingly challenging enemies, but also higher value rewards. Use \\depth to check your current depth level in the mine.'),
            Room('More Commands', 'Unless you are in a fight, you can \\exit the mine at any point if you are low on time, or low on health and at risk of dying. You will be able to re-enter near the maximum depth you have achieved. You can also use \\look to re-display the current room description.'),
            Room('Partying', 'You can form a party with up to two other players. This will increase the difficulty of fights proportionally.'),
            Room('Loot', 'Every five* depth tiers you reach in a mine will reward the party with loot. While inside a mine, but not fighting, you can change around your equipment. If you found an upgrade, now might be the time to equip it!'),
            Room('Leveling Up', 'You may have noticed in the last room that you gained a level. Unlike many RPGs which award xp for fights, in DelveRPG, levels are achieved by reaching specific depths in any mine, either solo or in a party. Use the \\level command after the fight to claim your level up reward.'),
            Room('Death', 'Should you die during a delve, your character will survive, but your equipped gear and inventory will be lost. The delve will end automatically when the last party member dies.'),
            Room('Professions', 'Upon completing this mine, you will be able to select a profession at the workshop. You can ask the proprietor about \\professions for more info.'),
            Room('Maps', 'In your journey, you may acquire maps. These allow you to enter specific mines, including some not accessible from the encampment. They also apply modifiers which change the risk/reward of the delve.'),
            Room('Congratulations', 'Reaching this depth means you have successfully completed Boon Mine. In addition to the knowledge, levels, and loot you have gained, reaching this point unlocks new mines for you to explore. You are free to repeat Boon Mine as many times as you like, but you will not gain further levels here.'),
        ],
    },


    'infernal': {
        1: [
            Room('Lava Tubes', 'You find yourself traveling through a braided maze of interconnected lava tubes. The roughly circular tunnels are uncomfortably warm to the touch. Step marks, lava pillars, and lavacicles hint at the violent origins of these pathways.'),
            Room('Magma Pools', 'The floor of this stone chamber is pocked with open pools of bubbling magma, giving off a heat-distorted glow and casting shadows across the rough walls. The oppresively hot air reeks of sulphur.'),
            Room('Disturbing Cavern', 'Large pillars of stone in this cavern take on disturbing, sculptural shapes. They dance on the edge between intentionally carved and suggestively natural. An unnatural wind blows through the cavern, causing the pillars wail.'),
            Room('Stalagmite Field', 'Your path opens into a high-valuted stone chamber, riddled with sharp stalagmites. Several of the stone protrusions are stained a dark red color, and the floor is littered with rusted and broken manacles.'),
            Room('Precarious Stone Bridge', 'Rivulets of lava pour from the high walls of this vast cavern into a chasm of receding darkness. A precariously narrow, natural stone bridge crosses to a small opening in the far wall.'),
            Room('Boiling Lake', 'Water flows from various cracks in the stone walls into this cavern, forming an underground lake. The ground is hot to the touch and the lake boils, filling the cavern with steam.'),
            Room('Forgotten Amphitheater', 'Ancient and worn carved benches of stone descend in a semi-circle towards a raised platform littered with rubble.'),
        ],
        21: [
            Room('Obsidian Staircase', 'A steep, glossy black stone staircase decends further into the depths. Jagged spikes of obsidian punctuate the surface, and the overall effect on your flickering torchlight is disorienting.'),
            Room('Torture Chamber', 'You stumble into a torch-lit room whose purpose does not take much effort to grasp. The floor is stained in dried blood and decayed guts, and the room is filled with tools and machines of torture. Some, you cannot even imagine how they work, and on what creatures.'),
        ],
    },
}
