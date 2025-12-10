from typing import Iterable, List
from enemy import Enemy

class EnemyGroup:
    def __init__(self, enemies: Iterable[Enemy] = ()):
        self.enemies: List[Enemy] = list(enemies)

    def add(self, enemy: Enemy):
        self.enemies.append(enemy)

    def remove(self, enemy: Enemy):
        self.enemies.remove(enemy)

    def update(self, dt):
        for e in self.enemies:
            e.update(dt)

    def draw(self, surface):
        for e in self.enemies:
            e.draw(surface)

    def collides_with(self, rect):
        for e in self.enemies:
            if e.collides_with(rect):
                return True
        return False

    def __iter__(self):
        return iter(self.enemies)

    def __len__(self):
        return len(self.enemies)
