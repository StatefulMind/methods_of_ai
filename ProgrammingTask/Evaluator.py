from itertools import product
from Grid import Grid
import argparse
import numpy as np

NOMOVE = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

DIRECTIONS = [NOMOVE, UP, RIGHT, DOWN, LEFT]

NOMOVE_D = (0, 0)
UP_D = (-1, 0)
RIGHT_D = (0, 1)
DOWN_D = (1, 0)
LEFT_D = (0, -1)

DIRECTIONS_D = {NOMOVE: NOMOVE_D, UP: UP_D, RIGHT: RIGHT_D, DOWN: DOWN_D, LEFT: LEFT_D}

class Evaluator:
    '''
    Evaluates generated policy and improves on it
    '''

    def __init__(self, grid, discount):
        self._grid = grid
        self._discount = discount

    def iterate(self, iterations, step_cost):
        succ_array = [[0 for x in range(self._grid.shape[1])] for y in range(self._grid.shape[0])]
        for i in range(iterations):
            for x, y in product(range(0, self._grid.shape[1]), range(0, self._grid.shape[0])):
                policy = self._grid.get_policy_field(x, y)
                field = self._grid.get_grid_field(x, y)

                if field.has_static_evaluation_value:
                    succ_array[y][x] = field.get_static_evaluation_value()
                    continue

                movement_probs = field.get_movement_probs()[policy]
                successor_sum = 0
                for dir, movement_prob in movement_probs.items():
                    x_mv, y_mv = np.add([x, y], DIRECTIONS_D[dir])
                    if isOutOfBoundaries(x_mv, y_mv, self._grid.shape):
                        #Stay at the same field
                        x_mv, y_mv = [x, y]
                    elif not field.can_move_here:
                        x_mv, y_mv = [x, y]
                    else:
                        pass
                    successor_sum += movement_prob * succ_array[y][x]
                #Immediate reward still missing
                succ_array[y][x] = -step_cost + (self._discount**i) * successor_sum

        self._grid.set_eval_grid(succ_array)
        print(succ_array)

    def evaluate(self):
        eval_directions = {}
        for direction in DIRECTIONS:
            eval_directions[direction] = [[0 for x in range(self._grid.shape[1])] for y in range(self._grid.shape[0])]
            for x, y in product(range(0, self._grid.shape[1]), range(0, self._grid.shape[0])):

                field = self._grid.get_grid_field(x, y)
                movement_probs = field.get_movement_probs()[direction]
                successor_sum = 0
                for dir_real, movement_prob in movement_probs.items():
                    x_mv, y_mv = np.add([x, y], DIRECTIONS_D[dir_real])
                    if isOutOfBoundaries(x_mv, y_mv, self._grid.shape):
                        # Stay at the same field
                        x_mv, y_mv = [x, y]
                    elif not field.can_move_here:
                        x_mv, y_mv = [x, y]
                    else:
                        pass
                    successor_sum += movement_prob * self._grid.get_eval_field(x_mv, y_mv)

                eval_directions[direction][y][x] = successor_sum

        new_policy = [[0 for x in range(self._grid.shape[1])] for y in range(self._grid.shape[0])]
        for x, y in product(range(0, self._grid.shape[1]), range(0, self._grid.shape[0])):
            new_policy[y][x] = np.argmax({direction: eval_directions[direction][y][x] for direction in DIRECTIONS})
        print(new_policy)
        self._grid.set_policy_grid(new_policy)
        self._grid.print()
        print(eval_directions)








def isOutOfBoundaries(x, y, shape):
    '''
    returns if iteration goes out of bounds - since outer walls are not defined and
    restricted by array lenght limits
    :param y:
    :param shape:
    :return:
    '''
    return x < 0 or y < 0 or x >= shape[1] or y >= shape[0]


# instantiate parser
parser = argparse.ArgumentParser(description='''Read grid-file from stdin,
parse and print grid file accordingly.''')
parser.add_argument('grid_file', help='path to input .grid file')
# parser.add_argument('-i', '--iter', type='int',
#                   help='how many iterations are performed by the policy iteration', )
args = parser.parse_args()

if __name__ == '__main__':
    grid = Grid(grid_file=args.grid_file)
    evaluator = Evaluator(grid, 1)
    evaluator.iterate(100, 0.04)
    evaluator.evaluate()

    for i in range(100):
        evaluator.evaluate()