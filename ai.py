import time
import dataclasses
from typing import List, Dict, Tuple
import random
from game import Piece, Action, make_pieces
from tboard import Board


class Ai:
    memo: Dict = {}

    def arg_max(self, board: Board, piece_set: List[Piece]) -> Action:
        mx_val = 0.0
        best_pos = -1
        best_piece = piece_set[0]
        for piece in piece_set:
            state = (str(board) + str(piece)).replace("\n", "")
            for x in range(board.col_num - piece.width + 1):
                key = (state, x)
                if key in self.memo:
                    values = self.memo[key]
                    if sum(values) / len(values) > mx_val:
                        mx_val = sum(values) / len(values)
                        best_pos = x
                        best_piece = piece
        return Action(best_pos, best_piece)

    def get_action(self, board: Board, piece_set: List[Piece]) -> Action:
        best_action = self.arg_max(board, piece_set)
        if best_action.x0 < 0:
            piece = random.choice(piece_set)
            best_action = Action(random.randint(0, board.col_num - piece.width), piece)
        return best_action

    @staticmethod
    def choose_random(board: Board, piece_set: List[Piece]) -> Action:
        piece = random.choice(piece_set)
        x = random.randint(0, board.col_num - piece.width)
        return Action(x, piece)

    def learn(self, num: int):
        pieces = make_pieces()
        start_time = time.time()
        for _ in range(num):
            keys: List[Tuple[str, int]] = []
            board = Board()
            count = 0
            while True:
                given_piece_set = random.choice(pieces)
                action = self.choose_random(board, given_piece_set)
                keys.append(
                    ((str(board) + str(action.piece)).replace("\n", ""), action.x0)
                )
                can_put = board.proceed(action)
                if not can_put:
                    for key in keys:
                        if key in self.memo:
                            self.memo[key].append(0)
                        else:
                            self.memo[key] = [0]
                    break
                board.resolve()
                count += 1
                if count == 23:  # 23ターン耐えたら報酬
                    for key in keys:
                        if key in self.memo:
                            self.memo[key].append(1)
                        else:
                            self.memo[key] = [1]
                    break

        end_time = time.time()
        print("{} seconds".format(end_time - start_time))
