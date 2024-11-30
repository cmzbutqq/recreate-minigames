"""Static Settings"""

import pygame

vec2 = pygame.math.Vector2

# world
SZ = W, H = 25, 20
WALL_COUNT = 5
BOUNDARY_WALL = False


# speed
def tick_interval(l):  # update interval in ms
    # each time you get a food, the speed will be multiplied by this factor
    ACC_FACTOR = 1.1
    BEG, END = 300, 100
    return max(END, BEG / (ACC_FACTOR**l))


FPS = 144

# resolution
BLOCK_SZ, EDGE = 50, 2
RES = RES_W, RES_H = W * BLOCK_SZ, H * BLOCK_SZ
# colors
BG_COLOR = pygame.Color(10, 10, 20)
WALL_COLOR = pygame.Color("gray")
FOOD_COLOR = pygame.Color("cyan")
BODY_COLOR = pygame.Color("brown")
HEAD_COLOR = pygame.Color("magenta")
