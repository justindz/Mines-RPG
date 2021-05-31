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
    def __init__(self, _name, _description, _level, _cost, _effects, _area=0, _cooldown=0, _area_modifiable=False, _cooldown_modifiable=False,
                 _base_crit_chance=0.05, _can_target_ally=True, _can_target_enemy=True, _summon=None):
        super().__init__(_name, _description, _level, _cost, _effects, _area, _cooldown, _area_modifiable, _cooldown_modifiable)

        if _summon is None:
            _summon = []

        self.base_crit_chance = _base_crit_chance
        self.can_target_ally = _can_target_ally
        self.can_target_enemy = _can_target_enemy
        self.summon = _summon


spells = {
    'stalagmite': Spell('Stalagmite', 'Stalagmite description.', 1,
                        {'h': 0, 's': 0, 'm': 5},
                        [SpellEffect(EffectType.damage_health, Elements.earth, 3, 6)],
                        _can_target_ally=False),
}
