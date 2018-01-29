
# We can move in the following directions
NOMOVE = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

DIRECTIONS = [NOMOVE, UP, RIGHT, DOWN, LEFT]

# Encoding (x, y) delta on the grid for every direction
NOMOVE_D = (0, 0)
UP_D = (0, -1)
RIGHT_D = (1, 0)
DOWN_D = (0, 1)
LEFT_D = (-1, 0)

DIRECTIONS_D = {NOMOVE: NOMOVE_D, UP: UP_D, RIGHT: RIGHT_D, DOWN: DOWN_D, LEFT: LEFT_D}

# use unicode arrows as directional symbols
DIRECTION_SYMBOLS = {NOMOVE: '\u220E',
                     UP: '\u2191',
                     RIGHT: '\u2192',
                     DOWN: '\u2193',
                     LEFT: '\u2190',}