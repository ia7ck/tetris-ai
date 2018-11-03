import unittest, copy
from game import Piece, Action, Board, pieces


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.pieces = pieces  # あ
        self.piece_dict = {}
        for form in ["I", "O", "S", "Z", "J", "L", "T"]:
            self.piece_dict[form] = [
                piece
                for piece_set in self.pieces
                for piece in piece_set
                if piece.form == form
            ]
        self.row_num = self.board.row_num
        self.col_num = self.board.col_num

    def test_resolve(self):
        self.assertEqual(self.board.resolve(), 0)

    def test_proceed(self):
        for piece_set in self.pieces:
            for piece in piece_set:
                for x in range(self.board.col_num - piece.width + 1):
                    board = copy.deepcopy(self.board)
                    self.assertTrue(board.proceed(Action(x, piece)))

    def test_z(self):
        """ 
            ##
             ##

        #####..###
        """
        for j in range(5):
            self.board.table[self.row_num - 1][j] = 1
        for j in range(7, self.col_num):
            self.board.table[self.row_num - 1][j] = 1
        piece = self.piece_dict["Z"][0]
        self.board.proceed(Action(4, piece))
        self.assertEqual(self.board.resolve(), 1, str(self.board))

    def test_vertical_z(self):
        """ 
             #
            ##
            #

        ####..####
        ####.#####
        """
        for i in [0, 1]:
            for j in range(4):
                self.board.table[self.row_num - i - 1][j] = 1
        for j in range(5, self.col_num):
            self.board.table[self.row_num - 1][j] = 1
        for j in range(6, self.col_num):
            self.board.table[self.row_num - 2][j] = 1
        piece = self.piece_dict["Z"][1]
        self.board.proceed(Action(4, piece))
        self.assertEqual(self.board.resolve(), 2, str(self.board))

    def test_i(self):
        """ 
                 #
                 #
                 #
                 #

        #########.
        #########.
        #########.
        #########.
        """
        for i in range(4):
            for j in range(self.col_num - 1):
                self.board.table[self.row_num - i - 1][j] = 1
        piece = self.piece_dict["I"][1]
        self.board.proceed(Action(self.col_num - 1, piece))
        self.assertEqual(self.board.resolve(), 4, str(self.board))

    def test_count_dead(self):
        """
        .###......
        .#.#.###..
        .#.#.#.#..
        """
        for i, js in enumerate([[1, 3, 5, 7], [1, 3, 5, 6, 7], [1, 2, 3]]):
            for j in js:
                self.board.table[self.row_num - i - 1][j] = 1
        self.assertEqual(self.board.count_dead(), 3, str(self.board))

    def test_max_height(self):
        """ 
        #.........
        ##........
        ###.......
        """
        for i in range(3):
            for j in range(3):
                if i + j <= 2:
                    self.board.table[self.row_num - i - 1][j] = 1
        self.assertEqual(self.board.max_height(), 3, str(self.board))

    def test_adj_diff_sum(self):
        """ 
        #.....#...
        #..#..#...
        #..##.#...
        """
        for i, js in enumerate([[0, 3, 4, 6], [0, 3, 6], [0, 6]]):
            for j in js:
                self.board.table[self.row_num - i - 1][j] = 1
        self.assertEqual(self.board.adj_diff_sum(), 13, str(self.board))  # 3+2+1+1+3+3


if __name__ == "__main__":
    unittest.main()
