from settings import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H))
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.start = False
        self.font = pygame.font.Font(None, 36)
        self.boid = Boid(self)

    def run(self):
        while True:
            self.event_handle()
            self.update()
            self.draw()
            self.dt = self.clock.tick(FPS)

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start = True

    def update(self):
        pygame.display.set_caption(f"FPS:{self.clock.get_fps():.1f} MS: {self.dt}")
        if not self.start:
            return
        self.boid.update()

    def draw(self):
        self.screen.fill((100, 100, 100))
        self.boid.draw()
        pygame.display.flip()


class Boid:
    def __init__(self, app: App):
        self.app = app
        self.grid: list[list[Bird]] = [[] for _ in range(GRID_H * GRID_W)]
        self.birds: list[Bird] = [self.add_bird() for _ in range(BIRD_COUNT)]

    def add_bird(self, ipos=None, ivel=None):
        pos: vec2 = (
            vec2(uniform(EDGE_X, W - EDGE_X), uniform(EDGE_Y, H - EDGE_Y))
            if ipos is None
            else ipos
        )
        vel: vec2 = (
            vec2.from_polar((VEL_INIT, uniform(0, 360))) if ivel is None else ivel
        )
        bird = Bird(self.app, self, pos, vel)
        self.grid[bird.grid_idx].append(bird)
        return bird

    def draw(self):
        [bird.draw() for bird in self.birds]
        # self.draw_by_grid()
        # self.draw_grid()
        focus = self.birds[0]
        # self.draw_vec(focus.avg_pos, focus.avg_vel * 1000)

        FACTOR = 100000
        self.draw_vec(focus.pos, focus.cohesion * FACTOR, pygame.color.Color("red"))
        self.draw_vec(focus.pos, focus.alignment * FACTOR, pygame.color.Color("blue"))
        self.draw_vec(focus.pos, focus.seperation * FACTOR, pygame.color.Color("green"))
        self.draw_vec(focus.pos, focus.acc * FACTOR * 3, pygame.color.Color("yellow"))
        # pygame.draw.circle(
        #     self.app.screen,
        #     (255, 0, 0),
        #     (int(focus.pos.x), int(focus.pos.y)),
        #     ACC_MAX * FACTOR,
        #     1,
        # )
        pygame.draw.circle(
            self.app.screen,
            (255, 0, 0),
            (int(focus.pos.x), int(focus.pos.y)),
            RADIUS,
            1,
        )

        [bird.draw((255, 200, 0)) for bird in focus.neighbors]
        focus.draw((255, 0, 0))

    def draw_vec(self, pos: vec2, vec: vec2, color=(255, 200, 200)):
        pygame.draw.circle(self.app.screen, color, (int(pos.x), int(pos.y)), 5)
        pygame.draw.line(self.app.screen, color, pos, pos + vec)

    def draw_grid(self):
        for i, j in product(range(GRID_H), range(GRID_W)):
            pygame.draw.rect(
                self.app.screen,
                (0, 255, 0),
                (j * RADIUS, i * RADIUS, RADIUS, RADIUS),
                1,
            )

    def draw_by_grid(self):
        self.draw_grid()

        def hash_color(i):
            r = (i * 819345) % 256
            g = (i * 1310732) % 256
            b = (i * 5242895) % 256
            return r, g, b

        for i, birds in enumerate(self.grid):
            [bird.draw(hash_color(i)) for bird in birds]

    def update(self):
        [bird.update() for bird in self.birds]

        self.grid = [[] for _ in range(GRID_H * GRID_W)]
        [self.grid[bird.grid_idx].append(bird) for bird in self.birds]


class Bird:
    def __init__(self, app: App, boid: Boid, pos: vec2, vel: vec2):
        self.app = app
        self.boid = boid
        self.pos = deepcopy(pos)
        self.vel = deepcopy(vel)
        self.right = vec2(self.vel.y, -self.vel.x).normalize()

        self.acc = vec2(0, 0)
        self.seperation = vec2(0, 0)
        self.alignment = vec2(0, 0)
        self.cohesion = vec2(0, 0)

        self.avg_pos = vec2(0, 0)
        self.avg_vel = vec2(0, 0)

    def draw(self, color=(220, 220, 220)):
        pygame.draw.circle(
            self.app.screen, color, (int(self.pos.x), int(self.pos.y)), 5
        )
        self.draw_vec(self.vel * 40)

    def draw_vec(self, vec: vec2, color=(220, 220, 220)):
        pygame.draw.line(
            self.app.screen,
            color,
            (int(self.pos.x), int(self.pos.y)),
            (int(self.pos.x + vec.x), int(self.pos.y + vec.y)),
        )

    @property
    def grid_idx(self):
        return int(self.pos.y / RADIUS) * GRID_W + int(self.pos.x / RADIUS)

    @property
    def neighbors(self):
        forward = self.vel.normalize()
        idx = self.grid_idx
        for grid_i in (
            idx - 1,
            idx,
            idx + 1,
            idx - GRID_W - 1,
            idx - GRID_W,
            idx - GRID_W + 1,
            idx + GRID_W - 1,
            idx + GRID_W,
            idx + GRID_W + 1,
        ):
            grid_i %= GRID_H * GRID_W
            for bird in self.boid.grid[grid_i]:
                ds = bird.pos - self.pos
                if (
                    bird != self
                    and ds.length() < RADIUS
                    and ds.normalize().dot(forward) > 0
                ):
                    yield bird

    def update(self):

        self.vel += self.acc * self.app.dt
        self.vel.clamp_magnitude_ip(VEL_MAX)
        self.vel = (
            VEL_MIN * self.vel.normalize() if self.vel.length() < VEL_MIN else self.vel
        )
        self.right = vec2(-self.vel.y, self.vel.x).normalize()

        self.pos += self.vel * self.app.dt
        self.pos.x %= W
        self.pos.y %= H

        self.update_acc()

    def update_acc(self):
        self.calc_wall_reject()
        self.seperation = vec2(0, 0)
        self.alignment = vec2(0, 0)
        self.cohesion = vec2(0, 0)

        self.avg_pos = vec2(0, 0)
        self.avg_vel = vec2(0, 0)
        self.neighbor_count = 0

        for bird in self.neighbors:
            self.calc_seperation(bird)
            self.calc_avg_vel(bird)
            self.calc_avg_pos(bird)
            self.neighbor_count += 1
        self.calc_alignment()
        self.calc_cohesion()

        if self.seperation.length() > 0:
            self.seperation.clamp_magnitude_ip(ACC_MAX)

        self.acc = self.seperation + self.alignment + self.cohesion + self.reject_wall
        if self.acc.length() > 0:
            self.acc.clamp_magnitude_ip(ACC_MAX)

    def calc_wall_reject(self):
        STRENTH = 0.001
        if self.pos.x < EDGE_X:
            x = STRENTH
        elif self.pos.x > W - EDGE_X:
            x = -STRENTH
        else:
            x = 0

        if self.pos.y < EDGE_Y:
            y = STRENTH
        elif self.pos.y > H - EDGE_Y:
            y = -STRENTH
        else:
            y = 0
        self.reject_wall = vec2(x, y)

    def calc_seperation(self, other):
        STRENGTH = 0.05
        ds: vec2 = self.pos - other.pos
        self.seperation += ds.normalize() * STRENGTH / (ds.length() * ds.length())

    def calc_cohesion(self):
        STRENGTH = 0.001
        ds = self.avg_pos - self.pos
        dir = sign(self.vel.cross(ds)) * self.right
        co = dir * STRENGTH * ds.length() / RADIUS + ds.normalize() * STRENGTH / 100
        if co.length() > 0:
            self.cohesion = co.clamp_magnitude(ACC_MAX)

    def calc_alignment(self):
        STRENGTH = 0.002
        align = (self.avg_vel - self.vel) * STRENGTH
        if align.length() > 0:
            self.alignment = align.clamp_magnitude(ACC_MAX)

    def calc_avg_vel(self, other):
        self.avg_vel = (self.avg_vel * self.neighbor_count + other.vel) / (
            self.neighbor_count + 1
        )

    def calc_avg_pos(self, other):
        self.avg_pos = (self.avg_pos * self.neighbor_count + other.pos) / (
            self.neighbor_count + 1
        )


if __name__ == "__main__":
    pygame.init()
    App().run()
