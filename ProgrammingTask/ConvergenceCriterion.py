from abc import ABC, abstractmethod
import numpy as np

class ConvergenceCriterion(ABC):

    @abstractmethod
    def is_converged(self, old, new):
        pass

    @abstractmethod
    def increase(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @property
    def iterations(self):
        return self._iterations

class ConvergenceCriterionEvaluation(ConvergenceCriterion):
    pass

class ConvergenceCriterionEvaluationMaxIterationSteps(ConvergenceCriterionEvaluation):

    def __init__(self, maxIterations):
        self._maxIterations = maxIterations
        self._iterations = 0

    def reset(self):
        self._iterations = 0

    def increase(self):
        self._iterations += 1

    def is_converged(self, oldPolicyEvaluationGrid, newPolicyEvaluationGrid):
        return self._iterations >= self._maxIterations

class ConvergenceCriterionEvaluationEpsilon(ConvergenceCriterionEvaluation):

    def __init__(self, epsilon_change):
        self._epsilon_delta = epsilon_change
        self._iterations = 0

    def increase(self):
        self._iterations += 1

    def reset(self):
        self._iterations = 0

    def is_converged(self, oldPolicyEvaluationGrid, newPolicyEvaluationGrid):
        policyEvaluationGridDelta = np.abs(oldPolicyEvaluationGrid.get_grid() - newPolicyEvaluationGrid.get_grid())
        sumDelta = np.sum(policyEvaluationGridDelta)
        return sumDelta <= self._epsilon_delta

class ConvergenceCriterionImprovement(ConvergenceCriterion):
    pass

class ConvergenceCriterionImprovementMaxSteps(ConvergenceCriterionImprovement):
    def __init__(self, maxIterations):
        self._maxIterations = maxIterations
        self._iterations = 0

    def reset(self):
        self._iterations = 0

    def increase(self):
        self._iterations += 1

    def is_converged(self, oldPolicyEvaluationGrid, newPolicyEvaluationGrid):
        return self._iterations >= self._maxIterations

class ConvergenceCriterionImprovementEpsilon(ConvergenceCriterionImprovement):
    def __init__(self, epsilon_change = 0):
        self._epsilon_delta = epsilon_change
        self._iterations = 0

    def increase(self):
        self._iterations += 1

    def reset(self):
        self._iterations = 0

    def is_converged(self, oldPolicyGrid, newPolicyGrid):
        policyEvaluationGridDelta = np.abs(oldPolicyGrid.get_grid() - newPolicyGrid.get_grid())
        sumDelta = np.sum(policyEvaluationGridDelta)
        return sumDelta <= self._epsilon_delta