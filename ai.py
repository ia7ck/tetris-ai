import time
import dataclasses
from typing import List, Dict, Tuple
import random
from game import Piece, Action, make_pieces
from tboard import Board

import abc


class Ai(abc.ABC):
    @abc.abstractmethod
    def get_action(self, board: Board, piece_set: List[Piece]) -> Action:
        pass
