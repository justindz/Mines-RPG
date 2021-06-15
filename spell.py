from elements import Elements
import ability
from ability import EffectType


class SpellEffect:
    def __init__(self, _type, _element, _min, _max):
        self.type = _type
        self.element = _element
        self.min = _min
        self.max = _max


class Spell(ability.Ability):
    def __init__(self, _name, _description, _level, _cost, _effects, _area=0, _area_modifiable=False,
                 _base_crit_chance=0.05, _targets_enemies=True, _summon=None):
        super().__init__(_name, _description, _level, _cost, _effects, _area, _area_modifiable)

        if _summon is None:
            _summon = []

        self.base_crit_chance = _base_crit_chance
        self.targets_enemies = _targets_enemies
        self.summon = _summon


spells = {
    'stalagmite': Spell('Stalagmite', 'Stalagmite description.', 1, {'h': 0, 's': 0, 'm': 5},
                        [SpellEffect(EffectType.damage_health, Elements.earth, 3, 6)], _targets_enemies=True),
    'mend_wounds': Spell('Mend Wounds', 'Mend description.', 1, {'h': 0, 's': 0, 'm': 5},
                         [SpellEffect(EffectType.restore_health, Elements.water, 5, 10),
                          SpellEffect(EffectType.restore_stamina, Elements.water, 5, 10),
                          SpellEffect(EffectType.restore_mana, Elements.water, 5, 10)],
                         _base_crit_chance=0.01, _targets_enemies=False),
}
