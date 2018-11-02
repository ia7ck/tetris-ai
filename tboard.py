import tkinter as tk
import dataclasses
from typing import List

CANVAS_WIDTH = 480
CANVAS_HEIGHT = 960

ObjectID = int  # たぶん


class Board:
    row_num: int = 20
    col_num: int = 10

    def __init__(self):
        self.table = [[0 for c in range(self.col_num)] for r in range(self.row_num)]


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
