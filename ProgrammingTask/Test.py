from Grid import *
from GridReader import parse_to_matrix

matrix = parse_to_matrix("grids/3by4.grid")

new_grid = FieldGrid(matrix)
print(new_grid)

new_policy = PolicyGrid((3, 4))
print(new_policy)

new_evaluation_grid = PolicyEvaluationGrid((3, 4))
print(new_evaluation_grid)
