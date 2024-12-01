import pygame as pg

SZ, PAD = 400, 20
CROSS_COLOR = (0, 200, 255)
DOT_COLOR = (255, 200, 0)


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((3 * SZ, 3 * SZ))
        self.board = [
            [0 for _ in range(3)] for _ in range(3)
        ]  # 0 for empty, 1 for cross, -1 for dot
        self.curr = -1
        self.ai, self.player = [1], [-1]
        self.mouse_pos = pg.mouse.get_pos()

    def run(self):
        while True:
            self.update()
            self.draw()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.mouse_pos = pg.mouse.get_pos()
        pg.draw.circle(self.screen, (255, 0, 0), self.mouse_pos, 10)

        for i, j in product(range(3), range(3)):
            if self.board[i][j] == 1:
                # pg.draw.rect(self.screen, (255, 0, 200), (i * SZ, j * SZ, SZ, SZ))
                pg.draw.line(
                    self.screen,
                    CROSS_COLOR,
                    (i * SZ + PAD, j * SZ + PAD),
                    (i * SZ + SZ - PAD, j * SZ + SZ - PAD),
                    5,
                )
                pg.draw.line(
                    self.screen,
                    CROSS_COLOR,
                    (i * SZ + SZ - PAD, j * SZ + PAD),
                    (i * SZ + PAD, j * SZ + SZ - PAD),
                    5,
                )
            elif self.board[i][j] == -1:
                # pg.draw.rect(self.screen, (255, 200, 0), (i * SZ, j * SZ, SZ, SZ))
                pg.draw.circle(
                    self.screen,
                    DOT_COLOR,
                    (i * SZ + SZ // 2, j * SZ + SZ // 2),
                    SZ // 2 - PAD,
                    5,
                )

        pg.display.flip()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                pos = pos[0] // SZ, pos[1] // SZ
                self.player_move(pos)
        self.ai_move()

    def player_move(self, pos):
        if self.curr in self.player and self.board[pos[0]][pos[1]] == 0:
            self.board[pos[0]][pos[1]] = self.curr
            self.curr = -self.curr

    def ai_move(self):
        if self.curr in self.ai:
            _, pos = best_move(self.board, self.curr)
            if pos is None:
                return
            pg.time.delay(100)
            self.board[pos[0]][pos[1]] = self.curr
            self.curr = -self.curr


from functools import cache
from itertools import product
from copy import deepcopy


# @cache
def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    for i, j in product(range(3), range(3)):
        if board[i][j] is 0:
            return None  # not ended
    return 0  # draw


# @cache
def best_move(
    board, curr
) -> tuple[int, tuple[int, int] | None]:  # final winner, best move
    if winner(board) is not None:
        return winner(board), None

    tie = []
    lose = []
    for i, j in product(range(3), range(3)):
        if board[i][j] is 0:
            nxt_board = deepcopy(board)
            nxt_board[i][j] = curr
            res, _ = best_move(nxt_board, -curr)
            if res == curr:
                return curr, (i, j)
            elif res == 0:
                tie.append((i, j))
            elif res == -curr:
                lose.append((i, j))
            else:
                raise Exception("Invalid result")
    if tie != []:
        return 0, tie[0]
    if lose != []:
        return -curr, lose[0]
    raise Exception("Can't win, lose, nor tie")


if __name__ == "__main__":
    app = App()
    app.run()
