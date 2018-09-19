# coding=utf-8
import copy
import json
import random
from abc import ABCMeta
from time import time


# import numpy

class Solution(object):
    g = None
    h = None
    time = None

    # strategy = None

    def __init__(self, tree_height_val, heuristic_val, time):
        self.g = tree_height_val
        self.h = heuristic_val
        self.time = time

    def print_solution(self):
        # print("SOLUTION FOUND!!!!")
        print("SOLUTION----------------------")
        print("g(n): ", self.g)
        print("h(n): ", self.h)
        print("f(n): ", self.g + self.h)
        print("TIME: ", self.time)
        # print("STRATEGY: ", self.strategy.__str__())


class Puzzle():
    # Matriz do puzzle
    matrix = None

    # Classe da estratégia de busca
    strategy_class = None
    strategy = None

    goal_solution = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    found_solutions = None

    iterations = 0

    satisficing = True
    max_iterations = None

    start_time = None
    max_solutions = None

    def __init__(self, matrix, strategy=None, strategy_class=None, satisficing=True, max_iterations=None,
                 max_solutions=None):
        self.matrix = matrix

        if not strategy:
            self.strategy_class = strategy_class
            self.strategy = self.strategy_class()
        else:
            self.strategy = strategy
        self.satisficing = satisficing
        self.found_solutions = []
        self.max_iterations = max_iterations
        self.max_solutions = max_solutions
        # self.blank_pos = self.find_blank_position(self.matrix)

    def get_possible_paths(self, blank_pos):
        res = ['U', 'D', 'L', 'R']
        if (blank_pos[0] == 0):
            res.remove('U')
        elif (blank_pos[0] == 2):
            res.remove('D')

        if (blank_pos[1] == 0):
            res.remove('L')
        elif (blank_pos[1] == 2):
            res.remove('R')

        return res

    def print_matrix(self, matrix):
        if matrix is None:
            print('None')
            return
        for i in range(0, len(matrix)):
            print(matrix[i])
        print()

    def find_blank_position(self, matrix):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                if matrix[i][j] == 0:
                    return [i, j]

    def up(self, matrix=None):
        if matrix is None:
            matrix = self.matrix
        blank_pos = self.find_blank_position(matrix)
        matrix[blank_pos[0]][blank_pos[1]] = matrix[blank_pos[0] - 1][blank_pos[1]]
        matrix[blank_pos[0] - 1][blank_pos[1]] = 0
        # blank_pos[0] = blank_pos[0] - 1
        # print('--UP!')

        return matrix

    def down(self, matrix=None):
        if matrix is None:
            matrix = self.matrix
        blank_pos = self.find_blank_position(matrix)
        matrix[blank_pos[0]][blank_pos[1]] = matrix[blank_pos[0] + 1][blank_pos[1]]
        matrix[blank_pos[0] + 1][blank_pos[1]] = 0
        # blank_pos[0] = blank_pos[0] + 1
        # print('--DOWN!')

        return matrix

    def left(self, matrix=None):
        if matrix is None:
            matrix = self.matrix
        blank_pos = self.find_blank_position(matrix)
        matrix[blank_pos[0]][blank_pos[1]] = matrix[blank_pos[0]][blank_pos[1] - 1]
        matrix[blank_pos[0]][blank_pos[1] - 1] = 0
        # blank_pos[1] = blank_pos[1] - 1
        # print('--LEFT!')

        return matrix

    def right(self, matrix=None):
        if matrix is None:
            matrix = self.matrix
        blank_pos = self.find_blank_position(matrix)
        matrix[blank_pos[0]][blank_pos[1]] = matrix[blank_pos[0]][blank_pos[1] + 1]
        matrix[blank_pos[0]][blank_pos[1] + 1] = 0
        # blank_pos[1] = blank_pos[1] + 1
        # print('--RIGHT!')

        return matrix

    def move(self, m, matrix=None):
        if matrix is None:
            matrix = self.matrix

        if m == 'U':
            matrix = self.up(matrix)
        elif m == 'D':
            matrix = self.down(matrix)
        elif m == 'L':
            matrix = self.left(matrix)
        elif m == 'R':
            matrix = self.right(matrix)

        return copy.deepcopy(matrix)

    def print_found_solutions(self):
        print('FOUND %s solution(s)' % str(len(self.found_solutions)))
        for s in self.found_solutions:
            if isinstance(s, Solution):
                s.print_solution()

        # GET BEST SOLUTION
        max_f = -1
        i = 0
        max_i = 0
        for s in self.found_solutions:
            f = s.g + (s.h if s.h is not None else 0)
            if f >= max_f:
                max_f = s.g + f
                max_i = i
            i = i + 1

        print('BEST FOUND SOLUTION:', str(max_i + 1) + 'a')
        self.found_solutions[max_i].print_solution()

    def solve(self):
        s = self.matrix

        self.start_time = time()

        self.strategy.visited = set()
        self.strategy.solutions = [s]
        # test if is goal solution
        while not self.test():
            self.generate(self.strategy.actual)

        return s

    def test(self):
        self.iterations = self.iterations + 1
        if len(self.strategy.solutions) == 0:
            print(self.strategy.visited)
            print('STOPPED ON STACK EMPTY...')
            self.print_found_solutions()
            return True

        if self.max_iterations is not None and self.iterations >= self.max_iterations:
            print('STOPPED ON MAX ITERATION...')
            self.print_found_solutions()
            return True

        if self.max_solutions is not None and self.max_solutions <= len(self.found_solutions):
            print('STOPPED ON MAX SOLUTIONS...')
            self.print_found_solutions()
            return True

        # self.actual = self.stack.pop()
        self.strategy.actual, heuristic_val = self.strategy.get_actual_solution(self.goal_solution)

        self.strategy.visited.add(json.dumps(self.strategy.actual))
        print("TEST:")
        self.print_matrix(self.strategy.actual)

        # print('BLANK_POS: ', self.find_blank_position(self.actual))

        if self.strategy.actual == self.goal_solution:
            print("SOLUTION FOUND!!!!")
            s = Solution(self.iterations, heuristic_val, time() - self.start_time)
            self.found_solutions.append(s)

            # print("ITERATIONS: ", self.iterations)
            # print("TIME: ", time() - self.start_time)
            # print("STRATEGY: ", self.strategy.__str__())
            if self.satisficing:
                print('STOPPED ON SATISFICING...')
                self.print_found_solutions()
                return True

        return False

    def generate(self, solution):

        # s = strategy(solution)
        blank_pos = self.find_blank_position(solution)
        possible_paths = self.get_possible_paths(blank_pos)
        print()
        print("GERENATE", possible_paths)

        for p in possible_paths:
            matrix = copy.deepcopy(solution)
            matrix_solution = self.move(p, matrix)
            serialized = json.dumps(matrix_solution)
            if serialized in self.strategy.visited:
                continue

            self.print_matrix(matrix_solution)
            self.strategy.solutions.append(matrix_solution)

        pass

    def randomize(self, n):
        """
        Faz n movimentos sortidos
        :param n: número de movimentos
        :return:
        """
        for i in range(0, n):
            blank_pos = self.find_blank_position(self.matrix)
            possible_paths = self.get_possible_paths(blank_pos)

            rand_move = random.randint(0, len(possible_paths) - 1)

            self.matrix = self.move(possible_paths[rand_move], self.matrix)


class SearchStrategy:
    """
    Classe abstrata de uma estratégia
    """

    __metaclass__ = ABCMeta
    visited = None
    solutions = None
    actual = None


# Implementações das estratégias

class DepthSearch(SearchStrategy):
    """
    Busca em profundidade
    """

    def get_actual_solution(self, goal):
        # PEGA ULTIMA
        return (self.solutions.pop(), 0)

    def __str__(self):
        return "DepthSearch"


class BreathFirstSearch(SearchStrategy):
    """
    Busca em largura
    """

    def get_actual_solution(self, goal):
        # PEGA PRIMEIRA
        return (self.solutions.pop(0), 0)

    def __str__(self):
        return "BreathFirstSearch"


class AStarSearch(object):
    """
    A*
    """

    def __init__(self, heuristica):
        self.heuristica = heuristica

    def get_actual_solution(self, goal):

        # verifica qual esta mais proxima da solucao
        k = 0
        maior_count = -1
        k_atual = -1
        for s in self.solutions:
            count = 0

            for i in range(0, len(s)):
                for j in range(0, len(s[i])):
                    if self.heuristica == 'numeros_dentro_de_posicao':
                        if s[i][j] == goal[i][j]:
                            count = count + 1
                    elif self.heuristica == 'numeros_fora_de_posicao':
                        if s[i][j] != goal[i][j]:
                            count = count + 1
            if count > maior_count:
                maior_count = count
                k_atual = k

            k = k + 1

        return (self.solutions.pop(k_atual), count)

    def __str__(self):
        return "AStarSearch"


if __name__ == '__main__':
    # strategy = AStarSearch(heuristica='numeros_fora_de_posicao')
    strategy = AStarSearch(heuristica='numeros_dentro_de_posicao')
    # strategy = DepthSearch()
    # strategy = BreathFirstSearch()

    puzzle = Puzzle([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ], strategy=strategy, satisficing=False, max_iterations=5000, max_solutions=1)

    puzzle.randomize(9000)
    puzzle.print_matrix(puzzle.matrix)

    puzzle.solve()
