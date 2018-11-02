import dataclasses
from typing import List


@dataclasses.dataclass
class Piece:
    form: str
    blocks: List[List[int]]
    width: int
    height: int

    def __str__(self) -> str:
        return "\n".join("".join(["#" if x else "." for x in r]) for r in self.blocks)


def make_pieces() -> List[List[Piece]]:
    pieces: List[List[Piece]] = []

    pieces.append(
        [Piece("I", [[1, 1, 1, 1]], 4, 1), Piece("I", [[1], [1], [1], [1]], 1, 4)]
    )

    pieces.append([Piece("O", [[1, 1], [1, 1]], 2, 2)])

    pieces.append(
        [
            Piece("S", [[0, 1, 1], [1, 1, 0]], 3, 2),
            Piece("S", [[1, 0], [1, 1], [0, 1]], 2, 3),
        ]
    )

    pieces.append(
        [
            Piece("Z", [[1, 1, 0], [0, 1, 1]], 3, 2),
            Piece("Z", [[0, 1], [1, 1], [1, 0]], 2, 3),
        ]
    )

    # pieces.append(
    #     [
    #         Piece("J", [[1, 0, 0], [1, 1, 1]], 3, 2),
    #         Piece("J", [[1, 1], [1, 0], [1, 0]], 2, 3),
    #         Piece("J", [[1, 1, 1], [0, 0, 1]], 3, 2),
    #         Piece("J", [[0, 1], [0, 1], [1, 1]], 2, 3),
    #     ]
    # )
    # pieces.append(
    #     [
    #         Piece("L", [[0, 0, 1], [1, 1, 1]], 3, 2),
    #         Piece("L", [[1, 0], [1, 0], [1, 1]], 2, 3),
    #         Piece("L", [[1, 1, 1], [1, 0, 0]], 3, 2),
    #         Piece("L", [[1, 1], [0, 1], [0, 1]], 2, 3),
    #     ]
    # )

    # pieces.append(
    #     [
    #         Piece("T", [[0, 1, 0], [1, 1, 1]], 3, 2),
    #         Piece("T", [[1, 0], [1, 1], [1, 0]], 2, 3),
    #         Piece("T", [[1, 1, 1], [0, 1, 0]], 3, 2),
    #         Piece("T", [[0, 1], [1, 1], [0, 1]], 2, 3),
    #     ]
    # )

    return pieces


@dataclasses.dataclass
class Action:
    x0: int
    piece: Piece
