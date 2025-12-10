import pygame
import sys
from settings import CLOCK, FPS, SCREEN, WIDTH, HEIGHT, FONT, WHITE
from facade import GameFacade
from level import levels
from movement_strategy import NormalMovement, SlowMovement, InvertedMovement
from observer import EventBus
from enemy_strategy import AggressiveStrategy, RandomStrategy
from decorators import SpeedDecorator

def show_victory(screen, seconds=3.0):
    t0 = pygame.time.get_ticks()
    ms = int(seconds * 1000)
    showing = True
    while showing:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                showing = False

        screen.fill((8, 8, 8))
        big = pygame.font.Font(None, 96)
        text = big.render("¡HAS GANADO!", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(text, rect)

        small = pygame.font.Font(None, 28)
        sub = small.render("Gracias por jugar", True, (200, 200, 200))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()
        CLOCK.tick(FPS)
        if pygame.time.get_ticks() - t0 >= ms:
            showing = False

def draw_strategy_info(screen, current_strategy_name):
    info_font = pygame.font.Font(None, 26)
    text1 = info_font.render(
        "Presiona [1] Normal | [2] Lento | [3] Invertido", True, WHITE
    )
    text2 = info_font.render(
        f"Modo de movimiento actual: {current_strategy_name}", True, WHITE
    )

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT - 60))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT - 35))


def main():
    pygame.display.set_caption("The Hardest Game - All Patterns Integrated")
    facade = GameFacade()
    facade.start(0)

    # attach EventBus
    bus = EventBus()
    g = facade.get_game()
    g.event_bus = bus

    # subscribe handlers for demonstration
    bus.subscribe("player_died", lambda p: print("event: player_died", p))
    bus.subscribe("level_completed", lambda p: print("event: level_completed", p))

    # assign some strategies to demonstrate Strategy pattern
    try:
        if len(levels) > 0 and levels[0].enemies:
            levels[0].enemies[0].strategy = AggressiveStrategy()
        if len(levels) > 1 and levels[1].enemies:
            levels[1].enemies[0].strategy = RandomStrategy()
    except Exception:
        pass

    # give player a small speed boost (decorator) for demonstration
    try:
        g.player = SpeedDecorator(g.player, factor=1.2, duration=5.0)
    except Exception:
        pass

    running = True
    current_strategy_name = "Normal"

    while running:
        dt = CLOCK.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    g.paused = not g.paused
                elif event.key == pygame.K_u:
                    facade.undo()
                elif event.key == pygame.K_r:
                    facade.restart()
                elif event.key == pygame.K_1:
                    facade.get_player().set_strategy(NormalMovement())
                    current_strategy_name = "Normal"
                elif event.key == pygame.K_2:
                    facade.get_player().set_strategy(SlowMovement())
                    current_strategy_name = "Lento"
                elif event.key == pygame.K_3:
                    facade.get_player().set_strategy(InvertedMovement())
                    current_strategy_name = "Invertido"

        facade.update(dt)
        facade.draw()

        draw_strategy_info(SCREEN, current_strategy_name)
        pygame.display.flip()

        if facade.get_player().level >= len(levels) - 1:
            show_victory(SCREEN, seconds=3.0)
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
import pygame
import sys
from settings import CLOCK, FPS, SCREEN, WIDTH, HEIGHT, FONT, WHITE
from facade import GameFacade
from level import levels
from movement_strategy import NormalMovement, SlowMovement, InvertedMovement
from observer import EventBus
from enemy_strategy import AggressiveStrategy, RandomStrategy
from decorators import SpeedDecorator

def show_victory(screen, seconds=3.0):
    t0 = pygame.time.get_ticks()
    ms = int(seconds * 1000)
    showing = True
    while showing:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                showing = False

        screen.fill((8, 8, 8))
        big = pygame.font.Font(None, 96)
        text = big.render("¡HAS GANADO!", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(text, rect)

        small = pygame.font.Font(None, 28)
        sub = small.render("Gracias por jugar", True, (200, 200, 200))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()
        CLOCK.tick(FPS)
        if pygame.time.get_ticks() - t0 >= ms:
            showing = False

def draw_strategy_info(screen, current_strategy_name):
    info_font = pygame.font.Font(None, 26)
    text1 = info_font.render(
        "Presiona [1] Normal | [2] Lento | [3] Invertido", True, WHITE
    )
    text2 = info_font.render(
        f"Modo de movimiento actual: {current_strategy_name}", True, WHITE
    )

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT - 60))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT - 35))


def main():
    pygame.display.set_caption("The Hardest Game - All Patterns Integrated")
    facade = GameFacade()
    facade.start(0)

    # attach EventBus
    bus = EventBus()
    g = facade.get_game()
    g.event_bus = bus

    # subscribe handlers for demonstration
    bus.subscribe("player_died", lambda p: print("event: player_died", p))
    bus.subscribe("level_completed", lambda p: print("event: level_completed", p))

    # assign some strategies to demonstrate Strategy pattern
    try:
        if len(levels) > 0 and levels[0].enemies:
            levels[0].enemies[0].strategy = AggressiveStrategy()
        if len(levels) > 1 and levels[1].enemies:
            levels[1].enemies[0].strategy = RandomStrategy()
    except Exception:
        pass

    # give player a small speed boost (decorator) for demonstration
    try:
        g.player = SpeedDecorator(g.player, factor=1.2, duration=5.0)
    except Exception:
        pass

    running = True
    current_strategy_name = "Normal"

    while running:
        dt = CLOCK.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    g.paused = not g.paused
                elif event.key == pygame.K_u:
                    facade.undo()
                elif event.key == pygame.K_r:
                    facade.restart()
                elif event.key == pygame.K_1:
                    facade.get_player().set_strategy(NormalMovement())
                    current_strategy_name = "Normal"
                elif event.key == pygame.K_2:
                    facade.get_player().set_strategy(SlowMovement())
                    current_strategy_name = "Lento"
                elif event.key == pygame.K_3:
                    facade.get_player().set_strategy(InvertedMovement())
                    current_strategy_name = "Invertido"

        facade.update(dt)
        facade.draw()

        draw_strategy_info(SCREEN, current_strategy_name)
        pygame.display.flip()

        if facade.get_player().level >= len(levels) - 1:
            show_victory(SCREEN, seconds=3.0)
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
