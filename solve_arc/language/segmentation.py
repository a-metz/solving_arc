import numpy as np


def extract_color_patches(grid, ignore=0):
    patches = []
    for color in grid.used_colors():
        if color != ignore:
            patch = extract_color_patch(grid, color)
            if patch is not None:
                patches.append(patch)

    if len(patches) == 0:
        return None

    if len(patches) == 1:
        return patches[0]

    return patches


def extract_color_patch(grid, color):
    indices = np.argwhere(grid.state == color)
    top, left = np.min(indices, axis=0)
    bottom, right = np.max(indices, axis=0) + 1
    patch = grid[top:bottom, left:right]

    if patch.shape == grid.shape:
        return None

    return patch


def extract_islands(grid, ignore=0):
    unassigned = {tuple(index) for index in np.argwhere(grid.state != ignore)}

    islands = []
    while len(unassigned) > 0:
        top, bottom, left, right, unassigned = _neighbor_bounds(unassigned.pop(), unassigned)
        island = grid[top:bottom, left:right]
        if island.shape != grid.shape:
            islands.append(island)

    if len(islands) == 0:
        return None

    if len(islands) == 1:
        return islands[0]

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
