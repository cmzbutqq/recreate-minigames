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
        self.unit = UNIT

    def run(self):
        while True:
            []
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and keys[pygame.K_s]:
            pass
        elif keys[pygame.K_w]:
            self.focus.vel.y += -CONTROL_ACC * self.dt
        elif keys[pygame.K_s]:
            self.focus.vel.y += CONTROL_ACC * self.dt
        else:
            pass

        if keys[pygame.K_a] and keys[pygame.K_d]:
            pass
        elif keys[pygame.K_a]:
            self.focus.vel.x += -CONTROL_ACC * self.dt
        elif keys[pygame.K_d]:
            self.focus.vel.x += CONTROL_ACC * self.dt
        else:
            pass

        if pygame.mouse.get_pressed()[0]:
            self.unit *= 1.01
        if pygame.mouse.get_pressed()[2]:
            self.unit /= 1.01

    def update(self):
        pygame.display.set_caption(f"FPS:{self.clock.get_fps():.1f} MS: {self.dt}")
        if not self.start:
            return

        for planet in self.solar:
            planet.acc = vec2(0, 0)
        [this.interact(other) for this, other in combinations(self.solar, 2)]
        [planet.update() for planet in self.solar]
    def draw(self):
        self.screen.fill((100, 100, 100))
        [planet.draw() for planet in self.solar]
        self.solar[1].draw_vec()

        status_text = self.font.render(
            f"pos: {self.focus.pos.x:1f} {self.focus.pos.y:1f} vel: {self.focus.vel.x:1f} {self.focus.vel.y:1f}",
            1,
            (255, 255, 255),
        )
        self.screen.blit(status_text, (0, 0))
        pygame.display.flip()


class Planet:
    def __init__(self, app: App, info):
        self.app = app
        self.pos: vec2 = info["pos"]
        self.rel_pos = self.pos
        self.vel = info["vel"]
        self.acc = vec2(0, 0)
        self.mass: float = info["mass"]
        self.radius = info["radius"]
        self.color = info["color"]

    def update(self):
        self.vel += self.acc * self.app.dt
        self.pos += self.vel * self.app.dt
        self.rel_pos = self.pos - self.app.focus.pos

    def interact(self, other):
        ds: vec2 = self.pos - other.pos
        dv: vec2 = (self.vel - other.vel) * BOUNCE_FACTOR
        rot: vec2 = sign(ds.cross(dv)) * vec2(ds.y, -ds.x).normalize() * 15

        r = ds.length()
        if r == 0 or self.mass == 0.0 or other.mass == 0.0:
            return
        if r <= self.radius + other.radius:
            # collision
            v = (self.vel * self.mass + other.vel * other.mass) / (
                self.mass + other.mass
            )
            self.vel = v - dv / 2 - rot/self.mass
            other.vel = v + dv / 2 + rot/other.mass
            s = ds.normalize() * (self.radius + other.radius) * 1.001

            self.pos = other.pos + s

            other.pos = self.pos - s
            return
        # gravity
        f = G * self.mass * other.mass / (r**3) * ds
        other.acc += f / other.mass
        self.acc += -f / self.mass

    def draw(self):
        pygame.draw.circle(
            self.app.screen,
            self.color,
            (
                self.rel_pos.x * self.app.unit + H_W,
                self.rel_pos.y * self.app.unit + H_H,
            ),
            self.radius * self.app.unit,
        )

    def draw_vec(self):
        dir = vec2(0, 0) if self.vel.length() == 0 else self.vel.normalize()

        dir2 = vec2(0, 0) if self.acc.length() == 0 else self.acc.normalize()
        pygame.draw.line(
            self.app.screen,
            self.color,
            (self.rel_pos + dir * self.radius) * self.app.unit + vec2(H_RES),
            (self.rel_pos + dir * self.radius + self.vel - self.app.focus.vel)
            * self.app.unit
            + vec2(H_RES),
        )
        pygame.draw.line(
            self.app.screen,
            (255, 0, 0),
            (self.rel_pos + dir2 * self.radius) * self.app.unit + vec2(H_RES),
            (self.rel_pos + dir2 * self.radius + self.acc - self.app.focus.acc)
            * self.app.unit
            + vec2(H_RES),
        )


if __name__ == "__main__":
    pygame.init()
    App().run()
