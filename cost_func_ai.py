from typing import List
import copy
import sys
from ai import Ai
from game import Piece, Action
from tboard import Board


class CostFuncAi(Ai):
    def get_action(self, board: Board, piece_set: List[Piece]) -> Action:
        best_action: Action
        min_cost = sys.maxsize
        for piece in piece_set:
            for x in range(board.col_num - piece.width + 1):
                action = Action(x, piece)
                tmp_board = copy.deepcopy(board)
                can_put = tmp_board.proceed(action)
                tmp_cost = self.calc(tmp_board) if can_put else sys.maxsize - 1
                if tmp_cost < min_cost:
                    min_cost = tmp_cost
                    best_action = action
        assert min_cost < sys.maxsize
        return best_action

    def calc(self, board: Board) -> int:
        cost = 0
        rm_line_num = board.resolve()
        cost -= rm_line_num * rm_line_num
        cost += board.count_dead()
        cost += board.max_height()
        return cost
