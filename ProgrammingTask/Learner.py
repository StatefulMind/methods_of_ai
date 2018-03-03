from itertools import product
import numpy as np
from time import sleep
from Constants import DIRECTIONS, DIRECTIONS_D, NOMOVE
import pandas as pd


class Learner:
    '''
    Learner generated policy and improves on it
    '''

    def __init__(self, grid, position='static', learning_rate=0.5, gamma=0.9,
                 reward_decay=0.04, epsilon_soft=0.4):
        self._grid = grid
        self._position_flag = position
        self._pos = self.start_position()
        self._learning_rate = learning_rate
        self._gamma = gamma
        self._reward_decay = reward_decay
        # already calculate the epsilon value
        self._epsilon_soft = 1 - epsilon_soft + epsilon_soft/4
        #self._q_table = np.zeros((self._grid.shape_y, self._grid.shape_x))
        self._q_table = self.init_q_table()

    def start_position(self):
        if self._position_flag == 'static':
            print('Start Position is (0,0)')
            # starting point is left corner - x coordinate corresponds to 0 and max y
            return 0, self._grid.shape_y - 1
        if self._position_flag == 'random':
            # pull random position
            random_pos = self.random_start()
            # as long as it is not a field repeat
            while not self._grid.get_grid_field(random_pos[0], random_pos[1]).type == 'F':
                random_pos = self.random_start()
            return random_pos

    def random_start(self):
        return np.random.randint(self._grid.shape_x), np.random.randint(self._grid.shape_y)

    # def learn(self, iterations, convergence=None):
    #     # when starting randomly pick for each new run a new starting position
    #     for e in range(self._episodes):
    #         self._pos = self.start_position()
    #
    #         for _ in range(iterations):
    #             is_terminal = False
    #             print('Position is {}'.format(self._pos))
    #             x = self._pos[0]
    #             y = self._pos[1]
    #             field = self._grid.get_grid_field(x, y)
    #             policy_of_field = self._grid.get_policy_field(x, y)
    #             print(field)
    #             print(policy_of_field)
    #
    #             # clone DIRECTIONS array to not have side effects
    #             direction_copy = DIRECTIONS[:]
    #             # selection of next state via the epsilon-soft policy
    #             if np.random.uniform() < self._epsilon_soft:
    #                 # policy of field corresponds with the greedy action (after 1st iteration)
    #                 action = field.get_movement_probs()[policy_of_field]
    #                 print('movement greedily selected')
    #             else:
    #                 # go explore randomly in all other directions
    #                 # first remove the greedy direction
    #                 direction_copy.remove(policy_of_field)
    #                 direction = np.random.choice(direction_copy)
    #                 action = field.get_movement_probs()[direction]
    #                 print('movement not greedily selected')
    #
    #
    #             print(action)
    #             print('qTable')
    #             print(self._q_table)
    #
    #             value = self._q_table[y, x]
    #             q_table_next = self._q_table
    #             # action by movement probability, sort directions by their probabilities
    #             relevant_action_probabilities = sorted(action.items(), key=lambda val: val[1],
    #                                                    reverse=True)[:3]
    #             decided_action = choose_action(relevant_action_probabilities)
    #
    #             # go into direction
    #             x_next, y_next = np.add([x, y], DIRECTIONS_D[decided_action])
    #             # check if out of bounds
    #             if is_out_of_bounds(x_next, y_next, self._grid.shape):
    #                 x_next, y_next = [x, y]
    #             possible_next_field = self._grid.get_grid_field(x_next, y_next)
    #             # check if wall
    #             if not possible_next_field.can_move_here:
    #                 x_next, y_next = [x, y]
    #             # now we have a fully confirmed field
    #             next_field = self._grid.get_grid_field(x_next, y_next)
    #
    #             if next_field.type == 'P' or next_field.type == 'E':
    #                 # return value when next field terminal
    #                 target_value = next_field.get_static_evaluation_value()
    #                 is_terminal = True
    #             else:
    #                 target_value = self._q_table[y_next, x_next] - self._gamma
    #                 # ToDo
    #             # now change state according to action
    #             q_table_next[y_next, x_next] += self._learning_rate * (target_value - value)
    #
    #             # check for convergence - difference of value arrays
    #             if convergence and check_convergence(self._q_table,
    #                                                  q_table_next,
    #                                                  convergence_value=convergence):
    #                 print('convergence value reached...')
    #                 break
    #             # round values
    #             q_table_next = np.round(q_table_next, decimals=2)
    #             # update the policy so that the next greedy pick is optimal
    #             self._grid.set_policy_field(x, y, self.max_direction())
    #
    #             # update the state after the applied action
    #             self._pos = x_next, y_next
    #             self._q_table = q_table_next
    #             sleep(2)
    #
    #             if is_terminal:
    #                 break
    #
    #             print('Policy now...')
    #             print(self._grid.get_policy_grid())

    def learn(self, episodes=3, iterations=20, convergence=0.1):
        # when starting randomly pick for each new run a new starting position
        for _e in range(episodes):
            self._pos = self.start_position()

            for _ in range(iterations):
                is_terminal = False
                print('Position is {}'.format(self._pos))
                x = self._pos[0]
                y = self._pos[1]
                field = self._grid.get_grid_field(x, y)
                policy_of_field = self._grid.get_policy_field(x, y)
                print(field)
                print(policy_of_field)

                # clone DIRECTIONS array to not have side effects
                direction_copy = DIRECTIONS[:]
                # selection of next state via the epsilon-soft policy
                if np.random.uniform() < self._epsilon_soft:
                    # policy of field corresponds with the greedy action (after 1st iteration)
                    direction = policy_of_field
                    action_probs = field.get_movement_probs()[direction]
                    print('movement greedily selected')
                else:
                    # go explore randomly in all other directions
                    # first remove the greedy direction
                    direction_copy.remove(policy_of_field)
                    direction = np.random.choice(direction_copy)
                    action_probs = field.get_movement_probs()[direction]
                    print('movement not greedily selected')

                # use this direction for indexing the q_table
                print('Direction {}'.format(direction))
                print(action_probs)


                print('q-Table')
                print(self._q_table)

                value = self._q_table[self._pos, direction]
                q_table_next = self._q_table
                # action by movement probability, sort directions by their probabilities
                relevant_action_probabilities = sorted(action_probs.items(), key=lambda val: val[1],
                                                       reverse=True)[:3]
                make_action = choose_action(relevant_action_probabilities)

                # go into direction
                x_next, y_next = np.add([x, y], DIRECTIONS_D[make_action])
                # check if out of bounds
                if is_out_of_bounds(x_next, y_next, self._grid.shape):
                    x_next, y_next = [x, y]
                possible_next_field = self._grid.get_grid_field(x_next, y_next)
                # check if wall
                if not possible_next_field.can_move_here:
                    x_next, y_next = [x, y]
                # now we have a fully confirmed field
                next_field = self._grid.get_grid_field(x_next, y_next)
                if next_field.type == 'P' or next_field.type == 'E':
                    # return value when next field terminal
                    target_value = next_field.get_static_evaluation_value()
                    is_terminal = True
                else:
                    # new reward value taken from q table and actual taken action after uncertainty calculations
                    target_value = self._gamma * q_table.ix[(y, x), make_action] - self._reward_decay
                # now change state according to action
                q_table_next.ix[self._pos, direction] += self._learning_rate * (target_value - value)

                # check for convergence - difference of value arrays
                if convergence and check_convergence(q_table,
                                                     q_table_next,
                                                     convergence_value=convergence):
                    print('convergence value reached...')
                    break

                # update the policy so that the next greedy pick is optimal
                # self._grid.set_policy_field(x, y, self.max_direction())
                # update policy in direction with max value from original position in q_table
                maximizing_direction = q_table_next.ix[self._pos, :].max().index[0]
                self._grid.set_policy_field(x, y, maximizing_direction)

                # update the state after the applied action
                self._pos = x_next, y_next
                q_table = q_table_next
                sleep(2)

                if is_terminal:
                    break

                print('Policy now...')
                print(self._grid.get_policy_grid())

    def max_direction(self):
        """evaluate the best next position from current position
        iterate over all possible directions and
        choose max for best policy"""
        # sum for all possible directions and
        nearest_values = []
        for direction in DIRECTIONS[1:4]:
            # get value from the direction you're going
            iter_x, iter_y = np.add([self._pos[0], self._pos[1]], DIRECTIONS_D[direction])
            try:
                value = self._q_table[iter_y][iter_x]
            except IndexError:
                continue
            nearest_values.append((direction, value))
        # return the direction from the corresponding max value
        max_direction = max(nearest_values, key=lambda x: x[1])[0]
        return max_direction

    def init_q_table(self):
        states = [i for i in product(range(self._grid.shape_x), range(self._grid.shape_y))]
        return pd.DataFrame(0, index=states, columns=DIRECTIONS[1:])


def check_convergence(old_step, new_step, convergence_value=0.05):
        """takes difference of old q_table and new q_table, takes absolute value
        of all values and compares it to the convergence value"""
        difference = abs(new_step.subtract(old_step).values.sum())
        return difference < convergence_value


def is_out_of_bounds(x, y, shape):
    return x < 0 or y < 0 or x >= shape[0] or y >= shape[1]


def choose_action(value_list):
    random_value = np.random.uniform()
    if random_value < 0.8:
        return value_list[0][0]
    elif random_value < 0.9:
        return value_list[1][0]
    else:
        return value_list[2][0]



