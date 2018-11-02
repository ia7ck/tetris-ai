import tkinter as tk
from typing import List
import tetromino
import tboard
import ai

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 960


class Graphic(tk.Tk):
    def __init__(self, board: tboard.Board):
        super().__init__()
        self.title("Tetris")
        self.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.field = tboard.Field(self, board)


def bin_to_dot_sharp_str(board: tboard.Board) -> str:
    """ 
    [
        [0, 1, 1], 
        [1, 0, 1],
    ]

    =>

    .##\n
    #.#
    """
    return "\n".join("".join(["#" if x else "." for x in r]) for r in board.table)


class Tetris:
    # keyword-only https://note.nkmk.me/python-args-kwargs-usage/
    def __init__(self):
        self.board = tboard.Board()
        self.pieces = tetromino.make_pieces()
        self.ai = ai.Ai()
        self.gui: Graphic

    def proceed(self, action: ai.Action) -> bool:
        assert 0 <= action.x0 and action.x0 < self.board.col_num
        min_distance = self.board.row_num - 1  # ピースの各ブロックが落下できる最小距離
        for i, row in enumerate(action.piece.blocks):
            for j in range(len(row)):
                if row[j]:
                    x = action.x0 + j
                    if x >= self.board.col_num:
                        return False
                    if self.board.table[i][x]:
                        return False
                    for y in range(i, self.board.row_num):
                        if self.board.table[y][x]:
                            min_distance = min(min_distance, y - i - 1)
                            break
                    else:  # 底まで落ちたとき
                        min_distance = min(min_distance, self.board.row_num - i - 1)
        assert min_distance >= 0
        for i, row in enumerate(action.piece.blocks):
            for j in range(len(row)):
                if row[j]:
                    self.board.table[i + min_distance][action.x0 + j] = 1
        return True

    def resolve(self) -> int:
        removed_num = 0
        for i, row in enumerate(self.board.table):
            if sum(row) == self.board.col_num:
                removed_num += 1
                for ii in reversed(range(i)):
                    for j in range(len(row)):
                        self.board.table[ii + 1][j] = self.board.table[ii][j]
                for j in range(len(row)):
                    self.board.table[0][j] = 0  # 最上段には空行
        return removed_num

    def random_play(self):
        import random

        given_piece = random.choice(self.pieces)
        action = self.ai.get_action(self.board, given_piece)
        can_put = self.proceed(action)
        self.gui.field.draw(self.board)
        if not can_put:
            print("can't put the piece with x = {}:".format(action.x0))
            print(action.piece)
            return
        wait_time = 100
        if self.resolve() > 0:
            wait_time += 200
        self.gui.after(wait_time, self.random_play)


def main():
    tetris = Tetris()
    tetris.gui = Graphic(tetris.board)
    tetris.random_play()
    tetris.gui.mainloop()


if __name__ == "__main__":
    main()
