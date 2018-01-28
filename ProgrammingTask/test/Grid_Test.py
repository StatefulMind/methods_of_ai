import argparse
import pytest

# instantiate parser
parser = argparse.ArgumentParser(description='''Read grid-file from stdin,
parse and print grid file accordingly.''')
parser.add_argument('grid_file', help='path to input .grid file')
# parser.add_argument('-i', '--iter', type='int',
#                   help='how many iterations are performed by the policy iteration', )
args = parser.parse_args()

def test_grid_create():
    pass

def test_grid_shape():
    pass

def test_grid_values():
    pass

def test_grid_print():
    pass


def main():
    # those would be test cases - ToDo put into pytest under ./test when done
    grid = Grid(grid_file=args.grid_file)
    print(grid)
    print('Get field at [0,0]... {}'.format(grid.get_grid_field(0, 0)))
    print('Get field at [1,1]... {}'.format(grid.get_grid_field(1, 1)))
    grid.set_grid_field(1, 1, "P")
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