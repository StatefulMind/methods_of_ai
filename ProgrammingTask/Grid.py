import itertools
import random
from Constants import DIRECTIONS, DIRECTION_SYMBOLS, UP, RIGHT, DOWN, LEFT

from GridField import GridField

class Grid:
    '''
    Grid class, initializes grid from file, reads input file
    and instantiates fields accordingly.
    Writes grid-values to _grid.
    has get and set methods for field and string representation
    '''

    def __init__(self, grid_file, policy_grid=None, initial_policy_eval=None):
        '''
        Constructor of Grid takes input file and reads it into array
        that is used to instantiate the Fields from GridFields
        bound to _grid
        :param grid_file: Filepath to a file representing a grid. Expects valid inputs. Fields should be separated by separator, lines should end with '\n'
        '''
        separator = " "

        self._array = []
        with open(grid_file) as read_file:
            for line in read_file.readlines():
                weight_list = line.strip('\n').split(separator)
                self._array.append(weight_list)
        # use grid values as input for field factory and instantiate the grid
        self._grid = [[GridField.factory(field_type) for field_type in line] for line in self._array]
        # instantiate the policy grid if parsed otherwise initialise randomly
        self._policy_grid = policy_grid if policy_grid else self.set_random_policy()
        # instantiate evaluation grid if given otherwise initialise with zero array
        self._eval_grid = initial_policy_eval if initial_policy_eval else self.set_policy_evaluation_zero()


    def __str__(self):
        return self.get_grid_str()

    def get_grid_field(self, x, y):
        return self._grid[y][x]

    def get_policy_field(self, x, y):
        return self._policy_grid[y][x]

    def get_eval_field(self, x, y):
        return self._eval_grid[y][x]

    def set_grid_field(self, x, y, obj):
        self._grid[y][x] = obj

    def set_policy_field(self, x, y, obj):
        self._policy_grid[y][x] = obj

    def set_eval_field(self, x, y, obj):
        self._eval_grid[y][x] = obj

    def get_grid(self):
        return self._grid

    def get_policy_grid(self):
        return self._policy_grid

    def set_policy_grid(self, grid):
        self._policy_grid = grid

    def get_eval_grid(self):
        return self._eval_grid

    def set_eval_grid(self, grid):
        self._eval_grid = grid

    @property
    def shape(self):
        return [self.shape_x, self.shape_y]

    @property
    def shape_x(self):
        return len(self._grid[0])

    @property
    def shape_y(self):
        return len(self._grid)

    def set_random_policy(self):
        '''
       Generate random initialisation of directions for fields in policy grid
       :return array: Random policy
       '''
        random_directions = [[random.choice([UP, RIGHT, DOWN, LEFT]) for x in range(self.shape_x)]
                             for y in range(self.shape_y)]
        self._policy_grid = random_directions
        return self._policy_grid

    def set_policy_evaluation_zero(self):
        '''
        initializes array of zero as initial evaluation grid
        :return array: Zero evaluation
        '''
        self._eval_grid = [[0 for x in range(self.shape_x)] for y in range(self.shape_y)]
        return self._eval_grid

    def get_policy_str(self):
        '''
        Converts policy values into direction symbols
        :return String: representation of the field
        '''

        field_string = ""
        line_old = 0
        for y, x in itertools.product(range(self.shape_y), range(self.shape_x)):
            if not line_old == y:
                field_string += "\n"
                line_old = y
                # uses policy values (directions) as key-value for direction symbols

            # If a grid field provides a symbol (every field to which or from which you can not move should do that),
            # then that symbol is used. Otherwise, show the symbol of the direction the policy predicts
            if self.get_grid_field(x, y).has_symbol:
                field_string += self.get_grid_field(x, y).symbol
            else:
                field_string += DIRECTION_SYMBOLS[self.get_policy_field(x, y)]
            field_string += " "
        return field_string

    def print_policy(self):
        """
        Prints the policy in a nice human-readable way
        """
        print(self.get_policy_str())

    def get_grid_str(self):
        """
        :return: readable String of the grid.
        """
        out = ""
        for line in self._grid:
            for field in line:
                out += f' {str(field)} '
            out += "\n"
        return out

    def print_grid(self):
        print(self.get_grid_str())