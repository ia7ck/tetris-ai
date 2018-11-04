import random, operator
from typing import List
from ai.cost_func_ai import CostFuncAi
from game import Board, pieces, SCORES

COEFFS_LENGTH = 3


class Individual:
    def __init__(self, coefficients, score):
        self.genom = coefficients
        self.fitness = score


class Ga:
    ai = CostFuncAi()
    board = Board()

    @staticmethod
    def selection(
        population: List[Individual]
    ) -> List[Individual]:  # 強いのを25%だけ残す TODO:ルーレット方式も試す
        return population[: (len(population) // 4)]

    @classmethod
    def calc_fitness(cls, coeffs: List[int]) -> int:
        cls.ai.coefficients = coeffs
        cls.board.clear()
        score = 0
        while True:
            given_piece_set = random.choice(pieces)
            action = cls.ai.get_action(cls.board, given_piece_set)
            can_put = cls.board.proceed(action)
            if not can_put:
                break
            rm_line_num = cls.board.resolve()
            score += SCORES[rm_line_num]
        return score

    @classmethod
    def crossover(cls, par1: Individual, par2: Individual) -> Individual:
        coeffs: List[int] = []
        for i in range(COEFFS_LENGTH):
            mn, mx = (
                min(par1.genom[i], par2.genom[i]),
                max(par1.genom[i], par2.genom[i]),
            )
            d = (mx - mn) // 10
            coeffs.append(random.randint(mn - d, mx + d))
        return Individual(coeffs, cls.calc_fitness(coeffs))

    @classmethod
    def solve(cls, population_size: int = 12, gen_limit: int = 10) -> List[int]:
        population: List[Individual] = []
        # init
        for i in range(population_size):
            coeffs = [random.randint(-10000, 10000) for _ in range(COEFFS_LENGTH)]
            population.append(Individual(coeffs, cls.calc_fitness(coeffs)))
        print("init finished")
        # selection, genetic operation
        for i in range(gen_limit):
            population.sort(key=operator.attrgetter("fitness"), reverse=True)
            elites = cls.selection(population)
            for j in range(len(elites), population_size):  # eliteとその他の個体を交叉させる
                population[j] = cls.crossover(
                    random.choice(elites), random.choice(population[len(elites) :])
                )
            print(
                "{}/{} selection-genetic finished.".format(i + 1, gen_limit)
                + " "
                + "current best score : {}".format(
                    max(population, key=operator.attrgetter("fitness")).fitness
                )
            )
        # termination
        best_score = -1
        best_coeffs: List[int] = []
        for individual in population:
            if individual.fitness > best_score:
                best_score = individual.fitness
                best_coeffs = individual.genom
        print("best score : {}".format(best_score))
        print("best coeffs : {}".format(best_coeffs))
        return best_coeffs
