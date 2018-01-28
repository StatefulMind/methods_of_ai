#test
import ProgrammingTask.ConvergenceCriterion as ConvergenceCriterion
from tools import iter2d, isOutOfBoundaries
import numpy as np
from ProgrammingTask.Grid import Grid

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

        old_policy_grid = Grid(shape)


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

def policyIterationStep(fieldGrid, policyGrid, oldPolicyEvaluationGrid, discount, step_cost):
    shape = policyGrid.shape
    new_policy_evaluation_grid = PolicyEvaluationGrid(shape)

    for x, y in iter2d(shape):
        oldEvaluationValue = oldPolicyEvaluationGrid.get_field(x, y)
        evaluationValueDelta = 0
        field = fieldGrid.get_field(x, y)
        if field.hasStaticEvaluationValue:
            new_policy_evaluation_grid.set_field(x, y, field.getStaticEvaluationValue())
            continue
        policy_direction = policyGrid.get_field(x, y)
        movementProbs = field.get_movement_probs()[policy_direction]

        successorStateSum = 0
        immediateReward = -step_cost
        for movementDirection in DIRECTIONS:
            (x_mv, y_mv) = np.add((x, y), DIRECTIONS_D[movementDirection])
            if (x_mv, y_mv) == (x, y):
                successorStateSum += movementProbs[movementDirection] * oldPolicyEvaluationGrid.get_field(x, y)
                continue
            if isOutOfBoundaries(x_mv, y_mv, shape):
                successorStateSum += 0
                successorStateSum += movementProbs[movementDirection] * oldPolicyEvaluationGrid.get_field(x, y)
                continue
            if not fieldGrid.get_field(x_mv, y_mv).canMoveHere:
                successorStateSum += movementProbs[movementDirection] * oldPolicyEvaluationGrid.get_field(x, y)
                continue
            successorStateSum += movementProbs[movementDirection] * oldPolicyEvaluationGrid.get_field(x_mv, y_mv)
        newEvaluationValue = immediateReward + discount * successorStateSum
        new_policy_evaluation_grid.set_field(x, y, newEvaluationValue)
    return new_policy_evaluation_grid

def performPolicyIteration(fieldGrid, policyGrid, discount, step_cost, convergence_criterion):
    shape = policyGrid.shape
    oldPolicyEvaluationGrid = PolicyEvaluationGrid(shape)
    oldPolicyEvaluationGrid.set_policy_evaluation_zero(shape)
    iteration = 1
    while True:
        iteration_discount = discount**iteration
        newPolicyEvaluationGrid = policyIterationStep(fieldGrid, policyGrid, oldPolicyEvaluationGrid, iteration_discount, step_cost)

        convergence_criterion.increase()
        if convergence_criterion.is_converged(oldPolicyEvaluationGrid, newPolicyEvaluationGrid):
            break
        oldPolicyEvaluationGrid = newPolicyEvaluationGrid
        iteration += 1
    # print(f'Policy Iteration converged after {iteration} iterations')
    return newPolicyEvaluationGrid
