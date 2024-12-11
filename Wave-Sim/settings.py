import pygame
from itertools import product
from math import exp


def sigmoid(x: float):
    return 1 / (1 + exp(-x))


vec2 = pygame.math.Vector2

VOXEL_SIZE = 10
GRID = W, H = 100, 100
RES = RES_W, RES_H = W * VOXEL_SIZE, H * VOXEL_SIZE
FPS = 60
DAMP = .8

CONV = [  # dx,dy,w
    (-1, -1, 0.8),
    (0, -1, 1),
    (1, -1, 0.8),
    (-1, 0, 1),
    (0, 0, 1),
    (1, 0, 1),
    (-1, 1, 0.8),
    (0, 1, 1),
    (1, 1, 0.8),
]

if __name__ == "__main__":
    print(sigmoid(+1))
