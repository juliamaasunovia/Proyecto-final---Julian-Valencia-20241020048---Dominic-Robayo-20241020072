# animacion_pelota.py
# Prueba básica de animación con pygame: una pelota que rebota
# Requisitos: pip install pygame

import pygame
import sys

# --- configuración inicial ---
WIDTH, HEIGHT = 640, 480
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prueba básica con pygame - Pelota que rebota")
clock = pygame.time.Clock()

# --- pelota ---
x, y = WIDTH // 2, HEIGHT // 2
radius = 20
vx, vy = 4, 3  # velocidad en pixeles por frame

# colores (valores RGB)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)

# --- bucle principal ---
running = True
while running:
    dt = clock.tick(FPS)  # limita a FPS y devuelve ms desde el último tick (no usado aquí)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # actualizar posición
    x += vx
    y += vy

    # rebote en paredes (cambia la dirección)
    if x - radius <= 0 or x + radius >= WIDTH:
        vx = -vx
    if y - radius <= 0 or y + radius >= HEIGHT:
        vy = -vy

    # dibujar
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), radius)
    pygame.display.flip()

pygame.quit()
sys.exit()
