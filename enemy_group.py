class EnemyGroup(object):
    def __init__(self, enemies: [list]):
        self.enemies = enemies


enemy_groups = {
    'basic': [
        [['slime', 'slime'], ['slime', 'slime', 'slime'], ['slime', 'slime', 'slime', 'slime']],
    ],
    'infernal': [
        [['bomb'], ['imp', 'bomb'], ['imp', 'imp', 'bomb']],
        [['imp'], ['imp', 'slime'], ['imp', 'imp', 'slime']],
        [['imp'], ['imp', 'imp'], ['imp', 'imp', 'imp']],
    ],
}
