from itertools import product
import numpy as np
import pandas as pd
from Constants import DIRECTIONS, DIRECTIONS_D, NOMOVE


class Learner:
    '''
    Learner generated policy and improves on it
    '''

    def __init__(self, grid, position='static', learning_rate=0.04, reward_decay=0.4,
                 epsilon_soft=0.4):
        self._grid = grid
        self._pos = self.start_position(position)
        self._learning_rate = learning_rate
        self._gamma = reward_decay
        # already calculate the epsilon value
        self._epsilon_soft = 1 - epsilon_soft + epsilon_soft/4
        self._q_table = np.zeros((self._grid.shape_y, self._grid.shape_x))

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
            return random_pos

    def random_start(self):
        return np.random.randint(self._grid.shape_x), np.random.randint(self._grid.shape_y)

    def learn(self, iterations, convergence=None):
        for _ in range(iterations):
            print('Position is {}'.format(self._pos))
            x = self._pos[0]
            y = self._pos[1]
            field = self._grid.get_grid_field(x, y)
            policy_of_field = self._grid.get_policy_field(x, y)
            print(field)
            print(policy_of_field)

            # selection of next state via the epsilon-soft policy
            if np.random.uniform() < self._epsilon_soft:
            # do (all possible) policy actions while checking if state exists
                action = field.get_movement_probs()[policy_of_field]
                a = np.argmax(self._q_table)
            else:
                # go explore
                direction = np.random.choice(DIRECTIONS)
                action = field.get_movement_probs()[direction]

            print('movement greedy selected')
            print(action)
            print('qTable')
            print(self._q_table)

            value = self._q_table[x, y]
            q_table_next = self._q_table
            for direction, probability in action.items():
                # go into direction
                x_next, y_next = np.add([x, y], DIRECTIONS_D[direction])
                # check if out of bounds
                if is_out_of_bounds(x_next, y_next, self._grid.shape):
                    x_next, y_next = [x, y]
                possible_next_field = self._grid.get_grid_field(x_next, y_next)
                # check if wall
                if not possible_next_field.can_move_here:
                    x_next, y_next = [x, y]
                # now we have a fully confirmed field
                next_field = self._grid.get_grid_field(x_next, y_next)
                #next_reward += probability * prev_array[x_next][y_next]# next array state or previous array state
                if next_field.type == 'P' or next_field.type == 'E':
                # return value when next field terminal
                    target_value = next_field.get_static_evaluation_value()
                else:
                    target_value = self._q_table[x_next, y_next] * self._gamma
                    ### ToDo
                # now change state according to action
                q_table_next[x_next, y_next] += self._learning_rate * (target_value - value)

            # check for convergence - difference of value arrays
            if convergence and self.check_convergence(self._q_table,
                                                      q_table_next,
                                                      convergence_value=convergence):
                print('convergence value reached...')
                break

            self._pos = x_next, y_next
            self._q_table = q_table_next

        #self._grid.set_eval_grid(new_array)

    def check_convergence(self, old_step, new_step, convergence_value=0.05):
        difference = 0
        for x, y in product(range(0, self._grid.shape_x), range(0, self._grid.shape_y)):
            difference = abs(old_step[y][x] - new_step[y][x])
        return difference < convergence_value


def is_out_of_bounds(x, y, shape):
    return x < 0 or y < 0 or x >= shape[0] or y >= shape[1] 
