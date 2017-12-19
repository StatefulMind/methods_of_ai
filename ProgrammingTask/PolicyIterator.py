from tools import iter2d, isOutOfBoundaries
from GridSettings import *
from Grid import PolicyGrid, PolicyEvaluationGrid
import numpy as np

def policyIterationStep(fieldGrid, policyGrid, oldPolicyEvaluationGrid, discount, step_cost):
    shape = policyGrid.shape
    newPolicyEvaluationGrid = PolicyEvaluationGrid(shape)

    for x, y in iter2d(shape):
        oldEvaluationValue = oldPolicyEvaluationGrid.get_field(x, y)
        evaluationValueDelta = 0
        field = fieldGrid.get_field(x, y)
        if field.hasStaticEvaluationValue:
            newPolicyEvaluationGrid.set_field(x, y, field.getStaticEvaluationValue())
            continue
        policyDirection = policyGrid.get_field(x, y)
        movementProbs = field.get_movement_probs()[policyDirection]

        successorStateSum = 0
        immediateReward = -step_cost
        for movementDirection in DIRECTIONS:
            (x_mv, y_mv) = np.add((x, y), DIRECTIONS_D[movementDirection])
            #Do not evaluate the field again, even if you do not move:
            if (x_mv, y_mv) == (x, y):
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
        newPolicyEvaluationGrid.set_field(x, y, newEvaluationValue)
    return newPolicyEvaluationGrid

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
    print(f'Policy Iteration converged after {iteration} iterations')
    return newPolicyEvaluationGrid
