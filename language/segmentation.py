from ..utilities.comparable_partial import partial

import numpy as np

from .grid import Grid
from .argument import extract_scalar, ArgumentError

# unused
def extract_rectangle(grid, origin, shape):
    return grid[origin[0] : shape[0] - origin[0], origin[1] : shape[1] - origin[1]]


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


def _extract_islands(grid, water):
    unassigned = {index for index, value in grid.enumerate() if value != water}

    def discover_island_bounds(index):
        top, left = index
        bottom, right = index[0] + 1, index[1] + 1

        for neighbor in _neighbors(index):
            if neighbor in unassigned:
                unassigned.remove(neighbor)
                top_, bottom_, left_, right_ = discover_island_bounds(neighbor)
                top = min(top, top_)
                bottom = max(bottom, bottom_)
                left = min(left, left_)
                right = max(right, right_)

        return top, bottom, left, right

    islands = []
    while len(unassigned) > 0:
        top, bottom, left, right = discover_island_bounds(unassigned.pop())
        island = grid[top:bottom, left:right]
        islands.append(island)

    return islands


def extract_islands(args, water=0):
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return None

    return _extract_islands(grid, water)


def _parameterize_extract_islands(args):
    """partially apply extract_islands with sensible parameter combinations"""
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return []

    return [partial(extract_islands, water=color) for color in grid.used_colors()]


extract_islands.parameterize = _parameterize_extract_islands
