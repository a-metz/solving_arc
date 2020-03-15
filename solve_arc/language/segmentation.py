from ..utilities.hashable_partial import partial

import numpy as np

from .grid import Grid
from .argument import extract_scalar, ArgumentError


def parameterize(args):
    """partially apply segmentation with sensible parameter combinations"""
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return []

    extract_islands_functions = [
        partial(extract_islands, ignore=color) for color in grid.used_colors()
    ]

    extract_color_patches_functions = [
        partial(extract_color_patches, ignore=color) for color in grid.used_colors()
    ]

    return extract_islands_functions + extract_color_patches_functions


def extract_islands(args, ignore=0):
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return None

    return _extract_islands(grid, ignore)


def extract_color_patches(args, ignore=0):
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return None

    return _extract_color_patches(grid, ignore)


def _extract_islands(grid, ignore):
    unassigned = {tuple(index) for index in np.argwhere(grid.state != ignore)}

    islands = []
    while len(unassigned) > 0:
        top, bottom, left, right, unassigned = _neighbor_bounds(unassigned.pop(), unassigned)
        islands.append(grid[top:bottom, left:right])

    return islands


def _neighbor_bounds(start, candidates):
    top, left = start
    bottom, right = start[0] + 1, start[1] + 1

    for neighbor in _neighbors(start):
        if neighbor in candidates:
            candidates.remove(neighbor)
            top_, bottom_, left_, right_, candidates = _neighbor_bounds(neighbor, candidates)
            top = min(top, top_)
            bottom = max(bottom, bottom_)
            left = min(left, left_)
            right = max(right, right_)

    return top, bottom, left, right, candidates


def _neighbors(index):
    y, x = index
    return [
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
        (y, x - 1),
        (y, x + 1),
        (y + 1, x - 1),
        (y + 1, x),
        (y + 1, x + 1),
    ]


def _extract_color_patches(grid, ignore):
    color_patches = []
    for color in grid.used_colors():
        if color != ignore:
            indices = np.argwhere(grid.state == color)
            top, left = np.min(indices, axis=0)
            bottom, right = np.max(indices, axis=0) + 1
            color_patches.append(grid[top:bottom, left:right])
    return color_patches
