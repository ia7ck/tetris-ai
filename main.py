import tkinter as tk
from typing import List
import game
import tboard
import tfield


class Graphic(tk.Tk):
    def __init__(self, board: tboard.Board):
        super().__init__()
        self.title("Tetris")
        self.geometry("{}x{}".format(game.WINDOW_WIDTH, game.WINDOW_HEIGHT))

        self.field = tfield.Field(self, board)


class Tetris:
    # keyword-only https://note.nkmk.me/python-args-kwargs-usage/
    def __init__(self):
        self.board = tboard.Board()
        self.pieces = game.make_pieces()
        # self.ai: ai.Ai # 気持ち
        self.gui: Graphic

    def play(self):
        import random

        given_piece_set = random.choice(self.pieces)
        action = self.ai.get_action(self.board, given_piece_set)
        can_put = self.board.proceed(action)
        self.gui.field.draw(self.board)
        if not can_put:
            print("can't put the piece with x = {}:".format(action.x0))
            print(action.piece)
            return
        wait_time = 100
        if self.board.resolve() > 0:
            wait_time += 200
        self.gui.after(wait_time, self.play)


def main():
    import sys
    import monte_carlo
    import cost_func_ai

    tetris = Tetris()

    tetris.ai = cost_func_ai.CostFuncAi()

    # rand_ai = monte_carlo.MonteCarlo()
    # n = 5000
    # if len(sys.argv) == 2:
    #     n = int(sys.argv[1])
    # rand_ai.learn(n)
    # tetris.ai = rand_ai

    tetris.gui = Graphic(tetris.board)
    tetris.play()
    tetris.gui.mainloop()


if __name__ == "__main__":
    main()
