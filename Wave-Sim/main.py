from settings import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.start = False
        self.font = pygame.font.Font(None, 36)
        self.grid = [[Voxel(self, (i, j)) for j in range(W)] for i in range(H)]

    def run(self):
        while True:
            self.event_handle()
            self.update()
            self.draw()
            self.dt = self.clock.tick(FPS) / 1000  # in seconds

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start = True
        if self.start:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                i,j = pos[0] // VOXEL_SIZE, pos[1] // VOXEL_SIZE
                self.grid[i][j].z += 1.0
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                i, j = pos[0] // VOXEL_SIZE, pos[1] // VOXEL_SIZE
                self.grid[i][j].z = 0.0

    def update(self):
        pygame.display.set_caption(f"FPS:{self.clock.get_fps():.1f} MS: {self.dt*1000}")
        if not self.start:
            return
        for i, j in product(range(W), range(H)):
            self.grid[i][j].update()

    def draw(self):
        self.screen.fill((100, 100, 100))
        for i, j in product(range(W), range(H)):
            color = self.grid[i][j].color()

            pygame.draw.rect(
                self.screen,
                color,
                (i * VOXEL_SIZE, j * VOXEL_SIZE, VOXEL_SIZE, VOXEL_SIZE),
            )

        pygame.display.flip()


class Voxel:
    def __init__(self, app: App, idx: tuple[int, int], z: float = 0.0, v: float = 0.0):
        self.app = app
        self.idx = idx
        self.z = z
        self.v = v
        self.a = 0.0

    def update(self):
        self.v += self.a * self.app.dt
        self.v *= DAMP**self.app.dt
        self.z += self.v * self.app.dt
        self.convolve()

    def convolve(self):
        self.a = 0.0
        for dx, dy, w in CONV:
            i, j = self.idx
            i += dx
            j += dy
            if 0 <= i < W and 0 <= j < H:
                self.a += (self.app.grid[i][j].z - self.z) * w

    def color(self):
        return (
            int(sigmoid(self.a) * 255),
            int(sigmoid(self.v) * 255),
            int(sigmoid(self.z) * 255),
        )


if __name__ == "__main__":
    pygame.init()
    App().run()
