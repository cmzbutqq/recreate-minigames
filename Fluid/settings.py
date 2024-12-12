import pygame
from math import ceil
from copy import deepcopy
from math import radians, sin, cos, sqrt, log
from typing import Optional
from random import uniform
from itertools import product

vec2 = pygame.math.Vector2


RES = W, H = 1080, 720
H_RES = W // 2, H // 2
EDGE = EDGE_X, EDGE_Y = W // 32, H // 32
FPS = 600
GRAVITY = 10.0
BOUNCE_DAMPING = 0.8
DROP_COUNT = 500
DAMP = 0.8
TARGET = 20
RADIUS = TARGET * 2
GRID = GRID_W, GRID_H = ceil(W / RADIUS), ceil(H / RADIUS)
H_GRID = H_GRID_W, H_GRID_H = GRID_W // 2, GRID_H // 2


VEL_INIT, VEL_MAX = 1, 50  # pixel/0.1s
ACC_MAX = VEL_MAX / 1.0  # pixel/0.1s^2


def rsqrt(x):
    return 1 / sqrt(x)


def normal(vec: vec2):
    if vec.length() == 0:
        return vec2(0, 0)
    else:
        return vec.normalize()


def clamp(vec: vec2, l):
    if vec.length() == 0:
        return vec2(0, 0)
    else:
        return vec.clamp_magnitude(l)


def clamp_ip(vec: vec2, l):
    if vec.length() == 0:
        return
    else:
        vec.clamp_magnitude_ip(l)
        return


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


if __name__ == "__main__":
    print(f"{GRID_W=}\n{GRID_H=}")
