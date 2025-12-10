import pygame

class PlayerDecorator:
    def __init__(self, player):
        object.__setattr__(self, "_player", player)

    def __getattr__(self, name):
        return getattr(self._player, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            setattr(self._player, name, value)

    def update_rect(self):
        return self._player.update_rect()

    def draw(self, surface):
        return self._player.draw(surface)

    def move(self, dx, dy):
        return self._player.move(dx, dy)

    def set_strategy(self, strat):
        if hasattr(self._player, "set_strategy"):
            return self._player.set_strategy(strat)

    def unwrap(self):
        return self._player

class SpeedDecorator(PlayerDecorator):
    def __init__(self, player, factor=1.5, duration=5.0):
        super().__init__(player)
        self._original_speed = getattr(self._player, "SPEED", None)
        if self._original_speed is not None:
            self._player.SPEED = self._player.SPEED * factor
        object.__setattr__(self, "remaining", duration)
        object.__setattr__(self, "active", True)

    def update(self, dt):
        if getattr(self, "active", False):
            self.remaining -= dt
            if self.remaining <= 0:
                if self._original_speed is not None:
                    self._player.SPEED = self._original_speed
                object.__setattr__(self, "active", False)
        if hasattr(self._player, "update"):
            self._player.update(dt)

    def draw(self, surface):
        try:
            r = self._player.rect.inflate(6,6)
            pygame.draw.rect(surface, (30,200,30), r, 2)
        except Exception:
            pass
        self._player.draw(surface)

class InvincibleDecorator(PlayerDecorator):
    def __init__(self, player, duration=3.0):
        super().__init__(player)
        object.__setattr__(self, "remaining", duration)
        object.__setattr__(self, "invincible", True)

    def update(self, dt):
        if getattr(self, "invincible", False):
            self.remaining -= dt
            if self.remaining <= 0:
                object.__setattr__(self, "invincible", False)
        if hasattr(self._player, "update"):
            self._player.update(dt)

    def draw(self, surface):
        if getattr(self, "invincible", False):
            try:
                r = self._player.rect.inflate(10,10)
                pygame.draw.rect(surface, (255,215,0), r, 3)
            except Exception:
                pass
        self._player.draw(surface)
