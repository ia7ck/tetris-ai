import tkinter as tk

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 960


class Field(tk.Canvas):
    def __init__(self, master, board):
        super().__init__(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.rects = self.create_rects(board)

    def create_rects(self, board):
        row_num = len(board)
        cell_height = WINDOW_HEIGHT // row_num
        rects = [[] for r in range(row_num)]
        for r in range(row_num):
            col_num = len(board[r])
            cell_width = WINDOW_WIDTH // col_num
            for c in range(col_num):
                rect = self.create_rectangle(
                    cell_width * c,
                    cell_height * r,
                    cell_width * (c + 1),
                    cell_height * (r + 1),
                    fill="white",
                )
                rects[r].append(rect)
        self.place(x=0, y=0)
        return rects

    def draw(self, board):
        for r in range(len(board)):
            for c in range(len(board[r])):
                fill_color = "black" if board[r][c] else "white"
                self.itemconfigure(self.rects[r][c], fill=fill_color)


class Tetris(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tetris")
        self.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.row_num = 20
        self.col_num = 10
        self.board = [[0 for c in range(self.col_num)] for r in range(self.row_num)]

        self.field = Field(self, self.board)


def main():
    tetris = Tetris()
    tetris.mainloop()


if __name__ == "__main__":
    main()
