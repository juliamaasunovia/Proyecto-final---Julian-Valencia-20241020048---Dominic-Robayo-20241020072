import pygame
import math
import os
from settings import BLUE, WIDTH

class EnemyState:
    def update(self, enemy, dt):
        raise NotImplementedError

# ---------------- PATRULLA LINEAL ----------------
class PatrolState(EnemyState):
    def update(self, enemy, dt):
        tx, ty = enemy.targets[enemy.target_index]
        dx, dy = tx - enemy.x, ty - enemy.y
        dist = (dx**2 + dy**2)**0.5

        if dist < enemy.speed * dt:
            enemy.x, enemy.y = tx, ty
            enemy.target_index = (enemy.target_index + 1) % len(enemy.targets)
        else:
            enemy.x += (dx / dist) * enemy.speed * dt
            enemy.y += (dy / dist) * enemy.speed * dt

# ---------------- SENO ----------------
class SineState(EnemyState):
    def __init__(self):
        self.t = 0

    def update(self, enemy, dt):
        self.t += dt
        enemy.x += enemy.direction * enemy.speed * dt
        enemy.y = enemy.base_y + enemy.amplitude * math.sin(self.t * enemy.frequency)

        if enemy.x < enemy.bounds[0] or enemy.x > enemy.bounds[1]:
            enemy.direction *= -1

# ---------------- PATRULLA RÁPIDA ----------------
class FastState(EnemyState):
    def update(self, enemy, dt):
        tx, ty = enemy.targets[enemy.target_index]
        dx, dy = tx - enemy.x, ty - enemy.y
        dist = (dx**2 + dy**2)**0.5

        if dist < enemy.speed * dt * 2:
            enemy.x, enemy.y = tx, ty
            enemy.target_index = (enemy.target_index + 1) % len(enemy.targets)
        else:
            enemy.x += (dx / dist) * enemy.speed * 2 * dt
            enemy.y += (dy / dist) * enemy.speed * 2 * dt

# ---------------- NUEVO: PATRULLA EN CUADRADO ----------------
class SquareState(EnemyState):
    """
    Sigue una ruta cuadrada:
    targets = [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
    """
    def update(self, enemy, dt):
        tx, ty = enemy.targets[enemy.target_index]
        dx, dy = tx - enemy.x, ty - enemy.y
        dist = (dx**2 + dy**2)**0.5

        if dist < enemy.speed * dt:
            enemy.x, enemy.y = tx, ty
            enemy.target_index = (enemy.target_index + 1) % len(enemy.targets)
        else:
            enemy.x += (dx / dist) * enemy.speed * dt
            enemy.y += (dy / dist) * enemy.speed * dt

# ---------------- ENEMIGO (con sprite animado) ----------------
class Enemy:
    # Variables de clase para almacenar frames una sola vez
    _frames = None
    _num_frames = 8  # spritesheet horizontal con 8 frames
    _frame_width = None
    _frame_height = None

    def __init__(self, x, y, radius=10, speed=100, state=None):
        # --- lógicamente igual que antes ---
        self.x = x
        self.y = y
        self.base_y = y
        self.radius = radius
        self.speed = speed
        self.state = state or PatrolState()
        self.targets = []
        self.target_index = 0

        self.amplitude = 30
        self.frequency = 2
        self.bounds = (0, WIDTH)
        self.direction = 1
        # -------------------------------------

        # --- animación ---
        self.anim_time = 0.0
        self.anim_speed = 12.0  # frames por segundo de la animación (ajustable)
        self.current_frame_index = 0

        # cargamos frames del spritesheet UNA vez (clase)
        if Enemy._frames is None:
            self._load_frames()

        # crear versiones escaladas de los frames para esta instancia,
        # usando radius para calcular el tamaño visual
        if Enemy._frames:
            size = max(1, int(self.radius * 2))
            # asegurar que cada frame es una Surface escalada a (size, size)
            self.frames_scaled = [
                pygame.transform.smoothscale(frame, (size, size))
                for frame in Enemy._frames
            ]
        else:
            # si no hay frames (no se encontró el archivo), usamos None y fallback en draw
            self.frames_scaled = None

    def _load_frames(self):
        """
        Intenta cargar assets/sprites/fuego.png (o rutas alternativas).
        Corta el spritesheet horizontal en _num_frames frames.
        """
        possible_paths = [
            os.path.join("assets", "sprites", "fuego.png"),
            "/mnt/data/fuego.png",
            "fuego.png"
        ]

        sheet = None
        for p in possible_paths:
            try:
                sheet = pygame.image.load(p).convert_alpha()
                break
            except Exception:
                sheet = None

        if sheet is None:
            # no se encontró el archivo: dejamos _frames en None para usar fallback
            Enemy._frames = None
            Enemy._frame_width = None
            Enemy._frame_height = None
            # opcional: mensaje en consola para debugging
            print("⚠️ enemy.py: no se encontró 'fuego.png'. Se usará el fallback (círculo).")
            return

        w, h = sheet.get_size()
        # calcular ancho de frame (entero)
        Enemy._frame_width = w // Enemy._num_frames
        Enemy._frame_height = h

        Enemy._frames = []
        for i in range(Enemy._num_frames):
            rect = pygame.Rect(i * Enemy._frame_width, 0, Enemy._frame_width, Enemy._frame_height)
            # subsurface devuelve una referencia; para mayor seguridad copiamos cada frame
            frame_surf = pygame.Surface((Enemy._frame_width, Enemy._frame_height), pygame.SRCALPHA)
            frame_surf.blit(sheet, (0, 0), rect)
            Enemy._frames.append(frame_surf)

    def update(self, dt):
        # MANTENER exactamente la lógica de movimiento / estados
        self.state.update(self, dt)

        # --- actualización de animación (solo visual) ---
        if self.frames_scaled:
            self.anim_time += dt
            frame_duration = 1.0 / float(self.anim_speed) if self.anim_speed > 0 else float('inf')
            # avanzar frames según tiempo acumulado
            while self.anim_time >= frame_duration:
                self.anim_time -= frame_duration
                self.current_frame_index = (self.current_frame_index + 1) % Enemy._num_frames

    def draw(self, surface):
        # si tenemos frames escalados, dibujamos el frame actual centrado en (x,y)
        if self.frames_scaled:
            frame = self.frames_scaled[self.current_frame_index]
            rect = frame.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(frame, rect)
        else:
            # fallback: dibujar el círculo azul como antes si el sprite no está disponible
            pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)

    def collides_with(self, rect):
        # idéntico a tu función original (no modifica la lógica)
        cx = max(rect.left, min(self.x, rect.right))
        cy = max(rect.top, min(self.y, rect.bottom))
        dx, dy = cx - self.x, cy - self.y
        return dx**2 + dy**2 < self.radius**2