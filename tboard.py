import tkinter as tk
import dataclasses
from typing import List
from game import Action

CANVAS_WIDTH = 480
CANVAS_HEIGHT = 960

ObjectID = int  # たぶん


class Board:
    row_num: int = 20
    col_num: int = 10

    def __init__(self):
        self.table = [[0 for c in range(self.col_num)] for r in range(self.row_num)]

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


class Field(tk.Canvas):
    def __init__(self, master, board: Board):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.rects = self.create_rects(board)

    def create_rects(self, board: Board) -> List[List[ObjectID]]:
        cell_height = CANVAS_HEIGHT // board.row_num
        rects: List[List[ObjectID]] = [[] for r in range(board.row_num)]
        for r in range(board.row_num):
            cell_width = CANVAS_WIDTH // board.col_num
            for c in range(board.col_num):
                rect: ObjectID = self.create_rectangle(
                    cell_width * c,
                    cell_height * r,
                    cell_width * (c + 1),
                    cell_height * (r + 1),
                    fill="white",
                )
                rects[r].append(rect)
        self.place(x=0, y=0)
        return rects

    def draw(self, board: Board):
        for r in range(board.row_num):
            for c in range(board.col_num):
                fill_color = "black" if board.table[r][c] else "white"
                self.itemconfigure(self.rects[r][c], fill=fill_color)
