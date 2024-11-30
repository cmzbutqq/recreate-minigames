from settings import *
import pygame
from random import randrange


class App:
    """The main class of the game"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((RES_W, RES_H))
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks()
        self.snake = [self.random_pos()]
        self.walls = []
        self.walls = [self.valid_randpos() for _ in range(WALL_COUNT)]
        self.food = self.valid_randpos()
        self.forward = 0, 0

    def random_pos(self) -> vec2:
        return vec2(randrange(0, W), randrange(0, H))

    def valid_randpos(self) -> vec2:
        pos = self.random_pos()
        while pos in self.snake or pos in self.walls:
            pos = self.random_pos()
        return pos

    def run(self):
        while True:
            self.event_handle()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.forward != vec2(0, 1):
                    self.forward = vec2(0, -1)
                if event.key == pygame.K_s and self.forward != vec2(0, -1):
                    self.forward = vec2(0, 1)
                if event.key == pygame.K_a and self.forward != vec2(1, 0):
                    self.forward = vec2(-1, 0)
                if event.key == pygame.K_d and self.forward != vec2(-1, 0):
                    self.forward = vec2(1, 0)

    def update(self):
        if pygame.time.get_ticks() - self.time > tick_interval(len(self.snake)):
            self.time = pygame.time.get_ticks()
            self.snake.insert(0, self.snake[0] + self.forward)
            if self.snake[0] in self.snake[1:] and self.forward != vec2(
                0, 0
            ):  # self collision
                self.__init__()
                return
            if self.snake[0] in self.walls:  # wall collision
                self.__init__()
                return
            if (
                self.snake[0][0] < 0
                or self.snake[0][0] >= W
                or self.snake[0][1] < 0
                or self.snake[0][1] >= H
            ):  # out of bound
                if BOUNDARY_WALL:
                    self.__init__()
                    return
                else:
                    self.snake[0] = vec2(self.snake[0][0] % W, self.snake[0][1] % H)
            if self.snake[0] == self.food:
                self.food = self.valid_randpos()
            else:
                self.snake.pop()

    def draw_rect(self, pos: vec2, color):
        pygame.draw.rect(
            self.screen,
            color,
            (
                pos[0] * BLOCK_SZ + EDGE,
                pos[1] * BLOCK_SZ + EDGE,
                BLOCK_SZ - EDGE * 2,
                BLOCK_SZ - EDGE * 2,
            ),
        )

    def draw(self):
        self.screen.fill(BG_COLOR)

        self.draw_rect(self.food, FOOD_COLOR)
        score_img = pygame.font.Font(None, BLOCK_SZ).render(
            f"{len(self.snake) - 1}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(score_img, (0, 0))
        self.draw_rect(self.snake[0], HEAD_COLOR)
        [self.draw_rect(body, BODY_COLOR) for body in self.snake[1:]]
        [self.draw_rect(wall, WALL_COLOR) for wall in self.walls]

        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
    pygame.quit()
