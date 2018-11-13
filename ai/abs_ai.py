import abc
from game import Piece, Action, Board


class Ai(abc.ABC):
    @abc.abstractmethod
    def get_action(self, board, piece_set):
        pass
