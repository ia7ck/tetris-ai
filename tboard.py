import tkinter as tk
import dataclasses
import collections
import sys
from typing import List
from game import Action, CANVAS_WIDTH, CANVAS_HEIGHT, ROW_NUM, COL_NUM

didj = [(0, 1), (-1, 0), (0, -1), (1, 0)]


class Board:
    row_num = ROW_NUM
    col_num = COL_NUM

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
                    self.table[i + min_distance][action.x0 + j] = 1
        return True

    def resolve(self) -> int:
        removed_num = 0
        for i, row in enumerate(self.table):
            if sum(row) == self.col_num:
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
            for di, dj in didj:
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
