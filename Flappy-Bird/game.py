from settings import *
from random import randint


class Bird:

    def __init__(
        self,
        app,
        pos: tuple = BIRD_POS,
    ):
        self.app = app
        self.pos: vec2 = vec2(*pos)
        self.vel: vec2 = vec2(0, 0)
        self.angle = 0

        self.SZ, self.JUMP_VEL = BIRD_SZ, JUMP_VEL
        self.sprite = pygame.transform.scale(BIRD_SPRITE, (self.SZ, self.SZ))
        self.collider = pygame.Rect(self.pos + vec2(self.SZ / 3), vec2(self.SZ / 1.8))

    def draw(self):
        self.app.screen.blit(self.sprite, self.pos)
        self.draw_collider()

    def draw_collider(self):
        pygame.draw.rect(self.app.screen, (255, 255, 0), self.collider, 3)

    def jump(self):
        self.vel.y = -self.JUMP_VEL

    def update(self, dt):
        self.vel.y += GRAVITY * dt
        self.pos += self.vel * dt
        self.collider = pygame.Rect(self.pos + vec2(self.SZ / 3), vec2(self.SZ / 1.8))
        # death check
        center_y = self.pos.y + self.SZ / 2
        if center_y > H or center_y < 0:
            self.app.game_over = True


class Pipe:
    def __init__(
        self,
        app,
        pos: vec2 = vec2(0, 0),
    ):
        self.app = app
        self.pos: vec2 = pos
        self.vel: vec2 = vec2(-MOVE_SPEED, 0)

        self.sprite = pygame.transform.scale(
            PIPE_SPRITE,
            PIPE_SPRITE_SZ,
        )
        self.triggered = False

        self.trigger = pygame.Rect(self.pos, vec2(PIPE_W, PIPE_GAP))
        self.upper = pygame.Rect((self.pos.x, 0), vec2(PIPE_W, self.pos.y))
        self.lower = pygame.Rect(
            (self.pos.x, self.pos.y + PIPE_GAP), vec2(PIPE_W, H - self.pos.y - PIPE_GAP)
        )

    def draw(self):
        center_x = self.pos.x + PIPE_HW
        upper_center_y, lower_center_y = (
            self.pos.y - PIPE_HW * RATIO,
            self.pos.y + PIPE_GAP + PIPE_HW * RATIO,
        )

        upper = vec2(center_x, upper_center_y) - PIPE_SPRITE_HSZ
        lower = vec2(center_x, lower_center_y) - PIPE_SPRITE_HSZ

        self.app.screen.blit(self.sprite, upper)
        self.app.screen.blit(pygame.transform.flip(self.sprite, False, True), lower)

        self.draw_collider()

    def draw_collider(self):
        pygame.draw.rect(self.app.screen, (0, 255, 0), self.trigger, 3)
        pygame.draw.rect(self.app.screen, (255, 255, 0), self.upper, 3)
        pygame.draw.rect(self.app.screen, (255, 255, 0), self.lower, 3)

    def update(self, dt):
        self.pos += self.vel * dt
        self.trigger = pygame.Rect(self.pos, vec2(PIPE_W, PIPE_GAP))
        self.upper = pygame.Rect((self.pos.x, 0), vec2(PIPE_W, self.pos.y))
        self.lower = pygame.Rect(
            (self.pos.x, self.pos.y + PIPE_GAP), vec2(PIPE_W, H - self.pos.y - PIPE_GAP)
        )


class Pipes:
    def __init__(self, app):
        self.app = app
        self.spawn_interval = SPAWN_INT
        self.timer = 0
        self.pipes: list[Pipe] = []

    def draw(self):
        [pipe.draw() for pipe in self.pipes]

    def update(self, dt):
        for pipe in reversed(self.pipes):
            pipe.update(dt)
            # score check
            if not pipe.triggered and self.app.bird.collider.colliderect(pipe.trigger):
                pipe.triggered = True
                self.app.score += 1
            # death check
            if self.app.bird.collider.colliderect(
                pipe.upper
            ) or self.app.bird.collider.colliderect(pipe.lower):
                self.app.game_over = True
            # remove
            if pipe.pos.x < -PIPE_SPRITE_SZ.x:
                self.pipes.remove(pipe)
                del pipe
        # spawn
        self.timer += dt
        if self.timer > self.spawn_interval:
            self.timer = 0
            self.pipes.append(
                Pipe(
                    self.app,
                    vec2(W + PIPE_SPRITE_SZ.x, randint(0, H - PIPE_GAP)),
                )
            )
