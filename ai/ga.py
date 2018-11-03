import dataclasses, random, operator, copy
from typing import List
from ai.cost_func_ai import CostFuncAi
from game import Board, pieces, SCORES


@dataclasses.dataclass
class Individual:
    coefficients: List[int]
    score: int


def selection(
    population: List[Individual]
) -> List[Individual]:  # 強いのを25%だけ残す TODO:ルーレット方式も試す
    return population[: (len(population) // 4)]


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


def crossover(par1: Individual, par2: Individual) -> Individual:
    return par2


def genetic_algorithm(population_size: int = 12, gen_limit: int = 10) -> List[int]:
    ai = CostFuncAi()
    board = Board()
    population: List[Individual] = []
    # init
    for _ in range(population_size):
        coeffs = [random.randint(-10000, 10000) for _ in range(3)]
        ai.coefficients = coeffs
        population.append(Individual(coeffs, calc_fitness(ai, board)))
    # selection, genetic operation
    for i in range(gen_limit):
        print("{} th trial".format(i))
        population.sort(key=operator.attrgetter("score"), reverse=True)
        elites = selection(population)
        for j in range(len(elites), population_size):  # eliteと適当に選んだ個体を交叉させる
            population[j] = crossover(random.choice(elites), random.choice(population))
    # termination
    best_score = -1
    best_coeffs: List[int] = []
    for individual in population:
        if individual.score > best_score:
            best_score = individual.score
            best_coeffs = individual.coefficients
    print("best score : {}".format(best_score))
    print("best coeffs : {}".format(best_coeffs))
    return best_coeffs
