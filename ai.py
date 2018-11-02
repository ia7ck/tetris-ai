import time
import dataclasses
from typing import List, Dict, Tuple
import random
from game import Piece, Action, make_pieces
from tboard import Board


class Ai:
    memo: Dict = {}

    def arg_max(self, board: Board, piece: Piece) -> Action:
        state = (str(board) + str(piece)).replace("\n", "")
        mx_pos = 0
        mx_val = 0.0
        for x in range(board.col_num - piece.width + 1):
            key = (state, x)
            if key in self.memo:
                values = self.memo[key]
                if sum(values) / len(values) > mx_val:
                    mx_val = sum(values) / len(values)
                    mx_pos = x
        return Action(mx_pos, piece)

    def get_action(self, board: Board, piece: Piece) -> Action:
        return self.arg_max(board, piece)

    @staticmethod
    def choose_random(board: Board, piece: Piece) -> Action:
        x = random.randint(0, board.col_num - piece.width)
        return Action(x, piece)

    def learn(self, num: int):
        pieces = make_pieces()
        start_time = time.time()
        for _ in range(num):
            keys: List[Tuple[str, int]] = []
            board = Board()
            while True:
                given_piece = random.choice(pieces)
                action = self.choose_random(board, given_piece)
                keys.append(
                    ((str(board) + str(action.piece)).replace("\n", ""), action.x0)
                )
                can_put = board.proceed(action)
                if not can_put:
                    for i, key in enumerate(keys):
                        if key in self.memo:
                            self.memo[key].append(len(keys) - i - 1)
                        else:
                            self.memo[key] = [len(keys) - i - 1]
                    break
                board.resolve()
        end_time = time.time()
        print("{} seconds".format(end_time - start_time))
