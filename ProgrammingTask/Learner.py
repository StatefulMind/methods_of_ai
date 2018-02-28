from itertools import product
import numpy as np
from Constants import DIRECTIONS, DIRECTIONS_D, NOMOVE


class Learner:
    '''
    Learner generated policy and improves on it
    '''

    def __init__(self, grid, learning_rate=0.04, reward_decay=0.04,
                 epsilon_soft=0.4):
        self._grid = grid
        self._learning_rate = learning_rate
        self._reward_decay = reward_decay
        self._epsilon_soft = epsilon_soft

    def evaluate_policy(self):
        pass

    def improve_policy(self):
        pass

    # use np.random.uniform < self._epsilon_soft for selection of move

    def check_convergence(self, old_step, new_step, convergence_value=0.05):
        difference = 0
        for x, y in product(range(0, self._grid.shape_x), range(0, self._grid.shape_y)):
            difference = abs(old_step[y][x] - new_step[y][x])
        return difference < convergence_value


def is_out_of_bounds(x, y, shape):
    return x < 0 or y < 0 or x >= shape[0] or y >= shape[1] 
