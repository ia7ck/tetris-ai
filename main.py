import tkinter as tk
from typing import List
import tetromino


WINDOW_WIDTH = 480
WINDOW_HEIGHT = 960

Board = List[List[int]]
ObjectID = int  # たぶん


class Field(tk.Canvas):
    def __init__(self, master, board: Board):
        super().__init__(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.rects = self.create_rects(board)

    def create_rects(self, board: Board) -> List[List[ObjectID]]:
        row_num = len(board)
        cell_height = WINDOW_HEIGHT // row_num
        rects: List[List[ObjectID]] = [[] for r in range(row_num)]
        for r in range(row_num):
            col_num = len(board[r])
            cell_width = WINDOW_WIDTH // col_num
            for c in range(col_num):
                rect: ObjectID = self.create_rectangle(
                    cell_width * c,
                    cell_height * r,
                    cell_width * (c + 1),
                    cell_height * (r + 1),
                    fill="white",
                )
                rects[r].append(rect)
        self.place(x=0, y=0)
        return rects

    def draw(self, board):
        for r in range(len(board)):
            for c in range(len(board[r])):
                fill_color = "black" if board[r][c] else "white"
                self.itemconfigure(self.rects[r][c], fill=fill_color)


class Graphic(tk.Tk):
    def __init__(self, board: Board):
        super().__init__()
        self.title("Tetris")
        self.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.field = Field(self, board)


def bin_to_dot_sharp_str(board: Board) -> str:
    """ 
    [
        [0, 1, 1], 
        [1, 0, 1],
    ]

    =>

    .##\n
    #.#
    """
    return "\n".join("".join(["#" if x else "." for x in r]) for r in board)


class Tetris:
    # keyword-only https://note.nkmk.me/python-args-kwargs-usage/
    def __init__(self):
        self.row_num = 20
        self.col_num = 10
        self.board = [[0 for c in range(self.col_num)] for r in range(self.row_num)]
        self.pieces = tetromino.make_pieces()

        self.gui: Graphic

    def put_piece(self, x0: int, piece: tetromino.Piece) -> bool:
        assert 0 <= x0 and x0 < self.col_num
        min_distance = self.row_num - 1  # ピースの各ブロックが落下できる最小距離
        for i, row in enumerate(piece.blocks):
            for j in range(len(row)):
                if row[j]:
                    x = x0 + j
                    if x >= self.col_num:
                        return False
                    if self.board[i][x]:
                        return False
                    for y in range(i, self.row_num):
                        if self.board[y][x]:
                            min_distance = min(min_distance, y - i - 1)
                            break
                    else:  # 底まで落ちたとき
                        min_distance = min(min_distance, self.row_num - i - 1)
        assert min_distance >= 0
        for i, row in enumerate(piece.blocks):
            for j in range(len(row)):
                if row[j]:
                    self.board[i + min_distance][x0 + j] = 1
        return True

    def resolve(self) -> bool:
        line_removed = False
        for i, row in enumerate(self.board):
            if sum(row) == self.col_num:
                line_removed = True
                for ii in reversed(range(i)):
                    for j in range(len(row)):
                        self.board[ii + 1][j] = self.board[ii][j]
                for j in range(len(row)):
                    self.board[0][j] = 0  # 最上段には空行
        return line_removed

    def random_play(self):
        import random

        piece = random.choice(self.pieces)
        # piece = tetromino.Piece("X", [[1]], 1, 1) # ふつうにやると全然1列揃わないので
        x = random.randint(0, self.col_num - piece.width)
        can_put = self.put_piece(x, piece)
        self.gui.field.draw(self.board)
        if not can_put:
            print("can't put the piece with x = {}:".format(x))
            print(piece)
            return
        wait_time = 100
        if self.resolve():
            wait_time += 200
        self.gui.after(wait_time, self.random_play)


def main():
    tetris = Tetris()
    tetris.gui = Graphic(tetris.board)
    tetris.random_play()
    tetris.gui.mainloop()


if __name__ == "__main__":
    main()
