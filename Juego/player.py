from dataclasses import dataclass

@dataclass
class PlayerMemento:
    x: float
    y: float
    level_index: int

class PlayerCaretaker:
    def __init__(self, player):
        self.player = player
        self._memento = None

    def create_memento(self):
        self._memento = PlayerMemento(self.player.x, self.player.y, self.player.level)
        return self._memento

    def get_memento(self):
        return self._memento

    def restore(self, memento=None):
        if memento is None:
            memento = self._memento
        if memento:
            self.player.x = memento.x
            self.player.y = memento.y
            self.player.level = memento.level_index
            if hasattr(self.player, 'update_rect'):
                try:
                    self.player.update_rect()
                except Exception:
                    pass

class Player:
    # Increased size ~75% (from 16 -> 28)
    SIZE = 28
    COLOR = (200, 30, 30)
    SPEED = 200.0  # pixels per second

    def __init__(self, x: float, y: float, level: int = 0):
        self.x = float(x)
        self.y = float(y)
        self.level = level
        self.rect = None
        self.strategy = None  # movement strategy
        self.invincible = False
        self.update_rect()

    def set_strategy(self, strat):
        self.strategy = strat

    def move(self, dx: float, dy: float):
        if self.strategy is not None and hasattr(self.strategy, 'transform'):
            dx, dy = self.strategy.transform(dx, dy, self)
        self.x += dx
        self.y += dy
        self.update_rect()

    def update_rect(self):
        import pygame
        self.rect = pygame.Rect(int(self.x), int(self.y), self.SIZE, self.SIZE)

    def draw(self, surface):
        import pygame
        self.update_rect()
        pygame.draw.rect(surface, self.COLOR, self.rect)
