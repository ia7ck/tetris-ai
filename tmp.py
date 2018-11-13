import copy, sys
from ai.abs_ai import Ai
from game import Piece, Action, Board


class CostFuncAi(Ai):
    def __init__(self):
        self.coefficients = []

    def get_action(self, board, piece_set):
        best_action = Action(None, None)
        min_cost = sys.maxsize
        for piece in piece_set:
            for x in range(board.col_num - piece.width + 1):
                action = Action(x, piece)
                before_board, after_board = copy.deepcopy(board), copy.deepcopy(board)
                can_put = after_board.proceed(action)
                if can_put:
                    tmp_cost = self.calc(before_board, after_board)
                else:
                    tmp_cost = sys.maxsize - 1
                if tmp_cost < min_cost:
                    min_cost = tmp_cost
                    best_action = action
        assert min_cost < sys.maxsize
        return best_action

    def calc(self, before_board, after_board):
        cost = 0
        rm_line_num = after_board.resolve()
        for c, x in zip(
            self.coefficients,
            [
                rm_line_num * rm_line_num,
                after_board.count_dead() - before_board.count_dead(),
                after_board.adj_diff_sum() - before_board.adj_diff_sum(),
            ],
        ):
            cost += c * x
        return cost
