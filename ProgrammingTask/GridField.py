from GridSettings import *
from abc import ABC, abstractmethod

class GridField(ABC):
    """Abstract Field Class"""
    def __init__(self, type):
        self._type = type
        super().__init__()

    @abstractmethod
    def get_movement_probs(self, type):
        return MOVEMENT_PROBS[type]

    def factory(type):
        if type == FIELD: return GridFieldField()
        if type == WALL: return GridFieldWall()
        if type == GOAL: return GridFieldGoal()
        if type == PENALTY: return GridFieldPenalty()
        print("Unknown type!")

    def __str__(self):
        return str(self._type)

    @property
    @abstractmethod
    def canMoveHere(self):
        pass

    @property
    @abstractmethod
    def hasStaticEvaluationValue(self):
        pass

    @property
    def type(self):
        return self._type

class GridFieldField(GridField):
    def __init__(self):
        super().__init__(FIELD)

    def get_movement_probs(self):
        return super().get_movement_probs(FIELD)

    @property
    def canMoveHere(self):
        return True

    @property
    def hasStaticEvaluationValue(self):
        return False

class GridFieldWall(GridField):
    def __init__(self):
        super().__init__(WALL)

    def get_movement_probs(self):
        return super().get_movement_probs(WALL)

    @property
    def canMoveHere(self):
        return False

    @property
    def hasStaticEvaluationValue(self):
        return True

    def getStaticEvaluationValue(self):
        return WALL_REWARD


class GridFieldPenalty(GridField):
    def __init__(self):
        super().__init__(PENALTY)

    def get_movement_probs(self):
        return super().get_movement_probs(PENALTY)

    @property
    def canMoveHere(self):
        return True

    @property
    def hasStaticEvaluationValue(self):
        return True

    def getStaticEvaluationValue(self):
        return PENALTY_REWARD

class GridFieldGoal(GridField):
    def __init__(self):
        super().__init__(GOAL)

    def get_movement_probs(self):
        return super().get_movement_probs(GOAL)

    @property
    def canMoveHere(self):
        return True

    @property
    def hasStaticEvaluationValue(self):
        return True

    def getStaticEvaluationValue(self):
        return GOAL_REWARD