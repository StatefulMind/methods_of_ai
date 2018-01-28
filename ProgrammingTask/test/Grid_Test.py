import pytest
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Grid import Grid
from GridField import GridField
from GridField import GridFieldField
from GridField import GridFieldPenalty

# we are in the root dir due to path.append...
grid_path = './grids/3by4.grid'
grid = Grid(grid_path)

def test_grid_create():
    assert grid is not None
    assert isinstance(grid, Grid)

    comp_array = []
    with open(grid_path) as read_file:
        for line in read_file.readlines():
            values = line.strip('\n').split()
            comp_array.append(values)
    assert grid._array == comp_array

def test_grid_shape():
    assert grid.shape == [3,4]

def test_grid_values():
    # check correct string value
    assert str(grid.get_grid_field(0,0)) == 'F'

def test_grid_field_type():
    # check correct type
    assert isinstance(grid.get_grid_field(0, 0), GridFieldField)

def test_change_grid():
    grid.set_grid_field(0,0, GridField.factory('P'))
    assert isinstance(grid.get_grid_field(0,0), GridFieldPenalty)

def test_policy_grid():
    # test random instantiation from policy grid
    # positions are encoded as int arrays
    positional_array = [0, 1, 2, 3, 4]
    assert grid.get_policy_field(0, 0) in positional_array

def test_eval_grid():
    # test zero instantiation of eval grid
    assert grid.get_eval_field(0, 0) == 0