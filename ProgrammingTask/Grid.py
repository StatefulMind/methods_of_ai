import itertools
import argparse
from random import randint

from ProgrammingTask.GridField import GridField

# TODO eliminate those
# Maybe we can solve this differently? global variables are bad practive in Python
NOMOVE  = 0
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
    Grid class, initializes grid from file, reads input file
    and instantiates fields accordingly
    has get and set methods for field and string representation
    '''

    def __init__(self, grid_file, separator=" ", policy_grid=None):
        '''
        Constructor of Grid takes input file and reads it into array
        that is used to instantiate the Fields from GridFields
        bound to _grid
        :param grid_file:
        :param separator:
        '''
        self._array = []
        with open(grid_file) as read_file:
            for line in read_file.readlines():
                weight_list = line.strip('\n').split(separator)
                self._array.append(weight_list)
        # use grid values as input for field factory and instantiate the grid
        self._grid = [[GridField.factory(field_type) for field_type in line] for line in self._array]
        self._policy_grid = self.set_policy(policy_grid) if policy_grid else self.set_random_policy()

    def __str__(self):
        out = ""
        for line in self._grid:
            for field in line:
                out += f' {str(field)} '
            out += "\n"
        return out

    def get_field(self, x, y):
        return self._grid[x][y]

    def set_field(self, x, y, obj):
        self._grid[x][y] = obj

    def get_grid(self):
        return self._grid

    @property
    def shape(self):
        x = len(self._grid)
        y = len(self._grid[0])
        return [x, y]

    def set_policy(self, policy_grid):
        self._grid = policy_grid

    def set_random_policy(self):
       # generate random initialisation of Direction array - exclude NOMOVE by starting at 1
       random_directions = [[DIRECTIONS[randint(1, len(DIRECTIONS))] for y in range(self.shape[1])]
                                 for x in range(self.shape[0])]
       self.set_policy(random_directions)


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


    def __str__(self):
        field_string = ""
        line_old = 0
        for line, row in itertools.product(range(self.shape[0]), range(self.shape[1])):
            if not line_old == line:
                field_string += "\n"
                line_old = line
            field_string += DIRECTION_SYMBOLS[self.get_field(line, row)]
            field_string += " "
        return field_string


# instantiate parser
parser = argparse.ArgumentParser(description='''Read grid-file from stdin,
parse and print grid file accordingly.''')
parser.add_argument('grid_file', help='path to input .grid file')
#parser.add_argument('-i', '--iter', type='int',
#                   help='how many iterations are performed by the policy iteration', )
args = parser.parse_args()


def main():
    # those would be test cases - ToDo put into pytest under ./test when done
    grid = Grid(grid_file=args.grid_file)
    print(grid)
    print('Get field at [0,0]... {}'.format(grid.get_field(0,0)))
    print('Get field at [1,1]... {}'.format(grid.get_field(1,1)))
    grid.set_field(1,1,"P")
    print('Adding Penalty at [1,1]...')
    print(grid)
    print('Get Shape Property of grid...')
    print(grid.shape)


if __name__ == '__main__':
    main()
