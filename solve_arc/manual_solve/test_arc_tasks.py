import pytest

from ..language import *

# colors
# 0: black
# 1: blue
# 2: red
# 3: green
# 4: yellow
# 5: gray
# 6: pink
# 7: orange
# 8: azure
# 9: crimson


def test_00d62c1b(input_, expected):
    selection = select_color(input_, color=0)
    areas = split_selection_into_connected_areas_no_diagonals(selection)
    areas = filter_selections_touching_edge(areas)
    selection = merge_selections(areas)
    result = set_selected_to_color(input_, selection, color=4)


def test_0520fde7(input_, expected):
    islands = extract_islands(input_, ignore=5)
    merged = elementwise_equal_and(*islands)
    result = switch_color(merged, 1, 2)
    assert result == expected


def test_05269061(input_, expected):
    return
    # get pattern for cell color to surrounding colors (underdefined)
    # fill with that pattern


def test_05f2a901(input_, expected):
    return
    # get red selection
    # get blue selection
    # get directional relation red to blue
    # move stepwise red in direction while possible


def test_08ed6ac7(input_, expected):
    return
    selection = select_all_colors(input_, ignore=0)
    areas = split_selection_into_connected_areas(grid, selection)
    # sort areas by size
    # unpack first
    # set selected color X
    # unpack second
    # set selected color Y
    # unpack third
    # set selected color Z
    # unpack fourth
    # set selected color W


def test_0a938d79(input_, expected):
    return
    selection = select_all_colors(input_, ignore=0)
    areas = split_selection_into_connected_areas(selection)
    # get directional relation first to second
    # copy stepwise first in direction
    # get directional relation second to first
    # copy stepwise second in direction
    # ...


def test_0b148d64(input_, expected):
    return
    selection = select_all_colors(input_, ignore=0)
    # areas = split_selection_into_color_areas(grid, selection)
    # result = filter_selections_touching_edge(areas)
    # alternative select by uniqueness?


def test_0ca9ddb6(input_, expected):
    return
    selection = select_color(input_, color=2)
    # select in direction all diagonals
    result = set_selected_to_color(result, selection, color=7)
    selection = select_color(input_, color=1)
    # select in direction all main directions
    result = set_selected_to_color(result, selection, color=7)


def test_0d3d703e(input_, expected):
    result = switch_color(input_, 3, 4)
    result = switch_color(result, 1, 5)
    result = switch_color(result, 2, 6)
    result = switch_color(result, 8, 9)
    assert result == expected


def test_0dfd9992(input_, expected):
    return
    # get pattern for cell color to surrounding colors (mutiple options)
    # fill with that pattern


def test_10fcaaa3(input_, expected):
    return
    # duplicate
    # concatenate horizontal
    # duplicate
    # concatenate vertical
    # selection = select_all_colors(result, ignore=0)
    # select in direction all diagonals
    # result = set_selected_to_color(result, selection, color=light_blue)


def test_11852cab(input_, expected):
    return
    selection = select_all_colors(input_, ignore=0)
    # copy rotate num_times=1 in selection bounds
    # copy rotate num_times=1 in selection bounds
    # copy rotate num_times=1 in selection bounds


# top down exploration ---
def test_178fcbfb(input_, expected):
    return


def test_1b2d62fb(input_, expected):
    islands = extract_islands(input_, ignore=1)
    merged = elementwise_equal_or(*islands)
    result = switch_color(merged, 0, 9)
    result = switch_color(result, 8, 9)
    assert result == expected


def test_1cf80156(input_, expected):
    islands = extract_islands(input_, ignore=0)
    assert islands == expected


def test_3428a4f5(input_, expected):
    islands = extract_islands(input_, ignore=4)
    merged = elementwise_xor(*islands)
    result = switch_color(merged, 2, 3)


def test_8d5021e8(input_, expected):
    return
    # extend flip_horizontal left
    # extend identity bottom
    # extend identity bottom


def test_31d5ba1a(input_, expected):
    return
    selection = select_all_colors(input_)
    # areas = split_selection_into_color_areas(grid, selection)
    areas = extract_selected_areas(areas)
    selection = selection_logical_xor(areas)
    result = colorize_selection(selection, color)
