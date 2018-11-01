import dataclasses
from typing import List


@dataclasses.dataclass
class Piece:
    form: str
    blocks: List[List[int]]

    def __str__(self) -> str:
        return (
            "form: {}".format(self.form)
            + "\n"
            + "\n".join("".join(["#" if x else "." for x in r]) for r in self.blocks)
        )


def make_pieces() -> List[Piece]:
    pieces: List[Piece] = []

    pieces.append(Piece("I", [[1, 1, 1, 1]]))
    pieces.append(Piece("I", [[1], [1], [1], [1]]))

    pieces.append(Piece("O", [[1, 1], [1, 1]]))

    pieces.append(Piece("S", [[0, 1, 1], [1, 1, 0]]))
    pieces.append(Piece("S", [[1, 0], [1, 1], [0, 1]]))

    pieces.append(Piece("Z", [[1, 1, 0], [0, 1, 1]]))
    pieces.append(Piece("Z", [[0, 1], [1, 1], [1, 0]]))

    pieces.append(Piece("J", [[1, 0, 0], [1, 1, 1]]))
    pieces.append(Piece("J", [[1, 1], [1, 0], [1, 0]]))
    pieces.append(Piece("J", [[1, 1, 1], [0, 0, 1]]))
    pieces.append(Piece("J", [[0, 1], [0, 1], [1, 1]]))

    pieces.append(Piece("L", [[0, 0, 1], [1, 1, 1]]))
    pieces.append(Piece("L", [[1, 0], [1, 0], [1, 1]]))
    pieces.append(Piece("L", [[1, 1, 1], [1, 0, 0]]))
    pieces.append(Piece("L", [[1, 1], [0, 1], [0, 1]]))

    pieces.append(Piece("T", [[0, 1, 0], [1, 1, 1]]))
    pieces.append(Piece("T", [[1, 0], [1, 1], [1, 0]]))
    pieces.append(Piece("T", [[1, 1, 1], [0, 1, 0]]))
    pieces.append(Piece("T", [[0, 1], [1, 1], [0, 1]]))

    return pieces
