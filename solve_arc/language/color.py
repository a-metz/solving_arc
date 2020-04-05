import numpy as np

from .grid import *


def switch_color(grid, a, b):
    mapped = grid.copy()
    mapped.state[grid.state == a] = b
    mapped.state[grid.state == b] = a
    return mapped


def map_color(grid, from_, to):
    mapped = grid.copy()
    mapped.state[mapped.state == from_] = to
    return mapped


def set_selected_to_color(grid, selection, color):
    changed = selection.state * color
    unchanged = grid.state * np.invert(selection.state)
    return Grid(changed + unchanged)
