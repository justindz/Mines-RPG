import random


def roll(count, die, crit=False) -> int:
    if crit:
        return count * die

    total = 0

    for _ in range(0, count):
        total += random.randint(1, die) if isinstance(die, int) else round(random.uniform(0.01, die), 2)

    return total


def count(level) -> int:
    return max(int((level-1)/2), 1)
