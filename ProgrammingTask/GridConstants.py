GOAL = "E"
PENALTY = "P"
FIELD = "F"
WALL = "O"

TYPES = [GOAL, PENALTY, FIELD, WALL]


NOMOVE = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

DIRECTIONS = [NOMOVE, UP, RIGHT, DOWN, LEFT]

NOMOVE_D = (0, 0)
UP_D = (-1, 0)
RIGHT_D = (0, 1)
DOWN_D = (1, 0)
LEFT_D = (0, -1)

DIRECTIONS_D = {NOMOVE: NOMOVE_D, UP: UP_D, RIGHT: RIGHT_D, DOWN: DOWN_D, LEFT: LEFT_D}