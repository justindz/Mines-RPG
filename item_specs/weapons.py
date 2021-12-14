from elements import Elements
from items.weapon import WeaponType

weapons = {
    # Hammer/Str
    'rusty_hammer': {
        'name': 'Rusty Hammer',
        'description': 'TODO',
        'level': 1,
        'weight': 3,
        'weapon_type': WeaponType.hammer.value,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0
    },
    'rusty_warhmammer': {
        'name': 'Rusty Warhammer',
        'description': 'TODO',
        'level': 1,
        'weight': 8,
        'weapon_type': WeaponType.hammer.value,
        'bonus_strength': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0
    },
    'stone_hammer': {
        'name': 'Stone Hammer',
        'description': 'TODO',
        'level': 3,
        'weight': 5,
        'weapon_type': WeaponType.hammer.value,
        'bonus_strength': 4,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 4
    },
    'stone_warhmammer': {
        'name': 'Stone Warhammer',
        'description': 'TODO',
        'level': 3,
        'weight': 10,
        'weapon_type': WeaponType.hammer.value,
        'bonus_strength': 4,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 6
    },
    'iron_hammer': {
        'name': 'Iron Hammer',
        'description': 'TODO',
        'level': 5,
        'weight': 5,
        'weapon_type': WeaponType.hammer.value,
        'bonus_strength': 8,
        'base_crit_chance': 0.05,
        'damages': [[2, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 8
    },
    'iron_warhmammer': {
        'name': 'Iron Warhammer',
        'description': 'TODO',
        'level': 5,
        'weight': 10,
        'weapon_type': WeaponType.hammer.value,
        'bonus_strength': 8,
        'base_crit_chance': 0.05,
        'damages': [[2, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 12
    },
    # Sword/Int
    'rusty_longsword': {
        'name': 'Rusty Longsword',
        'description': 'TODO',
        'level': 1,
        'weight': 3,
        'weapon_type': WeaponType.sword.value,
        'bonus_intelligence': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
    },
    'rusty_greatsword': {
        'name': 'Rusty Greatsword',
        'description': 'TODO',
        'level': 1,
        'weight': 8,
        'weapon_type': WeaponType.sword.value,
        'bonus_intelligence': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0
    },
    'stone_longsword': {
        'name': 'Stone Longsword',
        'description': 'TODO',
        'level': 3,
        'weight': 5,
        'weapon_type': WeaponType.sword.value,
        'bonus_intelligence': 4,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 4
    },
    'stone_greatsword': {
        'name': 'Stone Greatsword',
        'description': 'TODO',
        'level': 3,
        'weight': 10,
        'weapon_type': WeaponType.sword.value,
        'bonus_intelligence': 4,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 6
    },
    'iron_longsword': {
        'name': 'Iron Longsword',
        'description': 'TODO',
        'level': 5,
        'weight': 5,
        'weapon_type': WeaponType.sword.value,
        'bonus_intelligence': 8,
        'base_crit_chance': 0.05,
        'damages': [[2, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 8
    },
    'iron_greatsword': {
        'name': 'Iron Greatsword',
        'description': 'TODO',
        'level': 5,
        'weight': 10,
        'weapon_type': WeaponType.sword.value,
        'bonus_intelligence': 8,
        'base_crit_chance': 0.05,
        'damages': [[2, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 12
    },
    # Dagger/Dex
    'rusty_shiv': {
        'name': 'Rusty Shiv',
        'description': 'TODO',
        'level': 1,
        'weight': 1,
        'weapon_type': WeaponType.dagger.value,
        'bonus_dexterity': 2,
        'base_crit_chance': 0.08,
        'damages': [[1, 3, Elements.earth.value]],
        'crit_damage': 0
    },
    'rusty_dagger': {
        'name': 'Rusty Dagger',
        'description': 'TODO',
        'level': 1,
        'weight': 2,
        'weapon_type': WeaponType.dagger.value,
        'bonus_dexterity': 2,
        'base_crit_chance': 0.07,
        'damages': [[1, 5, Elements.earth.value]],
        'crit_damage': 0
    },
    'stone_shiv': {
        'name': 'Stone Shiv',
        'description': 'TODO',
        'level': 3,
        'weight': 3,
        'weapon_type': WeaponType.dagger.value,
        'bonus_dexterity': 4,
        'base_crit_chance': 0.08,
        'damages': [[1, 3, Elements.earth.value]],
        'crit_damage': 0,
        'required_dexterity': 4
    },
    'stone_dagger': {
        'name': 'Stone Dagger',
        'description': 'TODO',
        'level': 3,
        'weight': 4,
        'weapon_type': WeaponType.dagger.value,
        'bonus_dexterity': 4,
        'base_crit_chance': 0.07,
        'damages': [[1, 5, Elements.earth.value]],
        'crit_damage': 0,
        'required_dexterity': 6
    },
    'iron_shiv': {
        'name': 'Iron Shiv',
        'description': 'TODO',
        'level': 5,
        'weight': 3,
        'weapon_type': WeaponType.dagger.value,
        'bonus_dexterity': 4,
        'base_crit_chance': 0.08,
        'damages': [[2, 3, Elements.earth.value]],
        'crit_damage': 0,
        'required_dexterity': 8
    },
    'iron_dagger': {
        'name': 'Iron Dagger',
        'description': 'TODO',
        'level': 5,
        'weight': 4,
        'weapon_type': WeaponType.dagger.value,
        'bonus_dexterity': 4,
        'base_crit_chance': 0.07,
        'damages': [[2, 5, Elements.earth.value]],
        'crit_damage': 0,
        'required_dexterity': 12
    },
    # Staff/Will
    'rusty_scepter': {
        'name': 'Rusty Scepter',
        'description': 'TODO',
        'level': 1,
        'weight': 2,
        'weapon_type': WeaponType.staff.value,
        'bonus_willpower': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0
    },
    'rough_staff': {
        'name': 'Rough Staff',
        'description': 'TODO',
        'level': 1,
        'weight': 5,
        'weapon_type': WeaponType.staff.value,
        'bonus_willpower': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0
    },
    'stone_scepter': {
        'name': 'Stone Scepter',
        'description': 'TODO',
        'level': 3,
        'weight': 4,
        'weapon_type': WeaponType.staff.value,
        'bonus_willpower': 4,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_willpower': 4
    },
    'driftwood_staff': {
        'name': 'Driftwood Staff',
        'description': 'TODO',
        'level': 3,
        'weight': 6,
        'weapon_type': WeaponType.staff.value,
        'bonus_willpower': 4,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_willpower': 6
    },
    'iron_scepter': {
        'name': 'Iron Scepter',
        'description': 'TODO',
        'level': 5,
        'weight': 4,
        'weapon_type': WeaponType.staff.value,
        'bonus_willpower': 8,
        'base_crit_chance': 0.05,
        'damages': [[2, 3, Elements.earth.value]],
        'crit_damage': 0,
        'required_willpower': 8
    },
    'iron_staff': {
        'name': 'Iron Staff',
        'description': 'TODO',
        'level': 5,
        'weight': 8,
        'weapon_type': WeaponType.staff.value,
        'bonus_willpower': 8,
        'base_crit_chance': 0.05,
        'damages': [[2, 5, Elements.earth.value]],
        'crit_damage': 0,
        'required_willpower': 12
    },
    # Axe/Str+Int
    'rusty_war_axe': {
        'name': 'Rusty War Axe',
        'description': 'TODO',
        'level': 1,
        'weight': 3,
        'weapon_type': WeaponType.axe.value,
        'bonus_strength': 1,
        'bonus_intelligence': 1,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,

    },
    'rusty_battle_axe': {
        'name': 'Rusty Battle Axe',
        'description': 'TODO',
        'level': 1,
        'weight': 8,
        'weapon_type': WeaponType.axe.value,
        'bonus_strength': 1,
        'bonus_intelligence': 1,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,

    },
    'stone_war_axe': {
        'name': 'Stone War Axe',
        'description': 'TODO',
        'level': 3,
        'weight': 5,
        'weapon_type': WeaponType.axe.value,
        'bonus_strength': 2,
        'bonus_intelligence': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 2,
        'required_intelligence': 2,

    },
    'stone_battle_axe': {
        'name': 'Stone Battle Axe',
        'description': 'TODO',
        'level': 3,
        'weight': 10,
        'weapon_type': WeaponType.axe.value,
        'bonus_strength': 2,
        'bonus_intelligence': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 3,
        'required_intelligence': 3,

    },
    'iron_war_axe': {
        'name': 'Iron War Axe',
        'description': 'TODO',
        'level': 5,
        'weight': 5,
        'weapon_type': WeaponType.axe.value,
        'bonus_strength': 4,
        'bonus_intelligence': 4,
        'base_crit_chance': 0.05,
        'damages': [[2, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 5,
        'required_intelligence': 5,

    },
    'iron_battle_axe': {
        'name': 'Iron Battle Axe',
        'description': 'TODO',
        'level': 5,
        'weight': 10,
        'weapon_type': WeaponType.axe.value,
        'bonus_strength': 5,
        'bonus_intelligence': 5,
        'base_crit_chance': 0.05,
        'damages': [[2, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 6,
        'required_intelligence': 6,

    },
    # Spear/Str+Dex
    'rusty_spear': {
        'name': 'Rusty Spear',
        'description': 'TODO',
        'level': 1,
        'weight': 4,
        'weapon_type': WeaponType.spear.value,
        'bonus_strength': 1,
        'bonus_dexterity': 1,
        'base_crit_chance': 0.06,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0
    },
    'rusty_lance': {
        'name': 'Rusty Lance',
        'description': 'TODO',
        'level': 1,
        'weight': 8,
        'weapon_type': WeaponType.spear.value,
        'bonus_strength': 1,
        'bonus_dexterity': 1,
        'base_crit_chance': 0.06,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0
    },
    'stone_spear': {
        'name': 'Stone Spear',
        'description': 'TODO',
        'level': 3,
        'weight': 6,
        'weapon_type': WeaponType.spear.value,
        'bonus_strength': 2,
        'bonus_dexterity': 2,
        'base_crit_chance': 0.06,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 2,
        'required_dexterity': 2
    },
    'stone_lance': {
        'name': 'Stone Lance',
        'description': 'TODO',
        'level': 3,
        'weight': 10,
        'weapon_type': WeaponType.spear.value,
        'bonus_strength': 2,
        'bonus_dexterity': 2,
        'base_crit_chance': 0.06,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 3,
        'required_dexterity': 3
    },
    'iron_spear': {
        'name': 'Iron Spear',
        'description': 'TODO',
        'level': 5,
        'weight': 6,
        'weapon_type': WeaponType.spear.value,
        'bonus_strength': 4,
        'bonus_dexterity': 4,
        'base_crit_chance': 0.06,
        'damages': [[2, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 5,
        'required_dexterity': 5
    },
    'iron_lance': {
        'name': 'Iron Lance',
        'description': 'TODO',
        'level': 5,
        'weight': 10,
        'weapon_type': WeaponType.spear.value,
        'bonus_strength': 5,
        'bonus_dexterity': 5,
        'base_crit_chance': 0.06,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 6,
        'required_dexterity': 6
    },
    # Flail/Str+Will
    'rusty_morning_star': {
        'name': 'Rusty Morning Star',
        'description': 'TODO',
        'level': 1,
        'weight': 4,
        'weapon_type': WeaponType.flail.value,
        'bonus_strength': 1,
        'bonus_willpower': 1,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0
    },
    'rusty_flail': {
        'name': 'Rusty Flail',
        'description': 'TODO',
        'level': 1,
        'weight': 8,
        'weapon_type': WeaponType.flail.value,
        'bonus_strength': 1,
        'bonus_willpower': 1,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0
    },
    'stone_morning_star': {
        'name': 'Stone Morning Star',
        'description': 'TODO',
        'level': 3,
        'weight': 6,
        'weapon_type': WeaponType.flail.value,
        'bonus_strength': 2,
        'bonus_willpower': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 2,
        'required_willpower': 2
    },
    'stone_flail': {
        'name': 'Stone Flail',
        'description': 'TODO',
        'level': 3,
        'weight': 10,
        'weapon_type': WeaponType.flail.value,
        'bonus_strength': 2,
        'bonus_willpower': 2,
        'base_crit_chance': 0.05,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 3,
        'required_willpower': 3
    },
    'iron_morning_star': {
        'name': 'Iron Morning Star',
        'description': 'TODO',
        'level': 5,
        'weight': 6,
        'weapon_type': WeaponType.flail.value,
        'bonus_strength': 4,
        'bonus_willpower': 4,
        'base_crit_chance': 0.05,
        'damages': [[2, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 5,
        'required_willpower': 5
    },
    'iron_flail': {
        'name': 'Iron Flail',
        'description': 'TODO',
        'level': 5,
        'weight': 10,
        'weapon_type': WeaponType.flail.value,
        'bonus_strength': 5,
        'bonus_willpower': 5,
        'base_crit_chance': 0.05,
        'damages': [[2, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_strength': 6,
        'required_willpower': 6
    },
    # Fist/Int+Dex
    'rusty_katar': {
        'name': 'Rusty Katar',
        'description': 'TODO',
        'level': 1,
        'weight': 2,
        'weapon_type': WeaponType.fist.value,
        'bonus_intelligence': 1,
        'bonus_dexterity': 1,
        'base_crit_chance': 0.06,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0
    },
    'rusty_claw': {
        'name': 'Rusty Claw',
        'description': 'TODO',
        'level': 1,
        'weight': 3,
        'weapon_type': WeaponType.fist.value,
        'bonus_intelligence': 1,
        'bonus_dexterity': 1,
        'base_crit_chance': 0.06,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,

    },
    'stone_katar': {
        'name': 'Stone Katar',
        'description': 'TODO',
        'level': 3,
        'weight': 4,
        'weapon_type': WeaponType.fist.value,
        'bonus_intelligence': 2,
        'bonus_dexterity': 2,
        'base_crit_chance': 0.06,
        'damages': [[1, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 2,
        'required_dexterity': 2
    },
    'stone_claw': {
        'name': 'Stone Claw',
        'description': 'TODO',
        'level': 3,
        'weight': 5,
        'weapon_type': WeaponType.fist.value,
        'bonus_intelligence': 2,
        'bonus_dexterity': 2,
        'base_crit_chance': 0.06,
        'damages': [[1, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 3,
        'required_dexterity': 3,
    },
    'iron_katar': {
        'name': 'Iron Katar',
        'description': 'TODO',
        'level': 5,
        'weight': 4,
        'weapon_type': WeaponType.fist.value,
        'bonus_intelligence': 4,
        'bonus_dexterity': 4,
        'base_crit_chance': 0.06,
        'damages': [[2, 4, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 5,
        'required_dexterity': 5
    },
    'iron_claw': {
        'name': 'Iron Claw',
        'description': 'TODO',
        'level': 5,
        'weight': 5,
        'weapon_type': WeaponType.fist.value,
        'bonus_intelligence': 5,
        'bonus_dexterity': 5,
        'base_crit_chance': 0.06,
        'damages': [[2, 6, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 6,
        'required_dexterity': 6,
    },
    # Magic/Int+Will
    'rough_wand': {
        'name': 'Rough Wand',
        'description': 'TODO',
        'level': 1,
        'weight': 2,
        'weapon_type': WeaponType.magic.value,
        'bonus_intelligence': 1,
        'bonus_willpower': 1,
        'bonus_mana': 10,
        'base_crit_chance': 0.04,
        'damages': [[1, 2, Elements.earth.value]],
        'crit_damage': 5,

    },
    'cracked_orb': {
        'name': 'Cracked Orb',
        'description': 'TODO',
        'level': 1,
        'weight': 3,
        'weapon_type': WeaponType.magic.value,
        'bonus_intelligence': 1,
        'bonus_willpower': 1,
        'bonus_mana': 20,
        'base_crit_chance': 0.01,
        'damages': [[1, 1, Elements.earth.value]],
        'crit_damage': 0
    },
    'driftwood_wand': {
        'name': 'Driftwood Wand',
        'description': 'TODO',
        'level': 3,
        'weight': 2,
        'weapon_type': WeaponType.magic.value,
        'bonus_intelligence': 2,
        'bonus_willpower': 2,
        'bonus_mana': 15,
        'base_crit_chance': 0.04,
        'damages': [[1, 2, Elements.earth.value]],
        'crit_damage': 5,
        'required_intelligence': 2,
        'required_willpower': 2
    },
    'dull_orb': {
        'name': 'Dull Orb',
        'description': 'TODO',
        'level': 3,
        'weight': 3,
        'weapon_type': WeaponType.magic.value,
        'bonus_intelligence': 2,
        'bonus_willpower': 2,
        'bonus_mana': 30,
        'base_crit_chance': 0.01,
        'damages': [[1, 1, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 3,
        'required_willpower': 3
    },
    'carved_wand': {
        'name': 'Carved Wand',
        'description': 'TODO',
        'level': 5,
        'weight': 2,
        'weapon_type': WeaponType.magic.value,
        'bonus_intelligence': 4,
        'bonus_willpower': 4,
        'bonus_mana': 25,
        'base_crit_chance': 0.05,
        'damages': [[2, 2, Elements.earth.value]],
        'crit_damage': 7,
        'required_intelligence': 4,
        'required_willpower': 4
    },
    'glowing_orb': {
        'name': 'Glowing Orb',
        'description': 'TODO',
        'level': 5,
        'weight': 3,
        'weapon_type': WeaponType.magic.value,
        'bonus_intelligence': 4,
        'bonus_willpower': 4,
        'bonus_mana': 50,
        'base_crit_chance': 0.01,
        'damages': [[2, 1, Elements.earth.value]],
        'crit_damage': 0,
        'required_intelligence': 4,
        'required_willpower': 4
    },
    # Thrown/Dex+Will
    'rusty_darts': {
        'name': 'Rusty Darts',
        'description': 'TODO',
        'level': 1,
        'weight': 1,
        'weapon_type': WeaponType.thrown.value,
        'bonus_dexterity': 1,
        'bonus_willpower': 1,
        'base_crit_chance': 0.06,
        'damages': [[1, 3, Elements.earth.value]],
        'crit_damage': 3
    },
    'rusty_chakram': {
        'name': 'Rusty Chakram',
        'description': 'TODO',
        'level': 1,
        'weight': 3,
        'weapon_type': WeaponType.thrown.value,
        'bonus_dexterity': 1,
        'bonus_willpower': 1,
        'base_crit_chance': 0.06,
        'damages': [[1, 5, Elements.earth.value]],
        'crit_damage': 3
    },
    'stone_darts': {
        'name': 'Stone Darts',
        'description': 'TODO',
        'level': 3,
        'weight': 3,
        'weapon_type': WeaponType.thrown.value,
        'bonus_dexterity': 2,
        'bonus_willpower': 2,
        'base_crit_chance': 0.06,
        'damages': [[1, 3, Elements.earth.value]],
        'crit_damage': 3,
        'required_dexterity': 2,
        'required_willpower': 2
    },
    'stone_chakram': {
        'name': 'Stone Chakram',
        'description': 'TODO',
        'level': 3,
        'weight': 5,
        'weapon_type': WeaponType.thrown.value,
        'bonus_dexterity': 2,
        'bonus_willpower': 2,
        'base_crit_chance': 0.06,
        'damages': [[1, 5, Elements.earth.value]],
        'crit_damage': 3,
        'required_dexterity': 3,
        'required_willpower': 3,
    },
    'iron_darts': {
        'name': 'Iron Darts',
        'description': 'TODO',
        'level': 5,
        'weight': 3,
        'weapon_type': WeaponType.thrown.value,
        'bonus_dexterity': 4,
        'bonus_willpower': 4,
        'base_crit_chance': 0.06,
        'damages': [[2, 3, Elements.earth.value]],
        'crit_damage': 5,
        'required_dexterity': 5,
        'required_willpower': 5
    },
    'iron_chakram': {
        'name': 'Iron Chakram',
        'description': 'TODO',
        'level': 5,
        'weight': 5,
        'weapon_type': WeaponType.thrown.value,
        'bonus_dexterity': 5,
        'bonus_willpower': 5,
        'base_crit_chance': 0.06,
        'damages': [[2, 5, Elements.earth.value]],
        'crit_damage': 5,
        'required_dexterity': 6,
        'required_willpower': 6,
    },
}