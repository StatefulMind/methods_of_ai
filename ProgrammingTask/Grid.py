import itertools
import argparse
from random import randint

from ProgrammingTask.GridField import GridField

# TODO eliminate those
# Maybe we can solve this differently? global variables are bad practive in Python
NOMOVE = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
GOAL = 'E'
PENALTY = 'P'

DIRECTIONS = [NOMOVE, UP, RIGHT, DOWN, LEFT]

NOMOVE_D = (0, 0)
UP_D = (-1, 0)
RIGHT_D = (0, 1)
DOWN_D = (1, 0)
LEFT_D = (0, -1)

DIRECTIONS_D = {NOMOVE: NOMOVE_D, UP: UP_D, RIGHT: RIGHT_D, DOWN: DOWN_D, LEFT: LEFT_D}

# use unicode arrows as directional symbols
DIRECTION_SYMBOLS = {NOMOVE: '\u220E',
                     UP: '\u2191',
                     RIGHT: '\u2192',
                     DOWN: '\u2193',
                     LEFT: '\u2190',
                     GOAL: '\u2302',
                     PENALTY: '\u058E'}

class Grid:
    '''
    Grid class, initializes grid from file, reads input file
    and instantiates fields accordingly.
    Writes grid-values to _grid.
    has get and set methods for field and string representation
    '''

    def __init__(self, grid_file, separator=" ", policy_grid=None, initial_policy_eval=None):
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
        self._policy_grid = policy_grid if policy_grid else self.set_random_policy()
        self._eval_grid = initial_policy_eval if initial_policy_eval else self.set_policy_evaluation_zero()

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

    def set_random_policy(self):
        '''
       Generate random initialisation of Directions for fields in policy grid
       :return array:
       '''
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                val = self.get_field(x, y)
                # exclude NOMOVE by starting at 1
                self._policy_grid[x][y] = (DIRECTIONS[randint(1, len(DIRECTIONS)-1)] if val is 'F'
                                           else DIRECTION_SYMBOLS[val])

        # random_directions = [[DIRECTIONS[randint(1, len(DIRECTIONS) - 1)] for y in range(self.shape[1])]
        #                      for x in range(self.shape[0])]
        # return random_directions
        return self._policy_grid

    def set_policy_evaluation_zero(self):
        '''
        initializes array of zero as initial evaluation grid
        :param shape:
        '''
        self._eval_grid = [[0 * x for x in range(self.shape[1])] for y in range(self.shape[0])]

    def print(self):
        '''
        Converts Grid values into direction symbols and print them
        '''
        field_string = ""
        line_old = 0
        for line, row in itertools.product(range(self.shape[0]), range(self.shape[1])):
            if not line_old == line:
                field_string += "\n"
                line_old = line
                # uses policy values (directions) as key-value for direction symbols
            field_string += DIRECTION_SYMBOLS[self._policy_grid[line][row]]
            field_string += " "
        print(field_string)


# instantiate parser
parser = argparse.ArgumentParser(description='''Read grid-file from stdin,
parse and print grid file accordingly.''')
parser.add_argument('grid_file', help='path to input .grid file')
# parser.add_argument('-i', '--iter', type='int',
#                   help='how many iterations are performed by the policy iteration', )
args = parser.parse_args()


def main():
    # those would be test cases - ToDo put into pytest under ./test when done
    grid = Grid(grid_file=args.grid_file)
    print(grid)
    print('Get field at [0,0]... {}'.format(grid.get_field(0, 0)))
    print('Get field at [1,1]... {}'.format(grid.get_field(1, 1)))
    grid.set_field(1, 1, "P")
    print('Adding Penalty at [1,1]...')
    print(grid)
    print('Get Shape Property of grid...')
    print(grid.shape)

    # get initial grid again
    dir_grid = Grid(grid_file=args.grid_file)
    # print directions string
    dir_grid.print()


if __name__ == '__main__':
    main()
