from collections import deque
from functools import reduce

import numpy as np

from .grid import Grid, Selection


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
    selection = select_color(grid, color)
    return extract_selected_area(grid, selection)


def select_color(grid, color):
    """get selection for a single color"""
    return Selection(grid.state == color)


def select_all_colors(grid, ignore=0):
    """get selection for all colors except ignore"""
    return Selection(grid.state != ignore)


def extract_selected_areas(grid, selections):
    return tuple(extract_selected_area(grid, selection) for selection in selections)


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


# to be removed when using a DAG approach
def extract_islands(grid, ignore=0):
    selection = select_all_colors(grid, ignore)
    if not selection.any():
        return None

    selection_islands = split_selection_into_connected_areas(selection)

    # if no selection return
    if selection_islands is None:
        selection_islands = [selection]

    islands = []
    for selection in selection_islands:
        island = extract_selected_area(grid, selection)
        if island is not None:
            islands.append(island)

    if len(islands) == 1:
        return islands[0]

    return tuple(islands)


def split_selection_into_connected_areas(selection):
    return _split_selection_into_connected_areas(selection, _get_neighbors)


def split_selection_into_connected_areas_no_diagonals(selection):
    return _split_selection_into_connected_areas(selection, _get_neighbors_no_diag)


def _split_selection_into_connected_areas(selection, get_neighbors):
    unassigned = {tuple(index) for index in np.argwhere(selection.state)}

    areas = []
    while len(unassigned) > 0:
        connected, unassigned = _connected_indices(unassigned.pop(), unassigned, get_neighbors)
        area = Selection.from_indices(selection.shape, list(connected))
        areas.append(area)

    # only a single area means this was a pointless operation, just use original selection instead
    if len(areas) <= 1:
        return None

    return tuple(areas)


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


def filter_selections_touching_edge(selections):
    return tuple(selection for selection in selections if _is_selection_touching_edge(selection))


def filter_selections_not_touching_edge(selections):
    return tuple(
        selection for selection in selections if not _is_selection_touching_edge(selection)
    )


def _is_selection_touching_edge(selection):
    indices = np.argwhere(selection.state)
    return np.any(indices == 0) or np.any(indices == np.array(selection.shape) - 1)


# TODO: move to logical functions?
def merge_selections(selections):
    return Selection(reduce(np.logical_or, (selection.state for selection in selections)))
