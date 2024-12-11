from settings import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.start = False
        self.font = pygame.font.Font(None, 36)

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
        ...

    def draw(self):
        self.screen.fill((100, 100, 100))
        ...
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    App().run()
