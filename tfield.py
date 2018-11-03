import tkinter as tk
from tboard import Board
from typing import List
from game import CANVAS_WIDTH, CANVAS_HEIGHT, COLORS

ObjectID = int  # たぶん


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
                fill_color = COLORS[board.table[r][c]]
                self.itemconfigure(self.rects[r][c], fill=fill_color)
