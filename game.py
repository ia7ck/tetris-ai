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


@dataclasses.dataclass
class Piece:
    form: str
    form_id: int
    blocks: List[List[int]]
    width: int
    height: int

    def __str__(self) -> str:
        return "\n".join("".join(["#" if x else "." for x in r]) for r in self.blocks)


def make_pieces() -> List[List[Piece]]:
    pieces: List[List[Piece]] = []

    pieces.append(
        [Piece("I", 1, [[1, 1, 1, 1]], 4, 1), Piece("I", 1, [[1], [1], [1], [1]], 1, 4)]
    )

    pieces.append([Piece("O", 2, [[1, 1], [1, 1]], 2, 2)])

    pieces.append(
        [
            Piece("S", 3, [[0, 1, 1], [1, 1, 0]], 3, 2),
            Piece("S", 3, [[1, 0], [1, 1], [0, 1]], 2, 3),
        ]
    )

    pieces.append(
        [
            Piece("Z", 4, [[1, 1, 0], [0, 1, 1]], 3, 2),
            Piece("Z", 4, [[0, 1], [1, 1], [1, 0]], 2, 3),
        ]
    )

    pieces.append(
        [
            Piece("J", 5, [[1, 0, 0], [1, 1, 1]], 3, 2),
            Piece("J", 5, [[1, 1], [1, 0], [1, 0]], 2, 3),
            Piece("J", 5, [[1, 1, 1], [0, 0, 1]], 3, 2),
            Piece("J", 5, [[0, 1], [0, 1], [1, 1]], 2, 3),
        ]
    )
    pieces.append(
        [
            Piece("L", 6, [[0, 0, 1], [1, 1, 1]], 3, 2),
            Piece("L", 6, [[1, 0], [1, 0], [1, 1]], 2, 3),
            Piece("L", 6, [[1, 1, 1], [1, 0, 0]], 3, 2),
            Piece("L", 6, [[1, 1], [0, 1], [0, 1]], 2, 3),
        ]
    )

    pieces.append(
        [
            Piece("T", 7, [[0, 1, 0], [1, 1, 1]], 3, 2),
            Piece("T", 7, [[1, 0], [1, 1], [1, 0]], 2, 3),
            Piece("T", 7, [[1, 1, 1], [0, 1, 0]], 3, 2),
            Piece("T", 7, [[0, 1], [1, 1], [0, 1]], 2, 3),
        ]
    )

    return pieces


@dataclasses.dataclass
class Action:
    x0: int
    piece: Piece
