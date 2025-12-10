import random
from enemy import Enemy

class EnemyStrategy:
    def decide(self, enemy: Enemy, player_position, level):
        raise NotImplementedError

class AggressiveStrategy(EnemyStrategy):
    def decide(self, enemy: Enemy, player_position, level):
        px, py = player_position
        enemy.targets = [(px, py)]

class DefensiveStrategy(EnemyStrategy):
    def decide(self, enemy: Enemy, player_position, level):
        px, py = player_position
        bx0, bx1 = enemy.bounds if hasattr(enemy, 'bounds') else (0, 800)
        mid = (bx0 + bx1)/2
        tx = bx1 - 20 if px < mid else bx0 + 20
        enemy.targets = [(tx, enemy.y)]

class RandomStrategy(EnemyStrategy):
    def decide(self, enemy: Enemy, player_position, level):
        bx0, bx1 = enemy.bounds if hasattr(enemy, 'bounds') else (0, 800)
        tx = random.uniform(bx0 + 20, bx1 - 20)
        ty = random.uniform(50, 550)
        enemy.targets = [(tx, ty)]
