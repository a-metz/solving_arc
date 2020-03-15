from ..utilities.hashable_partial import partial

import numpy as np

from .grid import Grid
from .argument import extract_scalar, ArgumentError


def extract_islands(args, water=0):
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return None

    return _extract_islands(grid, water)


def _extract_islands(grid, water):
    unassigned = {index for index, value in grid.enumerate() if value != water}

    islands = []
    while len(unassigned) > 0:
        top, bottom, left, right, unassigned = _neighbor_bounds(unassigned.pop(), unassigned)
        island = grid[top:bottom, left:right]
        islands.append(island)

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


def _parameterize_extract_islands(args):
    """partially apply extract_islands with sensible parameter combinations"""
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return []

    return [partial(extract_islands, water=color) for color in grid.used_colors()]


extract_islands.parameterize = _parameterize_extract_islands
