import pygame
from settings import SCREEN, CLOCK, FONT, WIDTH, HEIGHT, FPS, BLACK, WHITE, GRAY, GREEN, WALL_THICK
from command import MoveCommand, RestartCommand
from player import Player, PlayerCaretaker
from level import levels
from prototype import clone_enemy

class Game:
    def __init__(self):
        # will be initialized properly in load_level
        self.player = Player(*levels[0].start)
        self.caretaker = PlayerCaretaker(self.player)
        self.caretaker.create_memento()
        self.command_history = []
        self.paused = False
        self.flash_time = 0.0
        self.flash_msg = ''
        self.event_bus = None
        # current_enemies holds runtime instances (fresh clones)
        self.current_enemies = []
        # load first level properly
        self.load_level(0)

    def push(self, cmd):
        cmd.execute()
        self.command_history.append(cmd)

    def undo(self):
        if self.command_history:
            cmd = self.command_history.pop()
            try:
                cmd.undo()
            except Exception:
                pass

    def restart(self):
        cmd = RestartCommand(self.caretaker)
        self.push(cmd)
        self.load_level(self.player.level)

    def load_level(self, idx):
        # clamp index
        idx = max(0, min(idx, len(levels)-1))
        base_level = levels[idx]
        self.player.level = idx

        # restore player start
        if getattr(base_level, 'start', None):
            self.player.x, self.player.y = base_level.start

        # recreate caretaker memento AFTER moving player
        self.caretaker.create_memento()

        # recreate enemies as fresh clones to reset positions/targets/state
        self.current_enemies = []
        for proto in getattr(base_level, 'enemies', []):
            try:
                ne = clone_enemy(proto)
            except Exception:
                # fallback: shallow copy
                from prototype import clone_enemy as fallback_clone
                ne = fallback_clone(proto)
            # ensure linear patrol state if not PatrolState
            # but restore state class from proto (proto.state.__class__)
            # clone_enemy already sets state to same class type
            ne.target_index = 0
            self.current_enemies.append(ne)

    def next_level(self):
        if self.player.level + 1 < len(levels):
            self.load_level(self.player.level + 1)
            if getattr(self, 'event_bus', None) is not None:
                try:
                    self.event_bus.publish("level_started", {"level_index": self.player.level})
                except Exception:
                    pass
        else:
            self.flash('¡Has completado todos los niveles!')
            if getattr(self, 'event_bus', None) is not None:
                try:
                    self.event_bus.publish("game_completed", {"player": self.player})
                except Exception:
                    pass

    def flash(self, msg, t=2.0):
        self.flash_time = t
        self.flash_msg = msg

    def update(self, dt):
        if self.paused:
            return

        level = levels[self.player.level]

        # input -> continuous movement
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.player.SPEED * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.player.SPEED * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.player.SPEED * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.player.SPEED * dt

        if dx != 0.0 or dy != 0.0:
            self.push(MoveCommand(self.player, dx, dy))

        self.player.update_rect()

        # walls collision
        for w in getattr(level, 'walls', []):
            if self.player.rect.colliderect(w):
                self.caretaker.restore()
                self.load_level(self.player.level)
                self.flash('¡Pared!')
                if getattr(self, 'event_bus', None) is not None:
                    try:
                        self.event_bus.publish("player_hit_wall", {"player": self.player, "level": self.player.level})
                    except Exception:
                        pass
                return

        # enemies update & collision (use current_enemies)
        for e in list(self.current_enemies):
            # allow strategy to decide
            if hasattr(e, 'strategy') and getattr(e, 'strategy', None) is not None:
                try:
                    e.strategy.decide(e, (self.player.x, self.player.y), level)
                except Exception:
                    pass

            e.update(dt)

            if e.collides_with(self.player.rect):
                # if player has invincible attribute, ignore
                if getattr(self.player, 'invincible', False):
                    continue
                # restore player and **recreate enemies** by reloading level
                self.caretaker.restore()
                self.load_level(self.player.level)
                self.flash('¡Te golpearon!')
                if getattr(self, 'event_bus', None) is not None:
                    try:
                        self.event_bus.publish("player_died", {"player": self.player, "enemy": e, "level": self.player.level})
                    except Exception:
                        pass
                return

        # goal
        if getattr(level, 'goal', None) is not None:
            if self.player.rect.colliderect(level.goal):
                self.flash('¡Nivel completado!')
                if getattr(self, 'event_bus', None) is not None:
                    try:
                        self.event_bus.publish("level_completed", {"level_index": self.player.level, "player": self.player})
                    except Exception:
                        pass
                self.next_level()

        # flash tick
        if self.flash_time > 0:
            self.flash_time -= dt
            if self.flash_time <= 0:
                self.flash_msg = ''

    def draw(self):
        level = levels[self.player.level]
        SCREEN.fill(BLACK)

        for w in getattr(level, 'walls', []):
            pygame.draw.rect(SCREEN, GRAY, w)

        if getattr(level, 'goal', None) is not None:
            pygame.draw.rect(SCREEN, GREEN, level.goal)

        for e in list(self.current_enemies):
            e.draw(SCREEN)

        if hasattr(self.player, 'draw'):
            self.player.draw(SCREEN)

        hud = FONT.render(f'Nivel: {self.player.level+1} / {len(levels)}   Comandos: {len(self.command_history)}   P: pausa  U: deshacer  R: reiniciar', True, WHITE)
        SCREEN.blit(hud, (10, 10))

        if self.flash_msg:
            txt = FONT.render(self.flash_msg, True, WHITE)
            SCREEN.blit(txt, (WIDTH//2 - txt.get_width()//2, 40))

        pygame.display.flip()
