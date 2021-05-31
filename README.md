# Mines-RPG

This project is a working starting point for a Discord bot that operates a text-based, multi-player RPG within a server.

=Getting Started=

1. You need to do Discord stuff to create a bot which is authorized to use your server, which should result in a token. Make sure to give the bot permissions to messages and to channels, as the bot will actually create dynamic channels for party game sessions and remove them on completion.
2. You need to create a secrets.py code file in the top level directory containing two variables:
    client_token = 'Your token here'
    encampment_channel_id = numeric channel id for the "game" channel on your server where the bot will listen for game commands
3. Run bot.py

These instructions are woefully inadequate! They should be improved with a github wiki or something. If you want to see how the bot should work, join: https://discord.gg/aZH68e4 and ask "justindz" to start it up.

=Code Layout=

TODO - maybe make a video overview or something?

Couple of key files:
- bot.py - the bot!
- delve_controller.py - the main flow for the delves (game sessions)
- enemy.py and enemy_group.py - where you can add new enemy types and spawn configurations

=TODOs=

There's a lot, but generally there are three categories of major improvements needed first:
1. Enhancements to the combat encounters. Right now, there are basic attack actions. The enemies need GOAP, and enemies and players need spells/abilities, players need consumable item use, etc.
2. Content, content, content. The mines, biomes, enemies, items are all as basic as needed to test that everything mechanically works. I have a Notion file with lots of biome plans if anyone's interested, but you could take this in any direction, such as a sci-fi theme exploring different planets or stars instead of mines (e.g.).
3. Persistence. No state is currently saved, so restarting the bot resets everything.

Beyond that, some general plans were:
- Professions and crafting
- Character improvement
- Loot gen
- An additional encampment-like channel for player commerce
