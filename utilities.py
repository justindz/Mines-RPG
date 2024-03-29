import ability
import dice
import spell
import skill
from elements import Elements


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


def get_rarity_symbol(rarity: int):
    if rarity == 2:
        return ':small_blue_diamond:'
    elif rarity == 3:
        return ':small_orange_diamond:'

    return ''


def get_elemental_symbol(element: Elements) -> str:
    if element == Elements.earth:
        return ':rock:'
    elif element == Elements.fire:
        return ':fire:'
    elif element == Elements.electricity:
        return ':zap:'
    elif element == Elements.water:
        return ':droplet:'


def dmgs_to_str(dmgs):
    out = ''

    for dmg in dmgs:
        out += '{} {},'.format(int(dmg[0]), dmg[1].name)

    out = out[:-1] + ' damage'
    return out


#  LOOKUPS  #
def get_ability_by_name(ability_name: str) -> ability:
    try:
        if ability_name.startswith('spell-'):
            return spell.spells[ability_name[6:]]
        elif ability_name.startswith("skill-"):
            return skill.skills[ability_name[6:]]
        else:
            raise Exception(f'utilities.get_ability_name called for unknown type: {ability_name}')
    except KeyError:
        raise Exception(f'utilities.get_ability_name called for unknown type: {ability_name}')


def ability_to_str(ability_name: str, level=1) -> str:
    ab = get_ability_by_name(ability_name)
    out = f'''
=========={ab.name} ({"Skill" if isinstance(ab, skill.Skill) else "Spell"})==========
{ab.description}

{'Requires: ' + ', '.join([x.name.capitalize() for x in ab.weapon_types]) if isinstance(ab, skill.Skill) else ''}
Targets: {"Enemies" if isinstance(ab, spell.Spell) and ab.targets_enemies else "Allies"}
Cost: {ab.ability_cost_to_str()}'''

    if isinstance(ab, spell.Spell):
        out += f'\nBase crit chance: {int(ab.base_crit_chance * 100)}%'

    if len(ab.activates) > 0:
        out += '\nActivates: '

        for ele in ab.activates:
            out += get_elemental_symbol(ele)

    if len(ab.consumes) > 0:
        out += '\nConsumes: '

        for ele in ab.consumes:
            out += get_elemental_symbol(ele)

    out += f'\nArea of Effect: {"None" if ab.area == 0 else ab.area}{ " (modifiable)" if ab.area_modifiable else "" }'
    out += f'\n\nEffects:'

    if isinstance(ab, skill.Skill):
        for effect in ab.effects:
            out += f'\n- {effect.type.name.capitalize()} : {effect.multiplier}x Weapon Damage'
    elif isinstance(ab, spell.Spell):
        for effect in ab.effects:
            if effect.type == ability.EffectType.damage_health:
                out += f'\n- Damage Health : {dice.count(level)}d{effect.dice_value} {get_elemental_symbol(effect.element)}'
            elif effect.type == ability.EffectType.burn:
                out += f'\n- Burn : {effect.dot_value} {get_elemental_symbol(effect.element)} for {effect.effect_turns} turns'
            elif effect.type == ability.EffectType.bleed:
                out += f'\n- Bleed : {effect.dot_value} {get_elemental_symbol(effect.element)} for {effect.effect_turns} turns'
            elif effect.type == ability.EffectType.buff:
                out += f'\n- Buff : {dice.count(level)}d{effect.dice_value} {effect.stat} {get_elemental_symbol(effect.element)} for {effect.effect_turns} turns'
            elif effect.type == ability.EffectType.debuff:
                out += f'\n- Debuff : -{dice.count(level)}d{effect.dice_value} {effect.stat} {get_elemental_symbol(effect.element)} for {effect.effect_turns} turns'

    return out


def get_requirements_display_string(item) -> str:
    if item.itype == 1:
        display_string = f'\nStrength {item.required_strength}' if item.required_strength != 0 else ''
        display_string += f'\nIntelligence {item.required_intelligence}' if item.required_intelligence != 0 else ''
        display_string += f'\nDexterity {item.required_dexterity}' if item.required_dexterity != 0 else ''
        display_string += f'\nWillpower {item.required_willpower}' if item.required_willpower != 0 else ''
        return display_string.lstrip('\n')
    else:
        return 'None'


def get_socket_display(item) -> str:
    out = ''

    if item.itype in [4, 7, 8]:
        return out

    for socket in item.sockets:
        if socket is None:
            out += ' {  }'
        else:
            out += f' {{ {socket} }}'

    return out.lstrip(' ')


def get_consumable_effects_display_string(item) -> str:
    if item.itype != 9:
        raise Exception(f'get_consumable_effects_display_string for unsupported itype {item.itype} on {item.name}')

    out = ''
    out += f'\n{item.health:+} health' if item.health != 0 else ''
    out += f'\n{item.stamina:+} stamina' if item.stamina != 0 else ''
    out += f'\n{item.mana:+} mana' if item.mana != 0 else ''
    out += f'\n{item.burn:+} burn duration' if item.burn != 0 else ''
    out += f'\n{item.bleed:+} bleed duration' if item.bleed != 0 else ''
    out += f'\n{item.shock:+} shock level' if item.shock != 0 else ''
    out += f'\n{item.confusion:+} confusion level' if item.confusion != 0 else ''
    return out.lstrip('\n')


#  MATHS  #
# def stat_check(total: int, difficulty: int, scaling: float, depth: int):
#     chance = 0.0001 * (total - difficulty + (depth * scaling)) ** 3 + .75
#     chance = clamp(chance, 0.05, 0.95)
#
#     if random.uniform(0, 1) <= chance:
#         return True
#
#     return False


# def scale_xp(xp: int, l1: int, l2: int):
#     penalty = 0.01 * 10 * abs(l1 - l2) ** 3
#     return max(round(xp * 1 - penalty), 1)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))
