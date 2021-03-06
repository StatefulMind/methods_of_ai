from itertools import product
import numpy as np
from time import sleep
import sys
from Constants import DIRECTIONS, DIRECTIONS_D, NOMOVE, DIRECTION_SYMBOLS
import pandas as pd
from UI import check_next_episode
from UI import check_next_step

# NOMOVE breaks the q_table movement implementation
DIRECTIONS.remove(NOMOVE)


class Learner:
    """
    The Learner generates a random policy and improves on it
    """

    def __init__(self, grid, position_flag='static',
                 learning_rate=0.5, gamma=0.9,
                 reward_decay=0.04, epsilon_soft=0.4):
        self._grid = grid
        self._position_flag = position_flag
        self._pos = self.start_position()
        self._learning_rate = learning_rate
        self._gamma = gamma
        self._reward_decay = reward_decay
        # already calculate the epsilon value
        self._epsilon_soft = 1 - epsilon_soft + epsilon_soft/4
        self._q_table = self.init_q_table()

    @property
    def _state(self):
        """
        Returns a string representation of the recent position of the agent
        as index for the pandas dataframe
        """
        return 's({})'.format(self._pos)

    def start_position(self):
        """
        Generates starting position for the agent depending on the given
        start_position flag
        :return 'random' or 'static':
        """
        if self._position_flag == 'static':
            print('Start Position is (0,0)')
            # start is left corner - x coordinate corresponds to 0 and max y
            return 0, self._grid.shape_y - 1
        if self._position_flag == 'random':
            # pull random position
            random_pos = self.random_start()
            # as long as it is not a field repeat
            while not self._grid.get_grid_field(random_pos[0], random_pos[1]).type == 'F':
                random_pos = self.random_start()
            return random_pos

    def random_start(self):
        """ randomly selects integers in range of grid for start value
        :return x, y: """
        return np.random.randint(self._grid.shape_x), np.random.randint(
            self._grid.shape_y)

    def print_and_quit(self):
        """
        Prints the best found policy with the corresponding evaluation and terminates the program.
        """
        print("Ending the program")
        print("The final policy is:")
        self._grid.print_policy()
        print("\nThe evaluation values of this policy are:")
        self.print_max_q_table()
        print("Thank you for running our program")
        sys.exit(0)

    def learn(self, episodes=100, convergence=0.00001,
              interactive='automatic', delay_time=0):
        """ applies q-learning with the q_table from the class as DataFrame over
        the given episodes while updating the q_table or terminating when
        convergence value is reached
        selects starting position - goes in direction given by the policy or
        explores randomly depending on the soft-epsilon criterion"""

        converged = False
        for _e in range(episodes):
            # run a new episode

            # check if the user is interested in running another episode
            if interactive == 'interactive' and not check_next_episode():
                self.print_and_quit()

            # assign a start_position to the agent
            self._pos = self.start_position()

            while True:
                # check if the user is interested in doing another evaluation step
                if interactive == 'interactive' and not check_next_step():
                    self.print_and_quit()

                is_terminal = False
                x = self._pos[0]
                y = self._pos[1]
                field = self._grid.get_grid_field(x, y)
                policy_of_field = self._grid.get_policy_field(x, y)

                # clone DIRECTIONS array to not have side effects
                direction_copy = DIRECTIONS[:]
                # selection of next state via the epsilon-soft policy
                if np.random.uniform() < self._epsilon_soft:
                    # policy of field corresponds with the greedy action (after 1st iteration)
                    direction = policy_of_field
                    action_probs = field.get_movement_probs()[direction]
                    print('Movement greedily selected: {}'.format(DIRECTION_SYMBOLS[direction]))
                else:
                    # go explore randomly in all other directions
                    # first remove the greedy direction
                    direction_copy.remove(policy_of_field)
                    if NOMOVE in direction_copy:
                        direction_copy.remove(NOMOVE)
                    direction = np.random.choice(direction_copy)
                    action_probs = field.get_movement_probs()[direction]
                    print('Movement not greedily selected: {}'.format(DIRECTION_SYMBOLS[direction]))

                value = self._q_table.ix[self._state, direction]
                q_table_next = self._q_table.copy()
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
                    target_value = next_field.get_static_evaluation_value() - self._reward_decay
                    is_terminal = True
                else:
                    # new reward value taken from q table and actual taken action after uncertainty calculations
                    target_value = self._gamma * self._q_table.loc['s({})'.format((x_next, y_next))].max() - self._reward_decay
                # now change state according to action
                q_table_next.ix[self._state, direction] += self._learning_rate * (target_value - value)

                # update policy in direction with max value from original position in q_table
                maximizing_direction = q_table_next.loc[self._state].argmax()
                self._grid.set_policy_field(x, y, maximizing_direction)

                # update the state after the applied action
                self._pos = x_next, y_next

                print('Policy after doing the step')
                # print(self._grid.get_policy_grid())
                self._grid.print_policy(pos=self._pos)
                print("")

                if interactive == 'interactive':
                    print("Corresponding table of evaluated values")
                    self.print_max_q_table()
                    print("")

                # check for convergence - difference of value arrays
                if convergence and check_convergence(self._q_table,
                                                     q_table_next,
                                                     convergence_value=convergence):
                    print('Convergence value reached...')
                    converged = True
                    break

                # Update the q_table
                self._q_table = q_table_next
                sleep(delay_time)

                if is_terminal:
                    break
                print("\n")

            if converged:
                print('The Q-Learner converged')
                self.print_and_quit()
            else:
                print("Episode finished. Policy after this episode:")
                self._grid.print_policy()
                print("\nCorresponding table of evaluated values")
                self.print_max_q_table()
                print("")
        print("Finished evaluating {} episodes.\n".format(episodes))

    def init_q_table(self):
        """
        Initializes a q_table as a pandas DataFrame.
        Because there are some issues with tuples as indices,
        we use strings of the positions as indices.
        :return: The new pandas DataFrame initialized with 0s
        """
        states = ['s({})'.format(i) for i in product(range(self._grid.shape_x), range(self._grid.shape_y))]
        return pd.DataFrame(0, index=states, columns=DIRECTIONS)

    def print_max_q_table(self):
        """
        Prints the maximal values of the q_table for each position in the field.
        This value corresponds to the direction given by the policy.
        """
        field_string = ""
        line_old = 0

        for y, x in product(range(self._grid.shape_y), range(self._grid.shape_x)):
            if not line_old == y:
                field_string += "\n"
                line_old = y
            field_string += str(float(np.round(self._q_table.loc['s({})'.format((x, y))].max(), 2)))
            field_string += " "
        print(field_string)


def check_convergence(old_step, new_step, convergence_value=0.05):
        """takes difference of old q_table and new q_table, takes absolute value
        of all values and compares it to the convergence value"""
        difference = abs(new_step.subtract(old_step).values.sum())
        return difference < convergence_value


def is_out_of_bounds(x, y, shape):
    return x < 0 or y < 0 or x >= shape[0] or y >= shape[1]


def choose_action(value_list):
    """
    chooses action to take from sorted input of possible actions,
    where the highest probability by sorted item corresponds to
    80% probability of moving there
    :param value_list:
    :return direction int: choose from 1, 2, 3, 4
    """
    random_value = np.random.uniform()
    if random_value < 0.8:
        return value_list[0][0]
    elif random_value < 0.9:
        return value_list[1][0]
    else:
        return value_list[2][0]
