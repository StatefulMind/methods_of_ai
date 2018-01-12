from Grid import *
import PolicyIterator as pi
from ConvergenceCriterion import *

def evaluate_policy(policyEvaluationGrid):
    policyGrid = PolicyGrid(policyEvaluationGrid.shape)

    # Retrieves the dimension=direction for which the future reward is maximal
    new_grid = np.argmax(policyEvaluationGrid, axis = 2)
    policyGrid.set_policy(new_grid)


    return policyGrid

def policy_optimizer(fieldGrid, discount, step_cost, evaluation_convergence_criterion, improvement_convergence_criterion = None):
        shape = fieldGrid.shape

        if improvement_convergence_criterion is None:
            improvement_convergence_criterion = ConvergenceCriterionImprovementEpsilon(epsilon_change=0)

        old_policy_grid = PolicyGrid(shape)


        while True:
            evaluation_convergence_criterion.reset()
            policyIterationGrid = pi.performPolicyIteration(fieldGrid=fieldGrid, policyGrid=old_policy_grid, discount=discount, step_cost=step_cost, convergence_criterion=evaluation_convergence_criterion)
            new_policy_grid = improve_policy_step(fieldGrid= fieldGrid, policyGrid=old_policy_grid, policyEvaluationGrid=policyIterationGrid, step_cost=step_cost)

            improvement_convergence_criterion.increase()
            if improvement_convergence_criterion.is_converged(old_policy_grid, new_policy_grid):
                break
        optimal_policy = new_policy_grid
        print(f"Got a policy which we hope is optimal after {improvement_convergence_criterion.iterations} steps")
        return optimal_policy

def improve_policy_step(fieldGrid, policyGrid, policyEvaluationGrid, step_cost):
    """Improving a policy by replacing every action of the policy by a greedy action"""
    shape = fieldGrid.shape
    direction_policy_grids = []
    evaluated_direction_policy_grids = []
    for direction in DIRECTIONS:
        d_policy = PolicyGrid(shape, direction * np.ones(shape))
        direction_policy_grids.append(d_policy)
    for direction in DIRECTIONS:
        e_policy = pi.policyIterationStep(fieldGrid, direction_policy_grids[direction], policyEvaluationGrid, 1, step_cost)
        evaluated_direction_policy_grids.append(e_policy.get_grid())
    new_grid = np.argmax(evaluated_direction_policy_grids, axis = 0)
    improvedPolicyGrid = PolicyGrid(policyEvaluationGrid.shape)
    improvedPolicyGrid.set_policy(new_grid)
    return improvedPolicyGrid