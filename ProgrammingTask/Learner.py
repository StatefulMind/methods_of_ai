import numpy as np
from Constants import DIRECTIONS, DIRECTIONS_D, NOMOVE

class Learner:
    '''
    Learner generated policy and improves on it
    '''

    def __init__(self, grid):
        self._grid = grid

