import numpy as np

from .arguments import *


def switch_color(grid, a, b):
    mapped = grid.copy()
    mapped.state[grid.state == a] = b
    mapped.state[grid.state == b] = a
    return mapped


def map_color(grid, from_, to):
    mapped = grid.copy()
    mapped.state[grid.state == from_] = to
    return mapped


def map_color_in_selection(grid, selection, from_, to):
    if grid.shape != selection.shape:
        return None

    mask = np.logical_and(selection.state, grid.state == from_)
    mapped = grid.copy()
    mapped.state[mask] = to
    return mapped


def set_selected_to_color(grid, selection, color):
    if grid.shape != selection.shape:
        return None

    changed = selection.state * color
    unchanged = grid.state * np.invert(selection.state)
    return Grid(changed + unchanged)


def fill_grid(grid, color):
    return Grid.fill(grid.shape, color)
