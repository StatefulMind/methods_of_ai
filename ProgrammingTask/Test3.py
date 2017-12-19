from Grid import *
from GridReader import parse_to_matrix
import PolicyIterator as pi
from ConvergenceCriterion import *
import PolicyEvaluator as pe


matrix = parse_to_matrix("grids/3by4.grid")

new_grid = FieldGrid(matrix)
print(new_grid)

new_policy = PolicyGrid((3, 4))
print(new_policy)

convergence_criterion = ConvergenceCriterionMaxIterationSteps(maxIterations=100)
#convergence_criterion = ConvergenceCriterionEpsilon(epsilon_change=0.0001)
policyEvaluationGrid = pi.performPolicyIteration(new_grid, new_policy, 1, 0.04, convergence_criterion)
print(policyEvaluationGrid)

while True:
    improved = pe.improve_policy(new_grid, new_policy, policyEvaluationGrid, 0.04)
    print(improved)
    new_policy = improved