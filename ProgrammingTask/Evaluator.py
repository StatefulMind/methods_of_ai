from Grid import Grid

class Evaluator:
    '''
    Evaluates generated policy and improves on it
    '''

    def __int__(self, grid):
        self._grid = grid

    def evaluate(self):
