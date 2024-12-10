import pygame

vec2 = pygame.math.Vector2

RES = W, H = 1080, 720
FPS = 200
SPRITE_BLOAT = 1.1
# Bird
BIRD_POS = (W / 6.0, H / 3.0)
BIRD_SZ = H / 15
JUMP_VEL = 600
GRAVITY = 1500
BIRD_SPRITE = pygame.image.load("Flappy-Bird/Bird.png")

# Pipe
PIPE_W = W / 6
PIPE_HW = PIPE_W / 2
PIPE_GAP = H / 3
MOVE_SPEED = W / 3
SPAWN_INT = 2
# Pipe sprite
PIPE_SPRITE = pygame.image.load("Flappy-Bird/pipe.png")
RATIO = PIPE_SPRITE.get_height() / PIPE_SPRITE.get_width()
PIPE_SPRITE_SZ = SPRITE_BLOAT * vec2(PIPE_W, PIPE_W * RATIO)
PIPE_SPRITE_HSZ = PIPE_SPRITE_SZ / 2


def step(e0, e1, x):
    x = max(0, min(1, (x - e0) / (e1 - e0)))
