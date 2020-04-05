import numpy as np

from .arguments import *


def flip_up_down(grid):
    return Grid(np.flipud(grid.state))


def flip_left_right(grid):
    return Grid(np.fliplr(grid.state))


def rotate(grid, num_times):
    return Grid(np.rot90(grid.state, k=num_times))
