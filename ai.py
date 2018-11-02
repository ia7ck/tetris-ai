import dataclasses
import random
from game import Piece, Action
from tboard import Board


class Ai:
    def get_action(self, board: Board, piece: Piece) -> Action:
        return self.choose_random(board, piece)

    @staticmethod
    def choose_random(board: Board, piece: Piece) -> Action:
        x = random.randint(0, board.col_num - piece.width)
        return Action(x, piece)
