# Mines-RPG

Mines-RPG is a multiplayer, text-based adventure RPG implemented as a Discord bot. Supports solo and party play, focused on turn-based combat in progressively harder dungeons. Also includes simple professions and crafting. It is intended to be fairly hackable, provided your desired theme jives with the game mechanics.

## Where to go for help / try the game

The latest development version of the game will be on the Crane Mountain Gaming server: https://discord.gg/aZH68e4

If you want to try it out, and it's not currently running (\help in the encampment channel does nothing), ping the channel owner, justindz. Same goes for any questions or feedback about the game/code. Also bug reports. Note that the current version is quite feature-rich and definitely playable, but content development and balance testing is very much ongoing. Anyone interested in contributing to either of those efforts should inquire within.

If you want to support continued development, or just generally show your appreciation for this free resource, consider checking out the Crane Mountain Gaming Patreon.

## Running your own server

You need a python environment and mongodb database (see Environment Setup) to run the bot and a Discord server (see Discord setup) for the bot to join, and where the game is played.

### Environment setup

The following python dependencies are required:
* python 3.10 (3.6+ probably works)
* discord.py 1.7.3
* pymongo 3.12.2
* pymodm 0.4.3

Create a secrets.py file in the bot's root folder. Add the following variables:
* encampment_channel_id = integer
* market_channel_id = integer
* workshop_channel_id = integer
* admins = [list of integers]
* client_token = 'string'
* MONGODB_URI = 'mongodb+srv://string'

You also need a mongodb database to store the game's data. This can be run locally, or in (e.g.) mongodb atlas. You will need a mongodb:srv connection string to the database for a user with read and write access, which will go in secrets.py as the MONGODB_URI string. You do not need to create any collections. Those should be created for you as needed when the game saves data.

### Discord setup

If you have not provisioned a Discord bot before, you may want to supplement this guide with a tutorial as it is not very in-depth. Generally:
* Access the Discord developer portal and create an application.
* Generate an OAuth2 URL to join the bot to your server with the bot scope and the following permissions: Manage Roles, Manage Channels, Read Messages/View Channels, Send Messages, Manage Messages, Read Message History, Mention Everyone, Add Reactions
* Copy your bot token and paste it in secrets.py as the client_token string
* You must enable Server Members Intent
* Create channels on your Discord server for the encampment, market, and workshop, then copy their IDs and enter them in secrets.py as the three respective integers
* Add the ID integer for each Discord user you want to be a game admin (distinct from any server role) to the secrets.py list "admins" -- these members will be able to use admin-only commands to do things like spawn items and level up for testing purposes. Or cheating purposes. But really... testing.
* Run the bot and cross your fingers!

### Notes on how the bot works

The bot responds to prefixed (\) commands that it recognizes in the appropriate channels as configured in secrets.py (see above). The bot also responds to some commands via DM. Depending on the command and context, the bot may respond in the channel or via DM to the player. While channel responses are a nicer experience, DMs are used to keep things from getting too spammy and unreadable for players.

When any member of the server uses a game command (e.g. \inventory) that requires them to have a character, the bot will attempt to retrieve their existing character. If they do not have one, at this point a new character is created automatically for that player. That character is tied to the member's current name, and changing that name will break the association. There is currently no mechanism to transfer or reset a character, but anyone with database access can modify a character object to rename it if needed.

When a player or party starts a delve, the bot creates a temporary channel for the session. If a crash occurs, preventing a delve from ending normally (i.e. the party exits or dies), the bot is unable to remove the channels, so an admin will need to delete these manually.

## Where do I go to change X?

The game is designed to be customizable in terms of thematics and content. For example, the encampment channel could easily be called the hub channel, and the workshop channel could be called the replicator forge channel. Mines could be planets. You get the idea. That said, the customization is currently going to occur in code, either by changing various strings or the properties in dictionaries. Here are some of the main places to look for certain things:

### ai

This module includes the actions that can be performed by enemies. Don't modify action.py directly. You can modify existing actions or create new ones following the included examples, however.

### controllers

This module contains the controllers which interact with player commands. They are:
* admin - commands restricted to admins for testing purposes
* character - character management stuff, like inventory, equipping, leveling up, character sheet, etc.
* delve - everything related to participating in a delve
* market - market channel-only interactions related to buying and selling loot
* party - commands related to managing a party for group delving purposes
* workshop - workshop channel-only commands related to professions and crafting

For the most part, you won't change much in controllers. You may want to rename \delve depending on your game them, and you probably want to customize the NPC names in the market and workshop channels, as well as their banter. You might also want to make them talk less. Or more, if you're a sicko.

### item_specs

This is where you can modify the game's base loot. The syntax is vanilla python dictionary. Properties must be supported by the item type. Generally, follow the examples provided.

### biome.py

Each zone (aka, mine) has a biome that determines the "flavor" of the zone.

Here is an example biome:

```
'generic': Biome('generic',
    ['basic'],
    {
        1: ['slime', 'scarab', 'spider'],
        21: [],
    }),
```

Let's look at this line by line:
* Line 1: The key to the entry and the first property in the Biome() constructor is the biome name. These values need to match.
* Line 2: A list of room tags. Each room in the zone will be randomly selected from the total set of rooms available, based on all room tags in the biome.
* Lines 3-6: These are the enemy keys that this biome can spawn. The integers (1 and 21) are the minimum levels at which those enemy types can spawn. In this example, regardless of depth, this biome will always spawn slimes, spiders, and scarabs. At depth 21, no new monster types will spawn. At levels 21+ (assuming a monster was added to the 21 list) the total set of all 1s and 21s are candidates to spawn.

It may seem like overkill to have biomes distinct from mines. However, it should facilitate some interesting content re-use.

### bot.py

There are some channel messages you may want to customize here if you rename the game.

### enemies.py

This needs a more thorough write-up. For the most part, you should be able to copy and tweak existing examples. However, let's note a few key things:
* Every enemy needs at least one action and goal to function. Valid goal types are in enemy.py, and valid actions are in the ai module.
* Goal values are tricky, and take some practice. Generally getting enemies to behave how you want in the right circumstances is an iterative process. The bot is currently set up to console log planning output by default, which can help you debug unexpected behavior.
* Status effect names are used to create overlapping status effects. For example, two enemies may have a slow ability, and as long as both have the name 'Slowed' the last one applied will overwrite. Or you could be evil.
* By convention, enemies summoned by enemies should begin with key prefix 'summoned_' and should not themselves have a summon ability. Be nice.
* Growth stats are how the game scales enemies with depth. There are defaults, so you only override the ones you want to scale more or less for a particular enemy. Remember that your "level 1" enemies could be used at every depth. The main purpose of higher level enemies is to be more mechanically complex and challenging, rather than just being bundles of stats.

### item_factory.py

Some things you might want to change in here:
* The value of loot generated items
* Rarity drop chances

Be careful with both of those, however.

The "lucky" flag isn't used yet. Yet.

### loot_encounter.py

The descs array of strings should be tailored to your theme. These will probably need to move to the biome tag system, btw.

### room.py

Room descriptions are generated randomly from the applicable biome tags in the zone from the rooms dictionary. Aside from changing what's already there, if you add a biome tag, make sure to add a corresponding set of room descriptions.

### skill.py

Note: skills are abilities that require (and scale off of) weapons, and are used against enemies.

TODO: explain all this better. Follow existing examples.

### spell.py

Note: spells are abilities that do not require weapons, and may target enemies or players.

See the note under enemies.py regarding status effect naming conventions.

TODO: explain all this better. Follow existing examples.

### summons.py

See enemies.py. Summons are actually enemies who, by way of a modified planner, are on your side. As a result, everything you learn about customizing enemies also applies to summons.

### zone.py

The zones array is how you add new mines (or whatever you're gonna call 'em). They need a name, starting depth, description, and a biome.

## Roadmap

Here are some of the larger items planned:
* Way more content (please help!)
* Bunch o' stats collection for balance research
* Fixed-depth boss fights
* Cartographer profession and map making (similar to Path of Exile's map affix system)
* Multi-effect affixes
* Ladder API
* Mythic items (3 affixes)

TODO: either link to the Trello board, or move all that into github somehow?

## License

MIT License

Copyright (c) 2021 Crane Mountain Gaming, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Non-Legal

Separate from the license, if you do run a copy of this game, I would appreciate:
* Acknowledgment
* Support, if you have the means, and encouragement either way
* Feedback/contributions if you find issues or make engine improvements (not content tweaks)