from abc import ABC
from Constants import NOMOVE, UP, DOWN, LEFT, RIGHT

class GridField(ABC):
    """Abstract Field Class for Fields in the Grid
    defines type property
    and __str__ method
    contains factory for instantiation of fields"""

    def __init__(self, field):
        super().__init__()
        self._type = field

    def factory(field):
        if field == 'F': return GridFieldField()
        if field == 'O': return GridFieldWall()
        if field == 'E': return GridFieldGoal()
        if field == 'P': return GridFieldPenalty()
        print("Unknown type!")

    def __str__(self):
        return str(self._type)

    @property
    def type(self):
        return self._type


class GridFieldField(GridField):
    '''
    Class containing the properties of the field field in the grid
    Adds movement probabilities and movement boolean
    Inherits type and __str__ function
    '''
    FIELD = "F"

    # Represents the probabilities in which directions you might move if you perform an action
    FIELD_PROBS = {NOMOVE: {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0},
                   UP: {NOMOVE: 0, UP: 0.8, RIGHT: 0.1, DOWN: 0, LEFT: 0.1},
                   RIGHT: {NOMOVE: 0, UP: 0.1, RIGHT: 0.8, DOWN: 0.1, LEFT: 0},
                   DOWN: {NOMOVE: 0, UP: 0, RIGHT: 0.1, DOWN: 0.8, LEFT: 0.1},
                   LEFT: {NOMOVE: 0, UP: 0.1, RIGHT: 0, DOWN: 0.1, LEFT: 0.8}}

    def __init__(self, FIELD=FIELD, FIELD_PROBS=FIELD_PROBS):
        super().__init__(FIELD)
        self._FIELD_PROBS = FIELD_PROBS

    def get_movement_probs(self):
        return self._FIELD_PROBS

    @property
    def can_move_here(self):
        return True

    @property
    def has_static_evaluation_value(self):
        return False

    @property
    def has_symbol(self):
        return False


class GridFieldWall(GridField):
    '''
    Class containing properties and probabilities of the wall field
    overwrites __str__ with Wall symbol
    '''
    WALL = 'O'
    WALL_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}

    # Represents the probabilities in which directions you might move if you perform an action
    WALL_PROBS = {NOMOVE: WALL_PROB_ANY, UP: WALL_PROB_ANY, RIGHT: WALL_PROB_ANY, DOWN: WALL_PROB_ANY,
                  LEFT: WALL_PROB_ANY}

    def __init__(self, WALL=WALL, WALL_PROB_ANY=WALL_PROB_ANY, WALL_PROBS=WALL_PROBS):
        super().__init__(WALL)
        self._WALL_REWARD = 0
        self._WALL_PROB_ANY = WALL_PROB_ANY
        self._WALL_PROBS = WALL_PROBS

    def get_movement_probs(self, **kwargs):
        return self._WALL_PROBS

    @property
    def can_move_here(self):
        return False

    @property
    def has_static_evaluation_value(self):
        return True

    def get_static_evaluation_value(self):
        return self._WALL_REWARD

    @property
    def has_symbol(self):
        return True

    @property
    def symbol(self):
        return '\u220E'

    def __str__(self):
        return self.symbol


class GridFieldPenalty(GridField):
    '''
    Class containing properties for the Penalty Field
    contains movement probabilities for the penalty field
    overwrites __str__ with penalty symbol
    '''

    PENALTY = "P"
    PENALTY_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}

    # Represents the probabilities in which directions you might move if you perform an action
    PENALTY_PROBS = {NOMOVE: PENALTY_PROB_ANY, UP: PENALTY_PROB_ANY, RIGHT: PENALTY_PROB_ANY, DOWN: PENALTY_PROB_ANY,
                     LEFT: PENALTY_PROB_ANY}

    def __init__(self, PENALTY=PENALTY, PENALTY_PROBS=PENALTY_PROBS):
        super().__init__(PENALTY)
        self._PENALTY_PROBS = PENALTY_PROBS
        self._PENALTY_REWARD = -1

    def get_movement_probs(self):
        return self._PENALTY_PROBS

    @property
    def can_move_here(self):
        return True

    @property
    def has_static_evaluation_value(self):
        return True

    def get_static_evaluation_value(self):
        return self._PENALTY_REWARD

    @property
    def has_symbol(self):
        return True

    @property
    def symbol(self):
        return '\u0298'

    def __str__(self):
        return self.symbol


class GridFieldGoal(GridField):
    '''
    Class containing properties for the Goal Field
    contains movement probabilities for the goal field
    overwrites __str__ with goal symbol
    '''

    GOAL = "E"
    # if in a goal state you do not move
    GOAL_PROB_ANY = {NOMOVE: 1, UP: 0, RIGHT: 0, DOWN: 0, LEFT: 0}

    # Represents the probabilities in which directions you might move if you perform an action
    GOAL_PROBS = {NOMOVE: GOAL_PROB_ANY, UP: GOAL_PROB_ANY, RIGHT: GOAL_PROB_ANY, DOWN: GOAL_PROB_ANY,
                  LEFT: GOAL_PROB_ANY}

    def __init__(self, GOAL=GOAL, GOAL_PROBS=GOAL_PROBS):
        super().__init__(GOAL)
        self._GOAL_REWARD = 1
        self._GOAL_PROBS = GOAL_PROBS

    def get_movement_probs(self):
        return self._GOAL_PROBS

    @property
    def can_move_here(self):
        return True

    @property
    def has_static_evaluation_value(self):
        return True

    @property
    def has_symbol(self):
        return True

    def get_static_evaluation_value(self):
        return self._GOAL_REWARD

    @property
    def symbol(self):
        return '\u2302'

    def __str__(self):
        return self.symbol
