import pygame
from settings import WIDTH, HEIGHT, GREEN, GRAY
from enemy import Enemy, PatrolState, SineState, FastState, SquareState

WALL_THICK = 18

def r(x, y, w, h):
    return pygame.Rect(x, y, w, h)

class Level:
    def __init__(self, walls, enemies, start, goal):
        self.walls = walls
        self.enemies = enemies
        self.start = start
        self.goal = goal

levels = []

# ---------------- LEVEL 1 ----------------
# (esto permanece igual)
walls1 = [
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),

    r(180, WALL_THICK + 80, WALL_THICK, HEIGHT - (WALL_THICK + 80) - WALL_THICK),
    r(620, 0, WALL_THICK, HEIGHT - 140),
    r(200, 300, 180, WALL_THICK),
    r(420, 300, 200, WALL_THICK),
]

e1 = Enemy(260, 240, radius=21, speed=140, state=PatrolState())
e1.targets = [(220,240),(580,240),(580,320),(220,320)]

levels.append(Level(
    walls1, [e1],
    (WALL_THICK + 40, HEIGHT // 2),
    pygame.Rect(WIDTH - 100, HEIGHT // 2 - 24, 48, 48)
))

# ---------------- LEVEL 2 ----------------
# (también lo dejamos igual)
walls2 = [
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),
]

col_xs = [120, 300, 480, 660]
top_height = 180
bottom_y = 360
for x in col_xs:
    walls2.append(r(x, WALL_THICK + 20, WALL_THICK, top_height - 20))
    walls2.append(r(x, bottom_y, WALL_THICK, HEIGHT - bottom_y - WALL_THICK))

walls2.append(r(150, HEIGHT - WALL_THICK - 140, 500, WALL_THICK))

e2a = Enemy(220, 150, radius=21, speed=110, state=SineState()); e2a.bounds = (180,620)
e2b = Enemy(600, 450, radius=21, speed=120, state=FastState()); e2b.targets = [(600,450),(220,450)]
e2c = Enemy(420, 250, radius=18, speed=85, state=SineState()); e2c.bounds = (360,520)

vertical_enemies = []
vertical_positions_x = [180, 340, 520, 700]
for x in vertical_positions_x:
    ev = Enemy(x, 200, radius=18, speed=130, state=PatrolState())
    ev.targets = [(x, WALL_THICK+40), (x, HEIGHT - WALL_THICK - 60)]
    vertical_enemies.append(ev)

levels.append(Level(
    walls2,
    [e2a, e2b, e2c] + vertical_enemies,
    (WALL_THICK + 40, HEIGHT // 2),
    pygame.Rect(WIDTH - 120, HEIGHT // 2 - 24, 48, 48)
))

# ---------------- LEVEL 3 CON RECORRIDOS CUADRADOS ----------------
walls3 = [
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),
]

GAP = 160
for i in range(1, 6):
    x = 100*i
    if i % 2 == 1:
        walls3.append(r(x, WALL_THICK, WALL_THICK, HEIGHT - WALL_THICK - GAP))
    else:
        walls3.append(r(x, GAP, WALL_THICK, HEIGHT - GAP - WALL_THICK))

# NUEVOS ENEMIGOS CON CUADRADO
square1 = Enemy(150, 150, radius=18, speed=95, state=SquareState())
square1.targets = [(120,120),(380,120),(380,280),(120,280)]

square2 = Enemy(650, 500, radius=24, speed=130, state=SquareState())
square2.targets = [(620,480),(760,480),(760,580),(620,580)]

square3 = Enemy(350, 300, radius=21, speed=80, state=SquareState())
square3.targets = [(300,260),(500,260),(500,380),(300,380)]

levels.append(Level(
    walls3,
    [square1, square2, square3],
    (WALL_THICK + 40, WALL_THICK + 40),
    pygame.Rect(WIDTH - 110, HEIGHT - 110, 48, 48)
))

# ---------------- LEVEL 4 (zigzag largo + más barreras + enemigos rápidos) ----------------
walls4 = [
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),
]

# Laberinto en zigzag largo
for x in [120, 240, 360, 480, 600, 720]:
    walls4.append(r(x, WALL_THICK + 40, WALL_THICK, 220))
    walls4.append(r(x, HEIGHT - WALL_THICK - 260, WALL_THICK, 220))

walls4.append(r(140, 240, 520, WALL_THICK))
walls4.append(r(140, 360, 520, WALL_THICK))

# Enemigos
e4a = Enemy(220, 120, radius=18, speed=170, state=FastState())
e4a.targets = [(220, 120), (700, 120)]

e4b = Enemy(700, 480, radius=18, speed=170, state=FastState())
e4b.targets = [(700, 480), (220, 480)]

e4c = Enemy(380, 200, radius=20, speed=120, state=PatrolState())
e4c.targets = [(380, 200), (380, 420)]

e4d = Enemy(560, 300, radius=20, speed=130, state=SquareState())
e4d.targets = [(520, 260), (640, 260), (640, 380), (520, 380)]

levels.append(
    Level(
        walls4,
        [e4a, e4b, e4c, e4d],
        (WALL_THICK + 34, HEIGHT // 2),
        pygame.Rect(WIDTH - 120, HEIGHT // 2 - 24, 48, 48),
    )
)

# ---------------- LEVEL 5 (intercalado + curvas + enemigos de rutas cerradas) ----------------
walls5 = [
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),
]

GAP = 150
for i in range(1, 8):
    x = 90 * i
    if i % 2 == 1:
        walls5.append(r(x, WALL_THICK, WALL_THICK, HEIGHT - WALL_THICK - GAP))
    else:
        walls5.append(r(x, GAP, WALL_THICK, HEIGHT - GAP - WALL_THICK))

# Enemigos
e5a = Enemy(160, 140, radius=18, speed=120, state=SquareState())
e5a.targets = [(120, 120), (280, 120), (280, 260), (120, 260)]

e5b = Enemy(520, 180, radius=18, speed=135, state=PatrolState())
e5b.targets = [(520, 180), (520, 520)]

e5c = Enemy(680, 420, radius=20, speed=150, state=FastState())
e5c.targets = [(680, 420), (220, 420)]

levels.append(
    Level(
        walls5,
        [e5a, e5b, e5c],
        (WALL_THICK + 38, WALL_THICK + 38),
        pygame.Rect(WIDTH - 110, HEIGHT - 110, 48, 48),
    )
)


# Nivel final vacío
levels.append(Level([], [], (0,0), None))
