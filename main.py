import sys, random
from typing import List
import game
import graphic
import ai.monte_carlo
import ai.cost_func_ai
import ai.ga


class Tetris:
    def __init__(self):
        self.board = game.Board()
        # self.ai: ai.Ai # 気持ち
        self.gui: graphic.Graphic
        self.score = 0

    def play(self):
        print("[start]")
        self.run()

    def run(self):
        given_piece_set = random.choice(game.pieces)
        action = self.ai.get_action(self.board, given_piece_set)
        can_put = self.board.proceed(action)
        self.gui.field.draw(self.board)
        if not can_put:
            self.tear_down(action)
            return
        wait_time = 100
        rm_line_num = self.board.resolve()
        self.score += game.SCORES[rm_line_num]
        if rm_line_num > 0:
            wait_time += 200
        self.gui.after(wait_time, self.run)

    def tear_down(self, action: game.Action):
        print("[end]")
        print("can't put the piece with x = {}:".format(action.x0))
        print(action.piece)
        print("score : {}".format(self.score))


def main():
    tetris = Tetris()
    tetris.ai = ai.cost_func_ai.CostFuncAi()
    tetris.ai.coefficients = ai.ga.Ga.solve(population_size=2, gen_limit=0)
    tetris.gui = graphic.Graphic(tetris.board)
    tetris.play()
    tetris.gui.mainloop()


if __name__ == "__main__":
    main()
