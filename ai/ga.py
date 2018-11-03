import dataclasses, random, operator
from typing import List
from ai.cost_func_ai import CostFuncAi
from game import Board, pieces, SCORES


@dataclasses.dataclass
class Genetic:
    coefficients: List[int]
    score: int


def calc_fitness(ai: CostFuncAi, board: Board) -> int:
    board.clear()
    score = 0
    while True:
        given_piece_set = random.choice(pieces)
        action = ai.get_action(board, given_piece_set)
        can_put = board.proceed(action)
        if not can_put:
            break
        rm_line_num = board.resolve()
        score += SCORES[rm_line_num]
    return score


def genetic_algorithm(population_size: int = 10, gen_limit: int = 10) -> List[int]:
    ai = CostFuncAi()
    board = Board()
    population: List[Genetic] = []
    # init
    for i in range(population_size):
        coeffs = [random.randint(-100, 100) for _ in range(3)]
        ai.coefficients = coeffs
        population.append(Genetic(coeffs, calc_fitness(ai, board)))
    # selection, genetic operation
    for _ in range(gen_limit):
        population.sort(key=operator.attrgetter("score"), reverse=True)

    # termination
    best_score = -1
    best_coeffs: List[int] = []
    for g in population:
        if g.score > best_score:
            best_score = g.score
            best_coeffs = g.coefficients
    print("best score : {}".format(best_score))
    print("best coeffs : {}".format(best_coeffs))
    return best_coeffs
