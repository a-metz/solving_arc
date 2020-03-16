import numpy as np

from .argument import expect_scalar


@expect_scalar(on_error_return=None)
def extract_color_patches(grid, ignore=0):
    color_patches = []
    for color in grid.used_colors():
        if color != ignore:
            indices = np.argwhere(grid.state == color)
            top, left = np.min(indices, axis=0)
            bottom, right = np.max(indices, axis=0) + 1
            if (bottom - top, right, left) != grid.shape:
                color_patches.append(grid[top:bottom, left:right])
    return color_patches


@expect_scalar(on_error_return=None)
def extract_islands(grid, ignore=0):
    unassigned = {tuple(index) for index in np.argwhere(grid.state != ignore)}

    islands = []
    while len(unassigned) > 0:
        top, bottom, left, right, unassigned = _neighbor_bounds(unassigned.pop(), unassigned)
        if (bottom - top, right, left) != grid.shape:
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
