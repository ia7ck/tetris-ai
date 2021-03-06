import sys, random, argparse
from typing import List
import game
import graphic
import ai.cost_func_ai
import ai.ga


class Tetris:
    def __init__(self):
        self.board = game.Board()
        self.ai: ai.cost_func_ai.CostFuncAi
        self.gui: graphic.Graphic
        self.score = 0

    def play(self):
        print("coefficients : {}".format(self.ai.coefficients))
        self.run()

    def run(self):
        given_piece_set = random.choice(game.pieces)
        action = self.ai.get_action(self.board, given_piece_set)
        can_put = self.board.proceed(action)
        self.gui.field.draw(self.board)
        self.board.activate(action.piece.form_id)
        self.gui.after(400, self.gui.field.draw, self.board)  # 巧みな調整
        if not can_put:
            self.tear_down(action)
            return
        rm_line_num = self.board.resolve()
        self.score += game.SCORES[rm_line_num]
        self.gui.after(300 if rm_line_num else 100, self.run)  # 巧みな調整その2

    def tear_down(self, action: game.Action):
        print("score : {}".format(self.score))


def main():
    tetris = Tetris()
    tetris.ai = ai.cost_func_ai.CostFuncAi()
    parser = argparse.ArgumentParser()
    parser.add_argument("--population_size", default=6, type=int)
    parser.add_argument("--gen_limit", default=4, type=int)
    args = parser.parse_args()
    tetris.ai.coefficients = ai.ga.Ga.solve(
        population_size=args.population_size, gen_limit=args.gen_limit
    )
    tetris.gui = graphic.Graphic(tetris.board)
    tetris.play()
    tetris.gui.mainloop()


if __name__ == "__main__":
    main()
