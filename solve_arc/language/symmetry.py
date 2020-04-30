import numpy as np

from .arguments import *
from .segmentation import extract_selected_area


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


def flip_up_down_within_bounds(grid, selection):
    return _transform_within_bounds(grid, selection, np.flipud)


def flip_left_right_within_bounds(grid, selection):
    return _transform_within_bounds(grid, selection, np.fliplr)


def rotate_90_within_bounds(grid, selection):
    return _transform_within_bounds(grid, selection, np.rot90, k=1)


def rotate_180_within_bounds(grid, selection):
    return _transform_within_bounds(grid, selection, np.rot90, k=2)


def rotate_270_within_bounds(grid, selection):
    return _transform_within_bounds(grid, selection, np.rot90, k=3)


def _transform_within_bounds(grid, selection, func, *args, **kwargs):
    if selection.shape != grid.shape:
        return None

    if not selection.any():
        return None

    indices = np.argwhere(selection.state)
    top, left = np.min(indices, axis=0)
    bottom, right = np.max(indices, axis=0) + 1
    patch = grid.state[top:bottom, left:right]

    if patch.shape == grid.shape:
        # was a pointless selection, just use original grid instead
        return None

    transformed = func(patch, *args, **kwargs)

    if transformed.shape != patch.shape:
        return None

    patched = grid.copy()
    patched.state[top:bottom, left:right] = transformed
    return patched
