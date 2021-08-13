class EnemyGroup(object):
    def __init__(self, enemies: [list]):
        self.enemies = enemies


enemy_groups = {
    'basic': [
        [['slime', 'slime'], ['slime', 'slime', 'slime'], ['slime', 'slime', 'slime', 'slime']],
        [['scarab'], ['slime', 'scarab'], ['slime', 'slime', 'scarab', ]],
        [['slime', 'spider'], ['slime', 'spider', 'spider'], ['slime', 'slime', 'spider', 'spider']],
        [['spider', 'spider'], ['spider', 'spider', 'scarab'], ['spider', 'scarab', 'scarab']],
    ],
    'infernal': [
        [['bomb'], ['imp', 'bomb'], ['imp', 'imp', 'bomb']],
        [['imp'], ['imp', 'slime'], ['imp', 'imp', 'slime']],
        [['imp'], ['imp', 'imp'], ['imp', 'imp', 'imp']],
    ],
}
