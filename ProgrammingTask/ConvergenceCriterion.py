from abc import ABC, abstractmethod
import numpy as np

class ConvergenceCriterion(ABC):

    @abstractmethod
    def is_converged(self, oldPolicyEvaluationGrid, newPolicyEvaluationGrid):
        pass

    @abstractmethod
    def increase(self):
        pass

    @abstractmethod
    def reset(self):
        pass

class ConvergenceCriterionMaxIterationSteps(ConvergenceCriterion):

    def __init__(self, maxIterations):
        self._maxIterations = maxIterations
        self._iterations = 0

    def reset(self):
        self._iterations = 0

    def increase(self):
        self._iterations += 1

    def is_converged(self, oldPolicyEvaluationGrid, newPolicyEvaluationGrid):
        return self._iterations >= self._maxIterations

class ConvergenceCriterionEpsilon(ConvergenceCriterion):

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