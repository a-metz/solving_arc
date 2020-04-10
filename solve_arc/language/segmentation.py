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
