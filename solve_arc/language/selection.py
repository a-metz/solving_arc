from collections import deque
from functools import reduce

import numpy as np

from .arguments import *


def select_color(grid, color):
    """get selection for a single color"""
    return Selection(grid.state == color)


def select_all_colors(grid, ignore=0):
    """get selection for all colors except ignore"""
    return Selection(grid.state != ignore)


def split_selection_into_connected_areas(selection):
    return _split_selection_into_connected_areas(selection, _get_neighbors)


def split_selection_into_connected_areas_no_diagonals(selection):
    return _split_selection_into_connected_areas(selection, _get_neighbors_no_diag)


def split_selection_into_connected_areas_skip_gaps(selection):
    return _split_selection_into_connected_areas(selection, _get_neighbors_skip_gaps)


def _split_selection_into_connected_areas(selection, get_neighbors):
    unassigned = {tuple(index) for index in np.argwhere(selection.state)}

    areas = []
    while len(unassigned) > 0:
        connected, unassigned = _connected_indices(
            unassigned.pop(), unassigned, get_neighbors
        )
        area = Selection.from_indices(selection.shape, list(connected))
        areas.append(area)

    # only a single area means this was a pointless operation, just use original selection instead
    if len(areas) <= 1:
        return None

    return Selections(areas)


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


def _get_neighbors_skip_gaps(index):
    y, x = index
    # slower and just as readable: set(product(range(y - 2, y + 3), range(x - 2, x + 3))) - {(y, x)}
    return {
        (y - 2, x - 2),
        (y - 2, x - 1),
        (y - 2, x),
        (y - 2, x + 1),
        (y - 2, x + 2),
        (y - 1, x - 2),
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
        (y - 1, x + 2),
        (y, x - 2),
        (y, x - 1),
        (y, x + 1),
        (y, x + 2),
        (y + 1, x - 2),
        (y + 1, x - 1),
        (y + 1, x),
        (y + 1, x + 1),
        (y + 1, x + 2),
        (y + 2, x - 2),
        (y + 2, x - 1),
        (y + 2, x),
        (y + 2, x + 1),
        (y + 2, x + 2),
    }


def extend_selections_to_bounds(selections):
    return selections.apply(extend_selection_to_bounds)


def extend_selection_to_bounds(selection):
    indices = np.argwhere(selection.state)

    if len(indices) == 0:
        return None

    top, left = np.min(indices, axis=0)
    bottom, right = np.max(indices, axis=0) + 1
    extended = selection.copy()
    extended.state[top:bottom, left:right] = True
    return extended


def filter_selections_touching_edge(selections):
    selections = Selections(
        selection for selection in selections if _is_selection_touching_edge(selection)
    )

    if len(selections) == 0:
        return None

    return selections


def filter_selections_not_touching_edge(selections):
    selections = Selections(
        selection
        for selection in selections
        if not _is_selection_touching_edge(selection)
    )

    if len(selections) == 0:
        return None

    return selections


def _is_selection_touching_edge(selection):
    indices = np.argwhere(selection.state)
    return np.any(indices == 0) or np.any(indices == np.array(selection.shape) - 1)


# TODO: move to logical functions?
def merge_selections(selections):
    if selections.shape == None:
        return None

    return Selection(
        reduce(np.logical_or, (selection.state for selection in selections))
    )
