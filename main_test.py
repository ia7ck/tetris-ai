import unittest
from typing import List
from main import Tetris
from tetromino import Piece


class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def test_I_O(self):  # Input/Outputではない
        pieces: List[Piece] = [
            Piece("I", [[1], [1], [1], [1]], 1, 4),
            Piece("I", [[1, 1, 1, 1]], 4, 1),
            Piece("O", [[1, 1], [1, 1]], 2, 2),
        ]
        for piece in pieces:
            tetris = Tetris()
            for col in range(piece.width - 1):
                # はみ出すのはダメ
                self.assertFalse(tetris.put_piece(tetris.col_num - col - 1, piece))
            limit = tetris.row_num // piece.height
            for col in range(0, tetris.col_num, piece.width):
                if col + piece.width <= tetris.col_num:
                    for _ in range(limit):
                        self.assertTrue(tetris.put_piece(col, piece))
            for col in range(tetris.col_num):
                self.assertFalse(tetris.put_piece(col, piece))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
