#!/usr/bin/env python3
# author: rimichael
# last_changed: 08-01-18
import argparse

parser = argparse.ArgumentParser(description='''Read grid-file from stdin,
parse and print grid file accordingly.''')
parser.add_argument('gridfile', help='path to input .grid file')
args=parser.parse_args()

def read_grid(path_to_grid):
    '''gets grid from input and returns grid_world to output'''
    grid_dict = {}
    with open(path_to_grid, 'r') as grid_file:
        # read file line by line and enumerate accordingly
        for num, line in enumerate(grid_file.readlines()):
            #write lines to dictionary and remove \n newline 
            grid_dict['{}_line'.format(num)]=line.strip()
    return grid_dict

def print_grid(grid_dict):
    '''prints grid from grid_array'''
    for line in sorted(grid_dict):
        print(grid_dict.get(line))

def main():
    grid = read_grid(args.gridfile)
    print_grid(grid)
        
if __name__ == '__main__':
    main()
