import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
FONT = pygame.font.SysFont(None, 20)

# Colors
BLACK = (12, 12, 12)
WHITE = (230, 230, 230)
GRAY = (100, 100, 100)
GREEN = (30, 200, 30)
BLUE = (30, 30, 200)
RED = (200, 30, 30)
YELLOW = (255, 215, 0)

WALL_THICK = 18
