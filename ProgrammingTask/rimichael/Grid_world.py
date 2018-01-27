#!/usr/bin/env python3
# author: rimichael
# last_changed: 08-01-18
import argparse

parser = argparse.ArgumentParser(description='''Read grid-file from stdin,
parse and print grid file accordingly.''')
parser.add_argument('gridfile', help='path to input .grid file')
parser.add_argument('-i', '--iter', type='int',
                    help='how many iterations are performed by the policy iteration', )
args = parser.parse_args()


class Grid_world():
    def __init__(self, path_to_grid):
        self.path_to_grid = path_to_grid
        # self.grid = read_grid(path_to_grid)

    def read_grid(path_to_grid):
        '''gets grid from input and returns grid_world to output'''
        grid_dict = {}
        with open(path_to_grid, 'r') as grid_file:
            # read file line by line and enumerate accordingly
            for num, line in enumerate(grid_file.readlines()):
                # write lines to dictionary and remove \n
                grid_dict['{}_line'.format(num)] = line.strip()
                return grid_dict

    def __str__(self, grid_dict):
        '''prints grid from grid_array'''
        for line in sorted(grid_dict):
            print(grid_dict.get(line))

    def policy_iterator(iterations = 5):
        grid_values = 0
        yield grid_values



def main():
    grid = Grid_world(args.gridfile)
    grid.print_grid(grid.read_grid())


if __name__ == '__main__':
    main()
