import abc
from typing import List
from game import Piece, Action, Board


class Ai(abc.ABC):
    @abc.abstractmethod
    def get_action(self, board: Board, piece_set: List[Piece]) -> Action:
        pass
