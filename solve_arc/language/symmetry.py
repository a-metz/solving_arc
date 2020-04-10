import numpy as np

from .arguments import *


def flip_up_down(grid):
    return Grid(np.flipud(grid.state))


def flip_left_right(grid):
    return Grid(np.fliplr(grid.state))


def rotate_90(grid):
    return Grid(np.rot90(grid.state, k=1))


def rotate_180(grid):
    return Grid(np.rot90(grid.state, k=2))


def rotate_270(grid):
    return Grid(np.rot90(grid.state, k=3))
