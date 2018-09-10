import copy
import json
import random
from time import time
import numpy


# ESTRATÉGIAS DE BUSCA CEGA
class DepthSearch(object):
    def get_actual_solution(self, solutions, goal):
        # PEGA ULTIMA
        return solutions.pop()

    def __str__(self):
        return "DepthSearch"


class BreathFirstSearch(object):
    def get_actual_solution(self, solutions, goal):
        # PEGA PRIMEIRA
        return solutions.pop(0)

    def __str__(self):
        return "BreathFirstSearch"


# OUTRAS ESTRATEGIAS
class MelhorzinhaSearch(object):
    def get_actual_solution(self, solutions, goal):

        # verifica qual esta mais proxima da solucao
        i = 0
        atual = 999999999
        i_atual = -1
        for s in solutions:
            # results2 = 1 - scipy.spatial.distance.cdist(s, goal, 'cosine')
            # numpy.matrix.mean()
            m1 = numpy.matrix(s)
            m1 = numpy.matrix.mean(m1)
            m2 = numpy.matrix(goal)
            m2 = numpy.matrix.mean(m2)

            if m2 - m1 < atual:
                atual = m2 - m1
                i_atual = i
            i = i + 1

        return solutions.pop(i_atual)

    def __str__(self):
        return "MelhorzinhaSearch"


class Puzzle():
    matrix = None

    strategy = None

    goal_solution = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    visited = None
    solutions = None
    actual = None

    iterations = 0

    start_time = None

    def __init__(self, matrix, strategy=DepthSearch):
        self.matrix = matrix
        self.strategy = strategy
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

    def solve(self):
        s = self.matrix

        strategy = self.strategy()
        # strategy = BreathFirstSearch()
        # strategy = MelhorzinhaSearch()

        self.start_time = time()

        self.visited = set()
        self.solutions = [s]
        # test if is goal solution
        while not self.test(strategy):
            self.generate(strategy, self.actual)

        return s

    def test(self, strategy):
        self.iterations = self.iterations + 1
        if len(self.solutions) == 0:
            print(self.visited)
            print('STACK EMPTY... NO SOLUTION FOUND')
            return True

        # self.actual = self.stack.pop()
        self.actual = strategy.get_actual_solution(self.solutions, self.goal_solution)

        self.visited.add(json.dumps(self.actual))
        print("TEST:")
        self.print_matrix(self.actual)

        print('BLANK_POS: ', self.find_blank_position(self.actual))

        if self.actual == self.goal_solution:
            print("SOLUTION FOUND!!!!")
            print("ITERATIONS: ", self.iterations)
            print("TIME: ", time() - self.start_time)
            print("STRATEGY: ", strategy)
            return True
        return False

    def generate(self, strategy, solution):

        # s = strategy(solution)
        blank_pos = self.find_blank_position(solution)
        possible_paths = self.get_possible_paths(blank_pos)
        print()
        print("GERENATE", possible_paths)

        for p in possible_paths:
            matrix = copy.deepcopy(solution)
            matrix_solution = self.move(p, matrix)
            serialized = json.dumps(matrix_solution)
            if serialized in self.visited:
                print('already visited')
                continue

            self.print_matrix(matrix_solution)
            self.solutions.append(matrix_solution)

        pass

    def sort(self, n):
        for i in range(0, n):
            blank_pos = self.find_blank_position(self.matrix)
            possible_paths = self.get_possible_paths(blank_pos)

            rand_move = random.randint(0, len(possible_paths) - 1)

            self.matrix = self.move(possible_paths[rand_move], self.matrix)


if __name__ == '__main__':
    puzzle = Puzzle([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ], strategy=DepthSearch)

    puzzle.sort(100)
    puzzle.print_matrix(puzzle.matrix)

    puzzle.solve()
