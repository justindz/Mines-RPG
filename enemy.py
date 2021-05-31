# Local
from actor import Actor
from elements import Elements
import utilities


#

class Enemy(Actor):
    def __init__(self, name, strength, strength_growth, intelligence, intelligence_growth, dexterity, dexterity_growth,
                 willpower, willpower_growth, health, health_growth, mana, mana_growth, stamina, stamina_growth, init,
                 init_growth, earth_res, earth_res_growth, fire_res, fire_res_growth, electricity_res,
                 electricity_res_growth, water_res, water_res_growth):
        super().__init__()
        self.name = name

        # Stats
        self.strength = strength
        self.strength_growth = strength_growth
        self.intelligence = intelligence
        self.intelligence_growth = intelligence_growth
        self.dexterity = dexterity
        self.dexterity_growth = dexterity_growth
        self.willpower = willpower
        self.willpower_growth = willpower_growth
        self.health = self.current_health = health
        self.health_growth = health_growth
        self.mana = mana
        self.mana_growth = mana_growth
        self.stamina = stamina
        self.stamina_growth = stamina_growth
        self.current_health = self.health
        self.current_stamina = self.stamina
        self.current_mana = self.mana
        self.init = init
        self.init_growth = init_growth

        # Resistances
        self.earth_res = earth_res
        self.earth_res_growth = earth_res_growth
        self.fire_res = fire_res
        self.fire_res_growth = fire_res_growth
        self.electricity_res = electricity_res
        self.electricity_res_growth = electricity_res_growth
        self.water_res = water_res
        self.water_res_growth = water_res_growth

    def scale(self, depth):
        self.level = depth
        gap = depth - 1
        self.strength += round(self.strength_growth * gap)
        self.intelligence += round(self.intelligence_growth * gap)
        self.dexterity += round(self.dexterity_growth * gap)
        self.willpower += round(self.willpower_growth * gap)
        self.health += round(self.health_growth * gap)
        self.mana += round(self.mana_growth * gap)
        self.stamina += round(self.stamina_growth * gap)
        self.current_health = self.health
        self.current_stamina = self.stamina
        self.current_mana = self.mana
        self.init += round(self.init_growth * gap)
        self.name = prefixes[utilities.clamp(int(depth / 10), 1, len(prefixes))] + " " + self.name

    def take_damage(self, dmgs: list):
        for dmg in dmgs:
            amt = dmg[0]

            if dmg[1] == Elements.earth:
                amt *= (1.0 - self.earth_res)
            elif dmg[1] == Elements.fire:
                amt *= (1.0 - self.fire_res)
            elif dmg[1] == Elements.electricity:
                amt *= (1.0 - self.electricity_res)
            elif dmg[1] == Elements.water:
                amt *= (1.0 - self.water_res)

            self.current_health -= round(amt)
            self.current_health = max(0, self.current_health)

        return dmgs

    def attack(self):
        return [[2, Elements.earth]]


prefixes = {
    1: 'Pico',
    2: 'Nano',
    3: 'Micro',
    4: 'Milli',
    5: 'Centi',
    6: 'Deci',
    7: 'Nomi',
    8: 'Deca',
    9: 'Hecto',
    10: 'Kilo',
    11: 'Mega',
    12: 'Giga',
    13: 'Tera',
    14: 'Peta',
    15: 'Exa',
    16: 'Zetta',
    17: 'Yotta'
}

enemies = {
    'slime': Enemy('Slime', 1, 0.3, 1, 0.3, 1, 0.3, 1, 0.3, 10, 0.1, 10, 0.1, 10, 0.1, 5, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0),
}
