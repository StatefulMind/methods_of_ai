from Grid import *
from GridReader import parse_to_matrix
import PolicyIterator as pi


def policyIterationTest(fieldGrid, policyGrid):
    oldPolicyEvaluationGrid = PolicyEvaluationGrid(fieldGrid.shape)
    return pi.policyIterationStep(fieldGrid, policyGrid, oldPolicyEvaluationGrid, discount = 1, step_cost = 0.4)


matrix = parse_to_matrix("grids/3by4.grid")

new_grid = FieldGrid(matrix)
print(new_grid)

new_policy = PolicyGrid((3, 4))
optimal_policy = PolicyGrid((3, 4))
optimal_policy.set_policy(np.array([[RIGHT, RIGHT, RIGHT, NOMOVE], [UP, NOMOVE, UP, NOMOVE], [UP, LEFT, LEFT, LEFT]]))
print(optimal_policy)

new_evaluation_grid = PolicyEvaluationGrid((3, 4))

first = pi.policyIterationStep(new_grid, optimal_policy, new_evaluation_grid, discount = 1, step_cost = 0.04)
print(first)
second = pi.policyIterationStep(new_grid, optimal_policy, first, discount = 1, step_cost = 0.04)
print(second)


print()
