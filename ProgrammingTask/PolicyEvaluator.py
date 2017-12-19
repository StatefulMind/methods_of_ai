from Grid import *
import PolicyIterator as pi
from scipy.ndimage.filters import maximum_filter

def evaluate_policy(policyEvaluationGrid):
    policyGrid = PolicyGrid(policyEvaluationGrid.shape)

    # Retrieves the dimension=direction for which the future reward is maximal
    new_grid = np.argmax(policyEvaluationGrid, axis = 2)
    policyGrid.set_policy(new_grid)


    return policyGrid

def improve_policy(fieldGrid, policyGrid, policyEvaluationGrid, step_cost):
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