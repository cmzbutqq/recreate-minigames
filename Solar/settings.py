import pygame
from itertools import combinations,product

vec2 = pygame.math.Vector2

RES = W, H = 1080, 720
H_W,H_H = W//2, H//2
UNIT = 2 # pixels
FPS = 60
G = 1.0   

PLANETS = [
    {
        "name": "Camera",
        "pos": vec2(0, 0),
        "vel": vec2(0, 0),
        "mass": 0,
        "radius": 0,
        "color": (255, 255, 0),
    },
    {
        "name": "Sun",
        "pos": vec2(0, 0),
        "vel": vec2(0, 0),
        "mass": 10000,
        "radius": 10,
        "color": (255, 255, 0),
    },
    {
        "name": "Earth",
        "pos": vec2(50, 0),
        "vel": vec2(0, 15),
        "mass": 1000,
        "radius": 2,
        "color": (100, 255, 100),
    },
    {
        "name": "Mars",
        "pos": vec2(100, 0),
        "vel": vec2(0, 12),
        "mass": 500,
        "radius": 4,
        "color": (255, 165, 0),
    },
    {
        "name": "Moon",
        "pos": vec2(60, 0),
        "vel": vec2(0, 15),
        "mass": 10,
        "radius": 1,
        "color": (255, 255, 255),
    },
]
