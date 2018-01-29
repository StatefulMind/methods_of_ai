from itertools import product
import numpy as np
from Constants import DIRECTIONS, DIRECTIONS_D, NOMOVE

class Evaluator:
    '''
    Evaluates generated policy and improves on it
    '''

    def __init__(self, grid):
        self._grid = grid


    def iterate(self, iterations, step_cost, discount, convergence_epsilon = None):
        """
        Performs the policy iteration without an evaluation
        Writes the computations into eval_grid in our grid
        :param iterations: How many iterations of policy iteration should be done
        :param step_cost: The cost for every step done by the agent
        :param discount: The discount factor gamma
        :param convergence_epsilon: When in one iteration step the summed absolute change of the iteration fields change less than convergence_epsilon, the iteration is stopped due to convergence
        :return:
        """
        # succ_array_prev encodes the previous step of policy iteration
        succ_array_prev = [[0 for x in range(self._grid.shape_x)] for y in range(self._grid.shape_y)]


        for i in range(iterations):
            # succ_array_new encodes the recent step of policy iteration
            succ_array_new = [[0 for x in range(self._grid.shape_x)] for y in range(self._grid.shape_y)]

            for x, y in product(range(0, self._grid.shape_x), range(0, self._grid.shape_y)):
                policy = self._grid.get_policy_field(x, y) # The direction the policy dictates for that position
                field = self._grid.get_grid_field(x, y)

                # Goals and penalties have static evaluation values (e.g., 1 or -1) We can skip the iteration step here
                if field.has_static_evaluation_value:
                    succ_array_new[y][x] = field.get_static_evaluation_value()
                    continue

                # Get the probabilities to move to other directions than the policy dictates
                movement_probs = field.get_movement_probs()[policy]

                # Compute the rewards here for every possible direction of movement and sum them up
                successor_sum = 0
                for dir, movement_prob in movement_probs.items():
                    x_mv, y_mv = np.add([x, y], DIRECTIONS_D[dir])
                    if isOutOfBoundaries(x_mv, y_mv, self._grid.shape):
                        #Stay at the same field
                        x_mv, y_mv = [x, y]
                    elif not self._grid.get_grid_field(x_mv, y_mv).can_move_here:
                        x_mv, y_mv = [x, y]
                    successor_sum += movement_prob * succ_array_prev[y_mv][x_mv]

                # Sum the step_cost and the discounted rewards for our new future reward
                succ_array_new[y][x] = -step_cost + (discount ** i) * successor_sum

            # Checks if convergence appeared
            if not convergence_epsilon is None and self.convergence_check(succ_array_prev, succ_array_new, convergence_epsilon=convergence_epsilon):
                print("Stopped policy iteration due to convergence (delta < {})".format(convergence_epsilon))
                break

            succ_array_prev = succ_array_new
        self._grid.set_eval_grid(succ_array_new)

    def evaluate(self):
        """
        Performs policy evaluation.
        Assumes, that previously policy iteration has been calles and that a meaningful solution is in the eval_grid
        Writes the optimized policy into policy in _grid
        :return:
        """

        #For every possible direction we need to evaluate every single field
        eval_directions = {}
        for direction in DIRECTIONS:
            eval_directions[direction] = [[0 for x in range(self._grid.shape_x)] for y in range(self._grid.shape_y)]

            for x, y in product(range(0, self._grid.shape_x), range(0, self._grid.shape_y)):
                field = self._grid.get_grid_field(x, y)
                # Gets the probability to move to unwanted directions when performing the action of going to direction
                movement_probs = field.get_movement_probs()[direction]

                successor_sum = 0
                for dir_real, movement_prob in movement_probs.items():
                    x_mv, y_mv = np.add([x, y], DIRECTIONS_D[dir_real])
                    if isOutOfBoundaries(x_mv, y_mv, self._grid.shape):
                        # Stay at the same field
                        x_mv, y_mv = [x, y]
                    elif not self._grid.get_grid_field(x_mv, y_mv).can_move_here:
                        x_mv, y_mv = [x, y]
                    successor_sum += movement_prob * self._grid.get_eval_field(x_mv, y_mv)

                # Writing the expected future reward for going to direction from field x, y to the evaluation dictionary
                eval_directions[direction][y][x] = successor_sum

        # Setting up an empty matrix for our optimized policy
        new_policy = [[0 for x in range(self._grid.shape_x)] for y in range(self._grid.shape_y)]
        for x, y in product(range(0, self._grid.shape_x), range(0, self._grid.shape_y)):
            # For each field we find the optimal direction to go
            dir = {direction: eval_directions[direction][y][x] for direction in DIRECTIONS if not direction == NOMOVE}
            new_policy[y][x] = max(dir, key=dir.get)


        self._grid.set_policy_grid(new_policy)

    def convergence_check(self, old_iteration_step, new_iteration_step, convergence_epsilon):
        """
        Checks, if the iteration steps are closer to each other than convergence_epsilon
        :param old_iteration_step:
        :param new_iteration_step:
        :param convergence_epsilon:
        :return:
        """
        diff = 0
        for x, y in product(range(0, self._grid.shape_x), range(0, self._grid.shape_y)):
            diff += abs(old_iteration_step[y][x] - new_iteration_step[y][x])
        return diff < convergence_epsilon

def isOutOfBoundaries(x, y, shape):
    '''
    returns if iteration goes out of bounds - since outer walls are not defined and
    restricted by array length limits
    :param x:
    :param y:
    :param shape:
    :return:
    '''
    return x < 0 or y < 0 or x >= shape[0] or y >= shape[1]

