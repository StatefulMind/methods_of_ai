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

convergence_criterion = ConvergenceCriterionEvaluationMaxIterationSteps(maxIterations=100)
#convergence_criterion = ConvergenceCriterionEvaluationEpsilon(epsilon_change=0.00001)
policyEvaluationGrid = pi.performPolicyIteration(new_grid, new_policy, 1, 0.04, convergence_criterion)
print(policyEvaluationGrid)

iterations = 0
while True:
    convergence_criterion.reset()
    new_evaluation_grid = pi.performPolicyIteration(fieldGrid=new_grid, policyGrid=new_policy,discount = 1, step_cost = 0.04, convergence_criterion = convergence_criterion)
    improved = pe.improve_policy_step(new_grid, new_policy, new_evaluation_grid, step_cost=0.04)
    print(improved)
    new_policy = improved
    iterations += 1
    if iterations >= 100:
        break
