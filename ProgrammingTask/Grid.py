import itertools
from GridSettings import *
from GridField import GridField
import numpy as np
from abc import ABC, abstractmethod
import random

# Contains all Settings for the Task
# Values for fields and definitions of directions

GOAL = "E"
PENALTY = "P"
FIELD = "F"
WALL = "O"

TYPES = [GOAL, PENALTY, FIELD, WALL]


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

FIELD_PROB_NOMOVE = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}
FIELD_PROB_UP = {NOMOVE: 0, UP: 0.8, RIGHT: 0.1, DOWN: 0, LEFT: 0.1}
FIELD_PROB_RIGHT = {NOMOVE: 0, UP: 0.1, RIGHT: 0.8, DOWN: 0.1, LEFT: 0}
FIELD_PROB_DOWN = {NOMOVE: 0, UP: 0, RIGHT: 0.1, DOWN: 0.8, LEFT: 0.1}
FIELD_PROB_LEFT = {NOMOVE: 0, UP: 0.1, RIGHT: 0, DOWN: 0.1, LEFT: 0.8}

FIELD_PROBS = {NOMOVE: FIELD_PROB_NOMOVE, UP: FIELD_PROB_UP, RIGHT: FIELD_PROB_RIGHT, DOWN: FIELD_PROB_DOWN,
               LEFT: FIELD_PROB_LEFT}

GOAL_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}
GOAL_PROBS = {NOMOVE: GOAL_PROB_ANY, UP: GOAL_PROB_ANY, RIGHT: GOAL_PROB_ANY, DOWN: GOAL_PROB_ANY,
              LEFT: GOAL_PROB_ANY}
GOAL_REWARD = 1

PENALTY_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}
PENALTY_PROBS = {NOMOVE: PENALTY_PROB_ANY, UP: PENALTY_PROB_ANY, RIGHT: PENALTY_PROB_ANY, DOWN: PENALTY_PROB_ANY,
                 LEFT: PENALTY_PROB_ANY}
PENALTY_REWARD = -1

WALL_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}
WALL_PROBS = {NOMOVE: WALL_PROB_ANY, UP: WALL_PROB_ANY, RIGHT: WALL_PROB_ANY, DOWN: WALL_PROB_ANY,
              LEFT: WALL_PROB_ANY}
WALL_REWARD = 0

MOVEMENT_PROBS = {FIELD: FIELD_PROBS, GOAL: GOAL_PROBS, PENALTY: PENALTY_PROBS,
                  WALL: WALL_PROBS}

class Grid(ABC):
    '''
    Abstract Grid class
    '''

    def __init__(self):
        super().__init__()
        self._grid = None

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


class FieldGrid(Grid):
    """
    Contains a Field with O, E, P,...
    """
    def __init__(self, matrix):
        super().__init__()
        self._grid = np.empty(matrix.shape, dtype=GridField.__class__)
        for x, y in itertools.product(range(matrix.shape[0]), range(matrix.shape[1])):
            fieldType = matrix[x, y]
            self._grid[x, y] = GridField.factory(fieldType)


class PolicyEvaluationGridDepr(Grid):
    """
    Contains a policy evaluation.
    Every element of self._grid contains a dictionary,
    with the keys representing directions and the values representing probabilities.
    The values of every field have to sum up to 1.
    """
    def __init__(self, shape, initial_policy_evaluation = None):
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
            #content[DIRECTIONS] = np.random.dirichlet(np.ones(len(DIRECTIONS)),size=1)
            #content = dict((DIRECTIONS, np.random.dirichlet(np.ones(len(DIRECTIONS)),size=1)))
            for (direction, value) in zip(DIRECTIONS, np.random.dirichlet(np.ones(len(DIRECTIONS)),size=1)[0]):
                content[direction] = value
            policy_grid[x, y] = content
        self.set_policy_evaluation(policy_grid)


class PolicyEvaluationGrid(Grid):
    """
    Contains a policy evaluation.
    2dimensional array with evaluation values
    """
    def __init__(self, shape, initial_policy_evaluation = None):
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
    def __init__(self, shape, policy_grid = None):
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
        #self.set_policy(np.random.choice([dir for dir in DIRECTIONS], self._grid.shape))

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

class GridField(ABC):
    """Abstract Field Class"""
    def __init__(self, type):
        self._type = type
        super().__init__()

    @abstractmethod
    def get_movement_probs(self, type):
        return MOVEMENT_PROBS[type]

    def factory(type):
        if type == FIELD: return GridFieldField()
        if type == WALL: return GridFieldWall()
        if type == GOAL: return GridFieldGoal()
        if type == PENALTY: return GridFieldPenalty()
        print("Unknown type!")

    def __str__(self):
        return str(self._type)

    @property
    @abstractmethod
    def canMoveHere(self):
        pass

    @property
    @abstractmethod
    def hasStaticEvaluationValue(self):
        pass

    @property
    def type(self):
        return self._type

class GridFieldField(GridField):
    def __init__(self):
        super().__init__(FIELD)

    def get_movement_probs(self):
        return super().get_movement_probs(FIELD)

    @property
    def canMoveHere(self):
        return True

    @property
    def hasStaticEvaluationValue(self):
        return False

class GridFieldWall(GridField):
    def __init__(self):
        super().__init__(WALL)

    def get_movement_probs(self):
        return super().get_movement_probs(WALL)

    @property
    def canMoveHere(self):
        return False

    @property
    def hasStaticEvaluationValue(self):
        return True

    def getStaticEvaluationValue(self):
        return WALL_REWARD


class GridFieldPenalty(GridField):
    def __init__(self):
        super().__init__(PENALTY)

    def get_movement_probs(self):
        return super().get_movement_probs(PENALTY)

    @property
    def canMoveHere(self):
        return True

    @property
    def hasStaticEvaluationValue(self):
        return True

    def getStaticEvaluationValue(self):
        return PENALTY_REWARD

class GridFieldGoal(GridField):
    def __init__(self):
        super().__init__(GOAL)

    def get_movement_probs(self):
        return super().get_movement_probs(GOAL)

    @property
    def canMoveHere(self):
        return True

    @property
    def hasStaticEvaluationValue(self):
        return True

    def getStaticEvaluationValue(self):
        return GOAL_REWARD


def parse_to_matrix(filepath, separator = " "):
    """
    By: Jan
    Reads a textfile to a matrix.
    Assumptions:Every line corresponds to one line of the matrix
    Every line has the same number of items
    separator is the sign with which weights are separated
    """
    file = open(filepath, "r")

    array = []

    for line in file.readlines():
        weight_list = line.strip('\n').split(separator)
        array.append(weight_list)

    return array
	#return np.array(array, dtype = np.unicode_)