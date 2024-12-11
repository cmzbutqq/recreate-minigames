import pygame
from math import ceil
from copy import deepcopy
from math import radians, sin, cos
from typing import Optional
from random import uniform
from itertools import product

vec2 = pygame.math.Vector2


RES = W, H = 1080, 720
EDGE = EDGE_X, EDGE_Y = W // 32, H // 32
FPS = 600

BIRD_COUNT =500
RADIUS = 100
GRID = GRID_W, GRID_H = ceil(W / RADIUS), ceil(H / RADIUS)


VEL_INIT, VEL_MAX, VEL_MIN = 0.3, 1, 0.2  # pixel/ms
ACC_MAX = VEL_MAX / 400.0  # pixel/ms^2


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


if __name__ == "__main__":
    print(f"{GRID_W=}\n{GRID_H=}")
