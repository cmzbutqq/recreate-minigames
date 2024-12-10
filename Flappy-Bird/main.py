from settings import *
from game import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H))
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.start = False
        self.game_over = False
        self.score = 0
        self.bird = Bird(self, BIRD_POS)
        self.pipes = Pipes(self)
        self.font = pygame.font.Font(None, 36)

    def run(self):
        while True:
            self.event_handle()
            self.update()
            self.draw()
            self.dt = self.clock.tick(FPS) / 1000

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start = True
                self.bird.jump()

    def update(self):
        if not self.start:
            return
        pygame.display.set_caption(
            f"Flappy Bird | PipeCount: {len(self.pipes.pipes)} | score: {self.score} |  birdpos: {self.bird.pos.y} | dt: {self.dt}"
        )
        self.bird.update(self.dt)
        self.pipes.update(self.dt)
        if self.game_over:
            self.game_over_screen()

    def draw(self):
        self.screen.fill((135, 206, 235))
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))
        self.bird.draw()
        self.pipes.draw()
        pygame.display.flip()

    def game_over_screen(self):
        # draw title
        message_surface = self.font.render(
            f"Game Over | Score: {self.score}", True, (255, 255, 255)
        )
        self.screen.blit(
            message_surface,
            (
                W / 2 - message_surface.get_width() / 2,
                H / 2 - message_surface.get_height() / 2,
            ),
        )
        # draw restart button
        restart_surface = self.font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(
            restart_surface,
            (
                W / 2 - restart_surface.get_width() / 2,
                H / 2 - restart_surface.get_height() / 2 + 50,
            ),
        )
        pygame.display.flip()
        # event handle
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.__init__()
                    return


if __name__ == "__main__":
    pygame.init()
    App().run()
