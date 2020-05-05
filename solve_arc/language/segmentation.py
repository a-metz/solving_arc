import numpy as np

from .arguments import *


def extract_selected_areas(grid, selections):
    extracted_areas = []
    for selection in selections:
        extracted_area = extract_selected_area(grid, selection)
        if extracted_area is not None:
            extracted_areas.append(extracted_area)

    if len(extracted_areas) == 0:
        return None

    return Grids(extracted_areas)


def extract_selected_area(grid, selection):
    """extract box bounding selection from grid"""
    if selection.shape != grid.shape:
        return None

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


def split_left_right(grid):
    if grid.width % 2 != 0:
        return None

    return Grids(Grid(split) for split in np.hsplit(grid.state, 2))


def split_left_middle_right(grid):
    if grid.width % 3 != 0:
        return None

    return Grids(Grid(split) for split in np.hsplit(grid.state, 3))


def split_top_bottom(grid):
    if grid.height % 2 != 0:
        return None

    return Grids(Grid(split) for split in np.vsplit(grid.state, 2))


def split_top_middle_bottom(grid):
    if grid.height % 3 != 0:
        return None

    return Grids(Grid(split) for split in np.vsplit(grid.state, 3))


def concatenate_left_right(a, b):
    if a.height != b.height:
        return None

    return Grid(np.hstack([a.state, b.state]))


def concatenate_top_bottom(a, b):
    if a.width != b.width:
        return None

    return Grid(np.vstack([a.state, b.state]))


def concatenate_left_to_right(grids):
    if grids.height is None:
        return None

    return Grid(np.hstack([grid.state for grid in grids]))


def concatenate_top_to_bottom(grids):
    if grids.width is None:
        return None

    return Grid(np.vstack([grid.state for grid in grids]))


def merge_grids_with_mask(a, b, mask):
    if not (a.shape == b.shape == mask.shape):
        return None

    return Grid(np.where(mask.state, a.state, b.state))


def take_first(sequence):
    if len(sequence) == 0:
        return None

    return sequence[0]


def take_last(sequence):
    if len(sequence) < 2:
        return None

    return sequence[-1]


def sort_by_area(sequence):
    return sequence.__class__(
        sorted(sequence, key=lambda element: element.shape[0] * element.shape[1])
    )


def take_grid_with_unique_colors(grids):
    # no definition of uniqueness for less than 3 elements
    if len(grids) < 3:
        return None

    unique_colors_grids = {}
    common_colors = set()

    for grid in grids:
        used_colors = grid.used_colors()
        if used_colors in common_colors:
            continue

        if used_colors in unique_colors_grids.keys():
            del unique_colors_grids[used_colors]
            common_colors.add(used_colors)
            continue

        unique_colors_grids[used_colors] = grid

    if len(unique_colors_grids) == 1:
        return next(iter(unique_colors_grids.values()))

    return None
