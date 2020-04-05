from collections import deque
from functools import reduce

import numpy as np

from .grid import Grid, Mask


# to be removed when using a DAG approach
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

    return tuple(patches)


# to be removed when using a DAG approach
def extract_color_patch(grid, color):
    mask = mask_for_color(grid, color)
    return extract_masked_area(grid, mask)


def mask_for_color(grid, color):
    """get mask for a single color"""
    return Mask(grid.state == color)


def mask_for_all_colors(grid, ignore=0):
    """get mask for all colors except ignore"""
    return Mask(grid.state != ignore)


def extract_masked_areas(grid, masks):
    return tuple(extract_masked_area(grid, mask) for mask in masks)


def extract_masked_area(grid, mask):
    """extract box bounding mask from grid"""
    indices = np.argwhere(mask.state)
    top, left = np.min(indices, axis=0)
    bottom, right = np.max(indices, axis=0) + 1
    patch = grid[top:bottom, left:right]

    if patch.shape == grid.shape:
        # was a pointless operation, just use original grid instead
        return None

    return patch


# to be removed when using a DAG approach
def extract_islands(grid, ignore=0):
    mask = mask_for_all_colors(grid, ignore)
    if not mask.any():
        return None

    mask_islands = split_mask_into_connected_areas(mask)

    # if no mask return
    if mask_islands is None:
        mask_islands = [mask]

    islands = []
    for mask in mask_islands:
        island = extract_masked_area(grid, mask)
        if island is not None:
            islands.append(island)

    if len(islands) == 1:
        return islands[0]

    return tuple(islands)


def split_mask_into_connected_areas(mask):
    return _split_mask_into_connected_areas(mask, _get_neighbors)


def split_mask_into_connected_areas_no_diagonals(mask):
    return _split_mask_into_connected_areas(mask, _get_neighbors_no_diag)


def _split_mask_into_connected_areas(mask, get_neighbors):
    unassigned = {tuple(index) for index in np.argwhere(mask.state)}

    islands = []
    while len(unassigned) > 0:
        connected, unassigned = _connected_indices(unassigned.pop(), unassigned, get_neighbors)
        island = Mask.from_indices(mask.shape, list(connected))
        islands.append(island)

    # only a single island means this was a pointless operation, just use original mask instead
    if len(islands) <= 1:
        return None

    return tuple(islands)


def _connected_indices(start, candidates, get_neighbors):
    connected = set()
    queue = deque([start])

    while len(queue) > 0:
        index = queue.popleft()
        connected.add(index)
        neighbors = get_neighbors(index) & candidates
        candidates -= neighbors
        queue.extend(neighbors)

    connected |= set(queue)
    return connected, candidates


def _get_neighbors(index):
    y, x = index
    return {
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
        (y, x - 1),
        (y, x + 1),
        (y + 1, x - 1),
        (y + 1, x),
        (y + 1, x + 1),
    }


def _get_neighbors_no_diag(index):
    y, x = index
    return {
        (y - 1, x),
        (y + 1, x),
        (y, x - 1),
        (y, x + 1),
    }


def filter_masks_touching_edge(masks):
    return tuple(mask for mask in masks if _is_mask_touching_edge(mask))


def filter_masks_not_touching_edge(masks):
    return tuple(mask for mask in masks if not _is_mask_touching_edge(mask))


def _is_mask_touching_edge(mask):
    indices = np.argwhere(mask.state)
    return np.any(indices == 0) or np.any(indices == np.array(mask.shape) - 1)


# TODO: move to logical functions?
def merge_masks(masks):
    return Mask(reduce(np.logical_or, (mask.state for mask in masks)))
