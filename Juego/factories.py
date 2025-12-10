from typing import List, Tuple, Optional
import pygame
from enemy import Enemy, PatrolState, SineState, FastState
from level import Level

class EnemyFactory:
    @staticmethod
    def create_patrol(x: float, y: float, radius: int = 12, speed: int = 90,
                      targets: Optional[List[Tuple[float, float]]] = None) -> Enemy:
        e = Enemy(x, y, radius=radius, speed=speed, state=PatrolState())
        e.targets = targets or [(x, y)]
        return e

    @staticmethod
    def create_sine(x: float, y: float, radius: int = 12, speed: int = 80,
                    bounds: Tuple[int,int]=(0,800), amplitude: float = 30, frequency: float = 2) -> Enemy:
        e = Enemy(x, y, radius=radius, speed=speed, state=SineState())
        e.bounds = bounds
        e.base_y = y
        e.amplitude = amplitude
        e.frequency = frequency
        return e

    @staticmethod
    def create_fast(x: float, y: float, radius: int = 12, speed: int = 120,
                    targets: Optional[List[Tuple[float, float]]] = None) -> Enemy:
        e = Enemy(x, y, radius=radius, speed=speed, state=FastState())
        e.targets = targets or [(x, y)]
        return e

class LevelBuilder:
    def __init__(self):
        self._walls = []
        self._enemies = []
        self._start = (0,0)
        self._goal = pygame.Rect(0,0,40,40)

    def add_wall(self, rect: pygame.Rect):
        self._walls.append(rect)
        return self

    def add_wall_xywh(self, x:int,y:int,w:int,h:int):
        self._walls.append(pygame.Rect(x,y,w,h))
        return self

    def add_enemy(self, enemy: Enemy):
        self._enemies.append(enemy)
        return self

    def set_start(self, x:int, y:int):
        self._start = (x,y)
        return self

    def set_goal(self, rect: pygame.Rect):
        self._goal = rect
        return self

    def build(self) -> Level:
        walls_copy = [w.copy() for w in self._walls]
        enemies_copy = list(self._enemies)
        return Level(walls_copy, enemies_copy, (self._start[0], self._start[1]), self._goal.copy())
