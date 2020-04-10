import numpy as np

from . import *


def extract_color_patches(grid, ignore=0):
    patches = []
    for color in grid.used_colors():
        if color != ignore:
            patch = extract_color_patch(grid, color)
            if patch is not None:
                patches.append(patch)

    if len(patches) == 1:
        return patches[0]

    if len(patches) == 0:
        return None

    return Grids(patches)


def extract_color_patch(grid, color):
    selection = select_color(grid, color)
    return extract_selected_area(grid, selection)


def extract_islands(grid, ignore=0):
    selection = select_all_colors(grid, ignore)
    if not selection.any():
        return None

    selection_islands = split_selection_into_connected_areas(selection)

    # if no selection islands extract single selection
    if selection_islands is None:
        selection_islands = [selection]

    islands = []
    for selection in selection_islands:
        island = extract_selected_area(grid, selection)
        if island is not None:
            islands.append(island)

    if len(islands) == 1:
        return islands[0]

    if len(islands) == 0:
        return None

    return Grids(islands)
