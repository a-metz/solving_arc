import numpy as np

from .arguments import *


def extract_selected_areas(grid, selections):
    return Grids(extract_selected_area(grid, selection) for selection in selections)


def extract_selected_area(grid, selection):
    """extract box bounding selection from grid"""
    if not selection.any():
        return None

    indices = np.argwhere(selection.state)

    top, left = np.min(indices, axis=0)
    bottom, right = np.max(indices, axis=0) + 1
    patch = grid[top:bottom, left:right]

    if patch.shape == grid.shape:
        # was a pointless operation, just use original grid instead
        return None

    return patch


def split_left_right(grid):
    return Grids(Grid(split) for split in np.hsplit(grid.state, 2))


def split_left_middle_right(grid):
    return Grids(Grid(split) for split in np.hsplit(grid.state, 3))


def split_top_bottom(grid):
    return Grids(Grid(split) for split in np.vsplit(grid.state, 2))


def split_top_middle_bottom(grid):
    return Grids(Grid(split) for split in np.vsplit(grid.state, 3))


def concatenate_left_right(a, b):
    return Grid(np.hstack([a.state, b.state]))


def concatenate_top_bottom(a, b):
    return Grid(np.vstack([a.state, b.state]))


def concatenate_left_to_right(grids):
    return Grid(np.hstack([grid.state for grid in grids]))


def concatenate_top_to_bottom(grids):
    return Grid(np.vstack([grid.state for grid in grids]))


def take_first(sequence):
    if len(sequence) == 0:
        return None

    return sequence[0]


def take_last(sequence):
    if len(sequence) < 2:
        return None

    return sequence[-1]
