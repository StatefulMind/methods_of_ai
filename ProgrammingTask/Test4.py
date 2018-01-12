from Grid import *
from GridReader import parse_to_matrix
import PolicyIterator as pi
from ConvergenceCriterion import *
import PolicyEvaluator as pe


matrix = parse_to_matrix("grids/3by4.grid")

new_grid = FieldGrid(matrix)
print(new_grid)

evaluation_convergence_criterion = ConvergenceCriterionEvaluationMaxIterationSteps(maxIterations=500)
improvement_convergence_criterion = ConvergenceCriterionImprovementEpsilon(epsilon_change=1)
improvement_convergence_criterion = ConvergenceCriterionImprovementMaxSteps(maxIterations=100)
optimal_policy = pe.policy_optimizer(new_grid, discount=1, step_cost=0.04, evaluation_convergence_criterion=evaluation_convergence_criterion, improvement_convergence_criterion= improvement_convergence_criterion)

print(optimal_policy)
optimal_policy.print()