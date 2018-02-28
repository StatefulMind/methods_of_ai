from itertools import product
import numpy as np
from Constants import DIRECTIONS, DIRECTIONS_D, NOMOVE


class Learner:
    '''
    Learner generated policy and improves on it
    '''

    def __init__(self, grid, position='static', learning_rate=0.04, reward_decay=0.04,
                 epsilon_soft=0.4):
        self._grid = grid
        self._pos = self.start_position(position)
        self._learning_rate = learning_rate
        self._reward_decay = reward_decay
        self._epsilon_soft = epsilon_soft

    def start_position(self, position):
        if position == 'static':
            print('Start Position is (0,0)')
            # starting point is left corner - x coordinate corresponds to 0 and max y
            return 0, self._grid.shape_y - 1
        if position == 'random':
            # pull random position
            random_pos = self.random_start()
            # as long as it is not a field repeat
            while not self._grid.get_grid_field(random_pos[0], random_pos[1]).type == 'F':
                random_pos = self.random_start()
            #print('Start Position is {} - randomly generated'.format(random_pos))
            # maybe dont print start position - they are inverse to display but are valid
            return random_pos

    def random_start(self):
        return np.random.randint(self._grid.shape_x), np.random.randint(self._grid.shape_y)

    def evaluate_policy(self):
        field_field = self._grid.get_grid_field(self._pos[0], self._pos[1])
        policy_of_field = self._grid.get_policy_field(self._pos[0], self._pos[1])
        print(field_field)
        print(policy_of_field)
        new_array = [[0 for _ in range(self._grid.shape_x)] for _ in range(self._grid.shape_y)]
        print(field_field.get_movement_probs()[policy_of_field])

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
