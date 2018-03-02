from itertools import product
import numpy as np
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

    def learn(self, iterations, convergence=None):
        for _ in range(iterations):
            x = self._pos[0]
            y = self._pos[1]
            field = self._grid.get_grid_field(x, y)
            policy_of_field = self._grid.get_policy_field(x, y)
            print(field)
            print(policy_of_field)
            # array in the same shape for adding values later
            new_array = [[0 for _ in range(self._grid.shape_x)] for _ in range(self._grid.shape_y)]

            # selection of next state via the epsilon-soft policy
            if np.random.uniform() < self.epsilon:
            # do (all possible) policy actions while checking if state exists
                movement = field.get_movement_probs()[policy_of_field]
                # go greedy
                # max(do_movement)
            else:
                # go explore
                direction = np.random.choice(DIRECTIONS)
                movement = field.get_movement_probs()[direction]
                
            next_reward = 0
            for direction, probability in movement.items():
                # go into direction
                x_next, y_next = np.add([x, y], DIRECTIONS_D[direction])
                possible_next_field = self._grid.get_grid_field(x_next, y_next)
                # check if out of bounds
                if is_out_of_bounds(x_next, y_next, self._grid.shape):
                    x_next, y_next = [x, y]
                elif not possible_next_field.can_move_here:
                    x_next, y_next = [x, y]
                next_reward += probability * prev_array[x_next][y_next]# next array state or previous array state
                if possible_next_field.type == 'P' or possible_next_field.type == 'E':
                    # return value when next field terminal
                    new_array[x_next][y_next] = possible_next_field.get_static_evaluation_value()
                else:
                    new_array[x_next][y_next] -= (possible_next_field.get_static_evaluation_value()
                                                  * self._gamma * #Q_table max value)
                    ### ToDo




            # check for convergence - difference of value arrays
            if not convergence is None and self.check_convergence(prev_array, new_array,
                                                                  convergence_value=convergence):
                print('convergence value reached...')
                break

            prev_array = new_array
        self._grid.set_eval_grid(new_array)


        print(field_field.get_movement_probs()[policy_of_field])

    # action corresponds to MOVEMENT > FROM MOVEMENT_D by policy
    def apply_epsilon(self, action):
        return np.random.uniform(#SOMETHING) # choose with epsilon soft policy from possible movements

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
