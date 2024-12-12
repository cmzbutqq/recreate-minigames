from settings import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.start = False
        self.font = pygame.font.Font(None, 36)
        self.solar: list[Planet] = [Planet(self, info) for info in PLANETS]
        self.focus = self.solar[0]

    def run(self):
        while True:
            self.event_handle()
            self.update()
            self.draw()
            self.dt = self.clock.tick(FPS) / 100.0

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
        [planet.update() for planet in self.solar]
        [me.interact(other) for me, other in combinations(self.solar, 2)]

    def draw(self):
        self.screen.fill((100, 100, 100))
        [planet.draw() for planet in self.solar]
        pygame.display.flip()


class Planet:
    def __init__(self, app: App, info):
        self.app = app
        self.pos: vec2 = info["pos"]
        self.rel_pos = self.pos
        self.vel = info["vel"]
        self.mass: float = info["mass"]
        self.radius = info["radius"]
        self.color = info["color"]

    def update(self):
        self.pos += self.vel * self.app.dt
        self.rel_pos = self.pos - self.app.focus.pos

    def interact(self, other):
        ds: vec2 = self.pos - other.pos
        r = ds.length()
        if r == 0 or self.mass == 0.0 or other.mass == 0.0:
            return
        if r <= self.radius + other.radius:
            # collision
            pass
        # gravity
        f = G * self.mass * other.mass / (r**3) * ds
        other.vel += f / other.mass * self.app.dt
        self.vel += -f / self.mass * self.app.dt

    def draw(self):
        pygame.draw.circle(
            self.app.screen,
            self.color,
            (self.rel_pos.x * UNIT + H_W, self.rel_pos.y * UNIT + H_H),
            self.radius * UNIT,
        )


if __name__ == "__main__":
    pygame.init()
    App().run()
