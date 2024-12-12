from settings import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H))
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.start = False
        self.font = pygame.font.Font(None, 36)
        self.water = Water(self)

    def run(self):
        while True:
            self.event_handle()
            self.update()
            self.draw()
            self.dt = self.clock.tick(FPS) / 100

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
        self.water.update()

    def draw(self):
        self.screen.fill((100, 100, 100))
        self.water.draw()
        pygame.display.flip()


class Water:
    def __init__(self, app: App):
        self.app = app
        self.grid: list[list[Particle]] = [[] for _ in range(GRID_H * GRID_W)]
        self.drops: list[Particle] = [
            self.add_drop(
                (vec2(divmod(idx, ceil(sqrt(DROP_COUNT)))) - vec2(H_GRID)) * TARGET
                + vec2(H_RES)
            )
            for idx in range(DROP_COUNT)
        ]

    def add_drop(self, ipos=None, ivel=None):
        pos: vec2 = (
            vec2(uniform(EDGE_X, W - EDGE_X), uniform(EDGE_Y, H - EDGE_Y))
            if ipos is None
            else ipos
        )
        vel: vec2 = (
            vec2.from_polar((VEL_INIT, uniform(0, 360))) if ivel is None else ivel
        )
        drop = Particle(self.app, self, pos, vel)
        self.grid[drop.grid_idx].append(drop)
        return drop

    def draw(self):
        [drop.draw() for drop in self.drops]
        # self.draw_by_grid()
        # self.draw_grid()
        focus = self.drops[DROP_COUNT // 2]

        FACTOR = 20
        self.draw_vec(focus.pos, focus.attract * FACTOR, pygame.color.Color("yellow"))
        self.draw_vec(focus.pos, focus.attract * FACTOR, pygame.color.Color("white"))
        self.draw_vec(focus.pos, focus.acc * FACTOR, pygame.color.Color("black"))
        pygame.draw.circle(
            self.app.screen,
            (255, 0, 0),
            (int(focus.pos.x), int(focus.pos.y)),
            ACC_MAX * FACTOR,
            1,
        )
        pygame.draw.circle(
            self.app.screen,
            (255, 0, 0),
            (int(focus.pos.x), int(focus.pos.y)),
            RADIUS,
            1,
        )

        [drop.draw((255, 200, 0)) for drop in focus.neighbors]
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

        for i, drops in enumerate(self.grid):
            [drop.draw(hash_color(i)) for drop in drops]

    def update(self):
        [drop.update() for drop in self.drops]

        self.grid = [[] for _ in range(GRID_H * GRID_W)]
        [self.grid[drop.grid_idx].append(drop) for drop in self.drops]


class Particle:
    def __init__(self, app: App, water: Water, pos: vec2, vel: vec2):
        self.app = app
        self.water = water
        self.pos = deepcopy(pos)
        self.vel = deepcopy(vel)
        self.right = normal(vec2(self.vel.y, -self.vel.x))

        self.acc = vec2(0, 0)
        self.attract = vec2(0, 0)
        self.attract = vec2(0, 0)

    def draw(self, color=(220, 220, 220)):
        pygame.draw.circle(
            self.app.screen, color, (int(self.pos.x), int(self.pos.y)), 5
        )
        # self.draw_vec(self.vel)

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
        forward = normal(self.vel)
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
            for drop in self.water.grid[grid_i]:
                ds = drop.pos - self.pos
                if drop != self and ds.length() < RADIUS:
                    yield drop

    def update(self):

        self.vel += self.acc * self.app.dt
        clamp_ip(self.vel, VEL_MAX)
        self.right = normal(vec2(-self.vel.y, self.vel.x))

        self.pos += self.vel * self.app.dt
        self.pos.x %= W
        self.pos.y %= H

        self.update_dynamics()

    def update_dynamics(self):
        self.calc_wall_collide()
        self.attract = vec2(0, 0)
        self.attract = vec2(0, 0)
        for drop in self.neighbors:
            self.calc_repulsion(drop)
            self.calc_attract(drop)
        self.calc_damp()
        self.acc = self.attract + self.attract
        clamp_ip(self.acc, ACC_MAX)
        self.acc.y += GRAVITY

    def calc_damp(self):
        self.vel *= DAMP**self.app.dt
        clamp_ip(self.vel, VEL_MAX)

    def calc_wall_collide(self):
        if self.pos.x < EDGE_X:
            self.vel.x = abs(self.vel.x)
            self.pos.x = EDGE_X
        elif self.pos.x > W - EDGE_X:
            self.vel.x = -abs(self.vel.x)
            self.pos.x = W - EDGE_X

        if self.pos.y < EDGE_Y:
            self.vel.y = abs(self.vel.y)
            self.pos.y = EDGE_Y
        elif self.pos.y > H - EDGE_Y:
            self.vel.y = -abs(self.vel.y)
            self.pos.y = H - EDGE_Y

    def calc_repulsion(self, other):
        STRENGTH = 10000
        ds: vec2 = self.pos - other.pos
        if ds.length() < TARGET:
            self.attract += (
                normal(ds) * STRENGTH * (max(ds.length(), 0.01) ** -2 - TARGET**-2)
            )

    def calc_attract(self, other):
        STRENGTH = 1
        ds: vec2 = self.pos - other.pos
        if ds.length() > TARGET:
            r=max(ds.length()-TARGET,0.01)
            self.attract += (
                -normal(ds) * STRENGTH * min(1,r**-2)
            )


if __name__ == "__main__":
    pygame.init()
    App().run()
