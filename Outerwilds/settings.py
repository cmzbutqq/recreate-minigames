import pygame
from itertools import combinations

vec2 = pygame.math.Vector2

RES = W, H = 1080, 720
H_RES = H_W, H_H = W // 2, H // 2
UNIT = 1.0  # pixels
FPS = 250
G = 1.0
BOUNCE_FACTOR = 0.1
CONTROL_ACC = 20.0


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


PLANETS = [
    {
        "name": "Camera",
        "pos": vec2(0, -400),
        "vel": vec2(0, 0),
        "mass": 1,
        "radius": 20,
        "color": (0, 0, 0),
    },
    {
        "name": "Sun",
        "pos": vec2(0, 0),
        "vel": vec2(0, 0),
        "mass": 100000,
        "radius": 50,
        "color": (255, 255, 0),
    },
    {
        "name": "Mars",
        "pos": vec2(400, 0),
        "vel": vec2(0, 15),
        "mass": 1000,
        "radius": 25,
        "color": (255, 165, 0),
    },
    {
        "name": "Earth",
        "pos": vec2(200, 0),
        "vel": vec2(0, 23),
        "mass": 1000,
        "radius": 25,
        "color": (100, 255, 100),
    },
    {
        "name": "Invader",
        "pos": vec2(800, 0),
        "vel": vec2(0, 6),
        "mass": 100,
        "radius": 20,
        "color": (255, 255, 255),
    },
]
