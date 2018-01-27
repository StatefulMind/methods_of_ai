import itertools
import numpy as np
from abc import ABC,
import argparse
import random

# Contains all Settings for the Task
# Values for fields and definitions of directions

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

DIRECTION_SYMBOLS = {NOMOVE: "o", UP: '\u25b2', RIGHT: '>', DOWN: 'V', LEFT: '<'}



class Grid:
    '''
    Grid class, initializes with Grid matrix from file
    has get and set methods for field and string representation
    '''

    # TODO Initialize field when constructor is called from input file...
    def __init__(self, matrix):
        self.__init__()
        self._grid = np.empty(matrix.shape, dtype=GridField.__class__)
        for x, y in itertools.product(range(matrix.shape[0]), range(matrix.shape[1])):
            field_type = matrix[x, y]
            self._grid[x, y] = GridField.factory(field_type)

    def __str__(self):
        out = ""
        for line in self._grid:
            for field in line:
                out += f' {str(field)} '
            out += "\n"
        return out

    def get_field(self, x, y):
        return self._grid[x, y]

    def set_field(self, x, y, obj):
        self._grid[x, y] = obj

    def get_grid(self):
        return self._grid

    @property
    def shape(self):
        return self._grid.shape

    def parse_to_matrix(self, filepath, separator=" "):
        """
        Reads a textfile to a matrix.
        Assumptions:Every line corresponds to one line of the matrix
        Every line has the same number of items
        separator is the sign with which weights are separated
        """
        array = []
        with open(filepath) as read_file:
            for line in read_file.readlines():
                weight_list = line.strip('\n').split(separator)
            array.append(weight_list)

        return array

    # return np.array(array, dtype = np.unicode_)


class PolicyEvaluationGridDepr(Grid):
    """
    Contains a policy evaluation.
    Every element of self._grid contains a dictionary,
    with the keys representing directions and the values representing probabilities.
    The values of every field have to sum up to 1.
    """

    def __init__(self, shape, initial_policy_evaluation=None):
        super().__init__()
        if initial_policy_evaluation is None:
            self.set_policy_evaluation_random(shape)
        else:
            self.set_policy_evaluation(initial_policy_evaluation)

    def set_policy_evaluation(self, policy_evaluation_grid):
        self._grid = policy_evaluation_grid

    def set_policy_evaluation_random(self, shape):
        """
        Generates a random policy evaluation.
        Every field in policy_grid sums up to 1, the indices of the dictionary indicate the direction
        """
        policy_grid = np.empty(shape, dtype=dict)
        content = {}
        for x, y in itertools.product(range(shape[0]), range(shape[1])):
            for (direction, value) in zip(DIRECTIONS, np.random.dirichlet(np.ones(len(DIRECTIONS)), size=1)[0]):
                content[direction] = value
            policy_grid[x, y] = content
        self.set_policy_evaluation(policy_grid)


class PolicyEvaluationGrid(Grid):
    """
    Contains a policy evaluation.
    2dimensional array with evaluation values
    """

    def __init__(self, shape, initial_policy_evaluation=None):
        super().__init__()
        if initial_policy_evaluation is None:
            self.set_policy_evaluation_zero(shape)
        else:
            self.set_policy_evaluation(initial_policy_evaluation)

    def set_policy_evaluation(self, policy_evaluation_grid):
        self._grid = policy_evaluation_grid

    def set_policy_evaluation_zero(self, shape):
        self._grid = np.zeros(shape)


class PolicyGrid(Grid):
    def __init__(self, shape, policy_grid=None):
        super().__init__()
        self._grid = np.empty(shape)
        if policy_grid is None:
            self.set_random_policy()
        else:
            self.set_policy(policy_grid)

    def set_policy(self, policy_grid):
        self._grid = policy_grid

    def set_random_policy(self):
        self.set_policy(np.random.choice([dir for dir in DIRECTIONS if not dir == NOMOVE], self._grid.shape))
        # self.set_policy(np.random.choice([dir for dir in DIRECTIONS], self._grid.shape))

    def print(self):
        field_string = ""
        line_old = 0
        for line, row in itertools.product(range(self.shape[0]), range(self.shape[1])):
            if not line_old == line:
                field_string += "\n"
                line_old = line
            field_string += DIRECTION_SYMBOLS[self.get_field(line, row)]
            field_string += " "
        print(field_string)


# ToDo REDUCE COMPLEXITY ELIMINATE GLOBAL VARIABLES, eliminate ABC for Field
class GridField(ABC):
    """Abstract Field Class for Fields in the Grid
    defines type property
    and __str__ method"""

    def __init__(self, field):
        super().__init__()
        self._type = field

    def factory(field):
        if field == 'F': return GridFieldField()
        if field == 'O': return GridFieldWall()
        if field == 'E': return GridFieldGoal()
        if field == 'P': return GridFieldPenalty()
        print("Unknown type!")

    def __str__(self):
        return str(self._type)

    @property
    def type(self):
        return self._type


class GridFieldField(GridField):
    '''
    Class containing the properties of the field field in the grid
    Adds movement probabilities and movement boolean
    Inherits type and __str__ function
    '''
    FIELD = "F"
    FIELD_PROBS = {'FIELD_PROB_NOMOVE': {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0},
                   'FIELD_PROB_UP': {NOMOVE: 0, UP: 0.8, RIGHT: 0.1, DOWN: 0, LEFT: 0.1},
                   'FIELD_PROB_RIGHT': {NOMOVE: 0, UP: 0.1, RIGHT: 0.8, DOWN: 0.1, LEFT: 0},
                   'FIELD_PROB_DOWN': {NOMOVE: 0, UP: 0, RIGHT: 0.1, DOWN: 0.8, LEFT: 0.1},
                   'FIELD_PROB_LEFT': {NOMOVE: 0, UP: 0.1, RIGHT: 0, DOWN: 0.1, LEFT: 0.8}}

    def __init__(self, FIELD, FIELD_PROBS):
        super().__init__(FIELD)
        self._FIELD_PROBS = FIELD_PROBS

    def get_movement_probs(self):
        return self._FIELD_PROBS

    @property
    def can_move_here(self):
        return True

    @property
    def has_static_evaluation_value(self):
        return False


class GridFieldWall(GridField):
    '''
    Class containing properties and probabilities of the wall field
    '''
    WALL = 'O'
    WALL_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}
    WALL_PROBS = {NOMOVE: WALL_PROB_ANY, UP: WALL_PROB_ANY, RIGHT: WALL_PROB_ANY, DOWN: WALL_PROB_ANY,
                  LEFT: WALL_PROB_ANY}

    def __init__(self, WALL, WALL_PROB_ANY, WALL_PROBS):
        super().__init__(WALL)
        self._WALL_REWARD = 0
        self._WALL_PROB_ANY = WALL_PROB_ANY
        self._WALL_PROBS = WALL_PROBS

    def get_movement_probs(self, **kwargs):
        return self._WALL_PROB_ANY

    @property
    def can_move_here(self):
        return False

    @property
    def has_static_evaluation_value(self):
        return True

    def get_static_evaluation_value(self):
        return self._WALL_REWARD


class GridFieldPenalty(GridField):
    '''
    Class containing properties for the Penalty Field
    '''

    PENALTY = "P"
    PENALTY_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}
    PENALTY_PROBS = {NOMOVE: PENALTY_PROB_ANY, UP: PENALTY_PROB_ANY, RIGHT: PENALTY_PROB_ANY, DOWN: PENALTY_PROB_ANY,
                     LEFT: PENALTY_PROB_ANY}


    def __init__(self, PENALTY, PENALTY_PROBS, PENALTY_PROBS_ANY):
        super().__init__(PENALTY)
        self._PENALTY_PROBS = PENALTY_PROBS
        self._PENALTY_REWARD = -1

    def get_movement_probs(self, **kwargs):
        return self._PENALTY_PROBS

    @property
    def can_move_here(self):
        return True

    @property
    def has_static_evaluation_value(self):
        return True

    def get_static_evaluation_value(self):
        return self._PENALTY_REWARD

]
class GridFieldGoal(GridField):
    '''
    Class containing properties for the Goal Field
    '''

    GOAL = "E"
    GOAL_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}
    GOAL_PROBS = {NOMOVE: GOAL_PROB_ANY, UP: GOAL_PROB_ANY, RIGHT: GOAL_PROB_ANY, DOWN: GOAL_PROB_ANY,
                  LEFT: GOAL_PROB_ANY}

    def __init__(self, GOAL, GOAL_PROBS):
        super().__init__(GOAL)
        self._GOAL_REWARD = 1
        self._GOAL_PROBS = GOAL_PROBS

    def get_movement_probs(self):
        return self._GOAL_PROBS

    @property
    def can_move_here(self):
        return True

    @property
    def has_static_evaluation_value(self):
        return True

    def get_static_evaluation_value(self):
        return self._GOAL_REWARD


# instantiate parser
parser = argparse.ArgumentParser(description='''Read grid-file from stdin,
parse and print grid file accordingly.''')
parser.add_argument('gridfile', help='path to input .grid file')
parser.add_argument('-i', '--iter', type='int',
                    help='how many iterations are performed by the policy iteration', )
args = parser.parse_args()


def main():
    grid = Grid(args.gridfile)


if __name__ == '__main__':
    main()
