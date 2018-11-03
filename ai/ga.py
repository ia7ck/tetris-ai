import dataclasses, random
from typing import List
from ai.cost_func_ai import CostFuncAi


@dataclasses.dataclass
class Genetic:
    coefficients: List[int]
    score: int


def calc_fitness(ai: CostFuncAi) -> int:
    return 0


def genetic_algorithm(population_size: int = 100, gen_limit: int = 10) -> List[int]:
    ai = CostFuncAi()
    population: List[Genetic] = []
    # init
    for i in range(population_size):
        coeffs = [random.randint(-100, 100) for _ in range(3)]
        ai.coefficients = coeffs
        population.append(Genetic(coeffs, calc_fitness(ai)))
    # selection, genetic operation
    for _ in range(gen_limit):
        pass
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
