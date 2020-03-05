import numpy as np

from .grid import Grid


def extract_rectangle(grid, origin, shape):
    return grid[origin[0] : shape[0] - origin[0], origin[1] : shape[1] - origin[1]]
