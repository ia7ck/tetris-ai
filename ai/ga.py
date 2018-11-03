import random, operator, copy
from typing import List
from ai.cost_func_ai import CostFuncAi
from game import Board, pieces, SCORES


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

    @staticmethod
    def crossover(par1: Individual, par2: Individual) -> Individual:
        return par2

    @classmethod
    def solve(cls, population_size: int = 12, gen_limit: int = 10) -> List[int]:
        population: List[Individual] = []
        # init
        for i in range(population_size):
            print("{} th trial".format(i))
            coeffs = [random.randint(-10000, 10000) for _ in range(3)]
            population.append(Individual(coeffs, cls.calc_fitness(coeffs)))
        # selection, genetic operation
        for i in range(gen_limit):
            print("{} th trial".format(i))
            population.sort(key=operator.attrgetter("fitness"), reverse=True)
            elites = cls.selection(population)
            for j in range(len(elites), population_size):  # eliteと適当に選んだ個体を交叉させる
                population[j] = cls.crossover(
                    random.choice(elites), random.choice(population)
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
