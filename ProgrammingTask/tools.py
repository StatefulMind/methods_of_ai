from itertools import product

def iter2d(shape):
    x = shape[0]
    y = shape[1]
    return product(range(0, x), range(0, y))

def isOutOfBoundaries(x, y, shape):
    return x < 0 or y < 0 or x >= shape[0] or y >= shape[1]