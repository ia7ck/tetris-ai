import tkinter as tk
from typing import List
import game
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


class Tetris:
    # keyword-only https://note.nkmk.me/python-args-kwargs-usage/
    def __init__(self):
        self.board = tboard.Board()
        self.pieces = game.make_pieces()
        self.ai = ai.Ai()
        self.gui: Graphic

    def random_play(self):
        import random

        given_piece = random.choice(self.pieces)
        action = self.ai.get_action(self.board, given_piece)
        can_put = self.board.proceed(action)
        self.gui.field.draw(self.board)
        if not can_put:
            print("can't put the piece with x = {}:".format(action.x0))
            print(action.piece)
            return
        wait_time = 100
        if self.board.resolve() > 0:
            wait_time += 200
        self.gui.after(wait_time, self.random_play)


def main():
    tetris = Tetris()
    tetris.random_play()
    tetris.gui.mainloop()


if __name__ == "__main__":
    main()
