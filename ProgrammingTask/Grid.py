import itertools
from GridSettings import *
from GridField import GridField
import numpy as np
from abc import ABC, abstractmethod
import random


class Grid(ABC):
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