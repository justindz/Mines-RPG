import random

import spell
import skill

from consumable import Consumable


#  DISPLAY  #


def red(txt):
    return '```diff\n- {}```'.format(txt)


def yellow(txt):
    return '```fix\n{}```'.format(txt)


def green(txt):
    return '```diff\n+ {}```'.format(txt)


def blue(txt):
    return '```ini\n[{}]```'.format(txt)


def bold(txt):
    return '**{}**'.format(txt)


def italics(txt):
    return '*{}*'.format(txt)


def underline(txt):
    return '__{}__'.format(txt)


def dmgs_to_str(dmgs):
    out = ''

    for dmg in dmgs:
        out += '{} {},'.format(int(dmg[0]), dmg[1].name)

    out = out[:-1] + ' damage'
    return out


#  LOOKUPS  #


def get_ability_by_name(ability_name):
    try:
        if ability_name.startswith('spell-'):
            return spell.spells[ability_name[6:]]
        elif ability_name.startswith("skill-"):
            return skill.skills[ability_name[6:]]
        else:
            raise Exception(f'utilities.get_ability_name called for unknown type: {ability_name}')
    except KeyError:
        raise Exception(f'utilities.get_ability_name called for unknown type: {ability_name}')


#  MATHS  #


def stat_check(total: int, difficulty: int, scaling: float, depth: int):
    chance = 0.0001 * (total - difficulty + (depth * scaling)) ** 3 + .75
    chance = clamp(chance, 0.05, 0.95)

    if random.uniform(0, 1) <= chance:
        return True

    return False


def scale_xp(xp: int, l1: int, l2: int):
    penalty = 0.01 * 10 * abs(l1 - l2) ** 3
    return max(round(xp * 1 - penalty), 1)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))
