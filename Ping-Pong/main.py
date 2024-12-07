from settings import *
from random import choice
from enum import Enum


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.start = False
        self.ball = Ball(
            self, H_WIDTH, H_HEIGHT, BALL_RADIUS, BALL_COLOR, INIT_BALL_SPEED
        )
        self.lpaddle = Paddle(
            self, 0, H_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_COLOR
        )
        self.rpaddle = Paddle(
            self,
            WIDTH - PADDLE_WIDTH,
            H_HEIGHT,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_COLOR,
        )
        self.font = pg.font.Font(None, 50)
        self.players = [Player(self, self.lpaddle)]
        self.AIs = [
            AI(self, self.rpaddle, Strat.PREDICT),
        ]

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.start = True
        [player.check_events() for player in self.players]

    def update(self):
        self.dt = self.clock.tick(250)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f} FPS, {self.dt} ms")
        if self.start:
            [ai.update() for ai in self.AIs]
            self.ball.update()
            self.lpaddle.update()
            self.rpaddle.update()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.ball.draw()
        self.lpaddle.draw()
        self.rpaddle.draw()
        [ai.draw() for ai in self.AIs]
        # draw ball.bounces count
        text = self.font.render(f"{self.ball.bounces}", True, TEXT_COLOR)
        self.screen.blit(text, (H_WIDTH, 50))

        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


class Paddle:
    def __init__(self, app, x, y, width, height, color):
        self.app = app
        self.pos = vec2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.vy = 0

    def draw(self):
        pg.draw.rect(
            self.app.screen,
            self.color,
            (self.pos.x, self.pos.y, self.width, self.height),
        )

    def update(self):
        self.pos.y += self.vy
        self.pos.y = max(self.pos.y, 0)
        self.pos.y = min(self.pos.y, HEIGHT - self.height)


class Ball:
    def __init__(self, app, x, y, radius, color, speed):
        self.app = app
        self.pos = vec2(x, y)
        self.radius = radius
        self.color = color
        self.vel = vec2(choice([-1, 1]), 0).normalize() * speed
        self.bounces = 0
        # reflection part
        self.reflect = []  # points of a polyline

    def draw(self):
        pg.draw.circle(self.app.screen, self.color, self.pos, self.radius)
        self.draw_reflect()

    def draw_reflect(self):
        if self.reflect:
            pg.draw.lines(self.app.screen, REFLECT_COLOR, False, self.reflect, 2)
        # draw reflect line

    def update(self):
        self.pos += self.vel * self.app.dt
        if (
            self.pos.x - self.radius < 0 or self.pos.x + self.radius > WIDTH
        ):  # exceed l/r bound
            self.app.__init__()
        if self.pos.y - self.radius < 0:  # exceed upper bound
            self.vel.y = abs(self.vel.y)
        if self.pos.y + self.radius > HEIGHT:  # exceed lower bound
            self.vel.y = -abs(self.vel.y)
        if self.check_collision(self.app.lpaddle) or self.check_collision(
            self.app.rpaddle
        ):
            self.bounces += 1
            self.update_reflect()

    def update_reflect(self):
        MAX_LOOP = 100
        pos, vel = self.pos.copy(), self.vel.copy()
        up, down = BALL_RADIUS, HEIGHT - BALL_RADIUS
        left = BALL_RADIUS + PADDLE_WIDTH
        right = WIDTH - left
        self.reflect = [pos.copy()]
        for _ in range(MAX_LOOP):

            if vel.y < 0:
                dy = up - pos.y
            else:
                dy = down - pos.y
            dx = dy / vel.y * vel.x
            pos += vec2(dx, dy)
            if left <= pos.x <= right:  # inbound
                self.reflect.append(pos.copy())
                vel.y *= -1
                continue
            else:  # outbound
                if vel.x < 0:
                    dx = left - pos.x
                else:
                    dx = right - pos.x
                dy = dx / vel.x * vel.y
                pos += vec2(dx, dy)
                self.reflect.append(pos.copy())
                break

    def check_collision(self, paddle):
        u, d = paddle.pos.y, paddle.pos.y + paddle.height  # up down
        l, r = paddle.pos.x, paddle.pos.x + paddle.width  # left right

        x, y = self.pos.x, self.pos.y
        # type A
        if u <= y <= d:
            if abs(x - l) < self.radius and self.vel.x > 0:  # l hit
                self.vel.x = -abs(self.vel.x)
            elif abs(x - r) < self.radius and self.vel.x < 0:  # r hit
                self.vel.x = abs(self.vel.x)
            else:  # not hit
                return False
            # additional speed depending on where you hit the paddle
            factor = 2 * (y - u) / paddle.height - 1  # range: [-1, 1]
            self.vel.y += factor * ADDITIONAL_SPEED
            # simulating friction
            self.vel.y += paddle.vy * FRICTION
            return True
        # type B
        elif l <= x <= r:
            if abs(y - u) < self.radius and self.vel.y > 0:  # upper hit
                self.vel.y = -abs(2 * paddle.vy - self.vel.y)
            elif abs(y - d) < self.radius and self.vel.y < 0:  # down hit
                self.vel.y = abs(2 * paddle.vy - self.vel.y)
            else:  # not hit
                return False
            return True
        # type C
        else:
            for corner in [vec2(l, u), vec2(l, d), vec2(r, u), vec2(r, d)]:
                normal = self.pos - corner
                if (
                    normal.length() < self.radius and self.vel.dot(normal) < 0
                ):  # corner hit
                    self.vel = self.vel.reflect(normal)
                    return True
        return False


class Player:
    def __init__(self, app, paddle, up_key=pg.K_w, down_key=pg.K_s):
        self.app = app
        self.paddle: Paddle = paddle
        self.up_key = up_key
        self.down_key = down_key

    def check_events(self):
        keys = pg.key.get_pressed()
        if keys[self.up_key] and keys[self.down_key]:
            self.paddle.vy = 0
        elif keys[self.up_key]:
            self.paddle.vy = -PADDLE_SPEED
        elif keys[self.down_key]:
            self.paddle.vy = PADDLE_SPEED
        else:
            self.paddle.vy = 0


class Strat(Enum):
    PREDICT = 1
    FOLLOW = 2


class AI(Player):
    def __init__(self, app, paddle, strat: Strat):
        super().__init__(app, paddle, pg.K_UP, pg.K_DOWN)

        self.goto_y = None
        match strat:
            case Strat.PREDICT:
                self.strat = self.strat_predict
                self.TOLERENCE = PADDLE_HEIGHT / 2.3
            case Strat.FOLLOW:
                self.strat = self.strat_follow
                self.TOLERENCE = PADDLE_HEIGHT / 6
            case _:
                raise ValueError("Invalid strat")

    def strat_predict(self):  # set self.goto_y to the predict based on reflections
        self.goto_y = (
            self.app.ball.reflect[-1].y
            if self.app.ball.reflect
            else self.app.ball.pos.y
        )

    def strat_follow(
        self,
    ):  # set self.goto_y to the y of current ball
        self.goto_y = self.app.ball.pos.y

    def act(self):
        to_y, now_y = self.goto_y, self.paddle.pos.y + PADDLE_HEIGHT / 2
        if to_y is None:
            return
        if abs(to_y - now_y) < self.TOLERENCE:
            self.paddle.vy = 0
        elif to_y > now_y:
            self.paddle.vy = PADDLE_SPEED
        else:
            self.paddle.vy = -PADDLE_SPEED

    def update(self):
        self.strat()
        self.act()

    def draw(self):
        # draw goto_y
        if self.goto_y is not None:
            pg.draw.line(
                self.app.screen,
                AI_COLOR,
                (self.paddle.pos.x - 100, self.goto_y),
                (self.paddle.pos.x + PADDLE_WIDTH + 100, self.goto_y),
                5,
            )
        # draw tolerence
        pg.draw.rect(
            self.app.screen,
            AI_COLOR,
            (
                self.paddle.pos.x,
                self.paddle.pos.y + PADDLE_HEIGHT / 2 - self.TOLERENCE,
                PADDLE_WIDTH,
                self.TOLERENCE * 2,
            ),
            5,
        )


if __name__ == "__main__":
    app = App()
    app.run()
