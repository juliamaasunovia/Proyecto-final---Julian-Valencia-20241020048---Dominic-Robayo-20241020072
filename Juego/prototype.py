"""
Cloning utilities: clone_enemy / clone_level
Used to recreate fresh enemies from prototypes stored in level definitions.
"""
from enemy import Enemy
from level import Level
import pygame

def clone_enemy(original: Enemy) -> Enemy:
    state_cls = original.state.__class__ if original.state else None
    new_state = state_cls() if state_cls else None
    ne = Enemy(original.x, original.y, radius=original.radius, speed=original.speed, state=new_state)
    ne.targets = list(getattr(original, 'targets', []))
    ne.base_y = getattr(original, 'base_y', original.y)
    ne.amplitude = getattr(original, 'amplitude', 30)
    ne.frequency = getattr(original, 'frequency', 2)
    ne.bounds = tuple(getattr(original, 'bounds', (0, pygame.display.get_surface().get_width() if pygame.display.get_surface() else 800)))
    ne.direction = getattr(original, 'direction', 1)
    return ne

def clone_level(original: Level) -> Level:
    walls_copy = [w.copy() for w in original.walls]
    enemies_copy = [clone_enemy(e) for e in original.enemies]
    start_copy = (original.start[0], original.start[1])
    goal_copy = original.goal.copy() if getattr(original, 'goal', None) is not None else None
    return Level(walls_copy, enemies_copy, start_copy, goal_copy)
