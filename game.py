import dataclasses
from typing import List

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 960

CANVAS_WIDTH = 480
CANVAS_HEIGHT = 960

ROW_NUM = 20
COL_NUM = 10

SCORES = [0, 100, 300, 500, 800]  # https://tetris.wiki/Scoring
COLORS = [
    "white",
    "#9FD9F6",  # I
    "#FFF9B1",  # O
    "#A5D4AD",  # S
    "#F5B090",  # Z
    "#A3BCE2",  # J
    "#FCD7A1",  # L
    "#CFA7CD",  # T
]


@dataclasses.dataclass(frozen=True)
class Piece:
    form: str
    form_id: int
    blocks: List[List[int]]
    width: int
    height: int

    def __str__(self) -> str:
        return "\n".join("".join(["#" if x else "." for x in r]) for r in self.blocks)


pieces: List[List[Piece]] = [
    [Piece("I", 1, [[1, 1, 1, 1]], 4, 1), Piece("I", 1, [[1], [1], [1], [1]], 1, 4)],
    [Piece("O", 2, [[1, 1], [1, 1]], 2, 2)],
    [
        Piece("S", 3, [[0, 1, 1], [1, 1, 0]], 3, 2),
        Piece("S", 3, [[1, 0], [1, 1], [0, 1]], 2, 3),
    ],
    [
        Piece("Z", 4, [[1, 1, 0], [0, 1, 1]], 3, 2),
        Piece("Z", 4, [[0, 1], [1, 1], [1, 0]], 2, 3),
    ],
    [
        Piece("J", 5, [[1, 0, 0], [1, 1, 1]], 3, 2),
        Piece("J", 5, [[1, 1], [1, 0], [1, 0]], 2, 3),
        Piece("J", 5, [[1, 1, 1], [0, 0, 1]], 3, 2),
        Piece("J", 5, [[0, 1], [0, 1], [1, 1]], 2, 3),
    ],
    [
        Piece("L", 6, [[0, 0, 1], [1, 1, 1]], 3, 2),
        Piece("L", 6, [[1, 0], [1, 0], [1, 1]], 2, 3),
        Piece("L", 6, [[1, 1, 1], [1, 0, 0]], 3, 2),
        Piece("L", 6, [[1, 1], [0, 1], [0, 1]], 2, 3),
    ],
    [
        Piece("T", 7, [[0, 1, 0], [1, 1, 1]], 3, 2),
        Piece("T", 7, [[1, 0], [1, 1], [1, 0]], 2, 3),
        Piece("T", 7, [[1, 1, 1], [0, 1, 0]], 3, 2),
        Piece("T", 7, [[0, 1], [1, 1], [0, 1]], 2, 3),
    ],
]


@dataclasses.dataclass
class Action:
    x0: int
    piece: Piece


import sys, collections


class Board:
    row_num = ROW_NUM
    col_num = COL_NUM
    didj = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    def __init__(self):
        self.table = [[0 for c in range(self.col_num)] for r in range(self.row_num)]

    def __str__(self) -> str:
        """ 
        [
            [0, 1, 1], 
            [1, 0, 1],
        ]

        =>

        .##\n
        #.#
        """
        return "\n".join("".join(["#" if x else "." for x in r]) for r in self.table)

    def clear(self):
        for i in range(self.row_num):
            for j in range(self.col_num):
                self.table[i][j] = 0

    def proceed(self, action: Action) -> bool:
        assert 0 <= action.x0 and action.x0 < self.col_num
        min_distance = self.row_num - 1  # ピースの各ブロックが落下できる最小距離
        for i, row in enumerate(action.piece.blocks):
            for j in range(len(row)):
                if row[j]:
                    x = action.x0 + j
                    if x >= self.col_num:
                        return False
                    if self.table[i][x]:
                        return False
                    for y in range(i, self.row_num):
                        if self.table[y][x]:
                            min_distance = min(min_distance, y - i - 1)
                            break
                    else:  # 底まで落ちたとき
                        min_distance = min(min_distance, self.row_num - i - 1)
        assert min_distance >= 0
        for i, row in enumerate(action.piece.blocks):
            for j in range(len(row)):
                if row[j]:
                    self.table[i + min_distance][action.x0 + j] = action.piece.form_id
        return True

    def resolve(self) -> int:
        removed_num = 0
        for i, row in enumerate(self.table):
            if row.count(0) == 0:
                removed_num += 1
                for ii in reversed(range(i)):
                    for j in range(len(row)):
                        self.table[ii + 1][j] = self.table[ii][j]
                for j in range(len(row)):
                    self.table[0][j] = 0  # 最上段には空行
        return removed_num

    def has_dead(self) -> bool:
        return self.count_dead() > 0

    def count_dead(self) -> int:
        dist = [[sys.maxsize for c in range(self.col_num)] for r in range(self.row_num)]
        # queue.Queue() は遅い http://n-knuu.hatenablog.jp/entry/2015/05/30/183718
        que: collections.deque = collections.deque()
        for j in range(self.col_num):
            if self.table[0][j] == 0:
                dist[0][j] = 0
                que.append((0, j))
        while len(que) > 0:
            i, j = que.popleft()
            for di, dj in self.didj:
                ni, nj = i + di, j + dj
                if 0 <= ni and ni < self.row_num and 0 <= nj and nj < self.col_num:
                    if (dist[ni][nj] == sys.maxsize) and (self.table[ni][nj] == 0):
                        dist[ni][nj] = dist[i][j] + 1
                        que.append((ni, nj))
        dead_num = 0
        for i in range(self.row_num):
            for j in range(self.col_num):
                if self.table[i][j] == 0:
                    if dist[i][j] > i:  # 細長いとこもダメ
                        dead_num += 1

        return dead_num

    def max_height(self) -> int:
        for i, row in enumerate(self.table):
            if sum(row) > 0:
                return self.row_num - i
        return 0

    def min_height(self) -> int:
        for i in reversed(range(self.row_num)):
            if self.table[i].count(0):
                return self.row_num - i - 1
        return self.row_num

    def adj_diff_sum(self) -> int:
        """ retrun sum(abs(dep[i+1]-dep[i])) for i in [0, col_num) """
        ret = 0
        pre_d = 0
        for j in range(self.col_num):
            for i in range(self.row_num):
                if self.table[i][j]:
                    if j > 0:
                        ret += abs(pre_d - (i))
                    pre_d = i
                    break
            else:
                ret += abs(pre_d - self.row_num)
                pre_d = self.row_num
        return ret
