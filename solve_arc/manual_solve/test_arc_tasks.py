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
    areas = filter_selections_not_touching_edge(areas)
    selection = merge_selections(areas)
    result = set_selected_to_color(input_, selection, color=4)
    assert result == expected


def test_0520fde7(input_, expected):
    islands = extract_islands(input_, ignore=5)
    merged = elementwise_equal_and(*islands)
    result = switch_color(merged, 1, 2)
    assert result == expected


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
    # extrude stepwise first in direction
    # get directional relation second to first
    # extrude stepwise second in direction
    # ...


def test_0b148d64(input_, expected):
    return
    # selections = select_each_color
    # result = filter_selections_touching_edge(selections)
    # result = extract_selected_areas(areas)


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


def test_10fcaaa3(input_, expected):
    return
    # (duplicate)
    # concatenate horizontal
    # (duplicate)
    # concatenate vertical
    # selection = select_all_colors(result, ignore=0)
    # select in direction all diagonals
    # result = set_selected_to_color(result, selection, color=light_blue)


def test_11852cab(input_, expected):
    return
    selection = select_all_colors(input_, ignore=0)
    # extrude rotate num_times=1 in selection bounds
    # extrude rotate num_times=1 in selection bounds
    # extrude rotate num_times=1 in selection bounds


def test_178fcbfb(input_, expected):
    return
    # selection2 = select_color(input_, color=2)
    # extrude selected stepwise to top
    # extrude selected stepwise to bottom
    # selection1 = select_color(input_, color=1)
    # selection3 = select_color(input_, color=3)
    # selection = selection_logical_or(selection1, selection3)
    # extrude selected stepwise to left
    # extrude selected stepwise to right


def test_1b2d62fb(input_, expected):
    islands = extract_islands(input_, ignore=1)
    merged = elementwise_equal_or(*islands)
    result = switch_color(merged, 0, 9)
    result = switch_color(result, 8, 9)
    assert result == expected


def test_1c786137(input_, expected):
    return
    # select_each_color
    # sort by bounds size
    # get first (smallest)
    # extract selected area
    # select_each_color
    # areas = filter_selections_touching_edge(areas)
    # selection = selection_logical_or(areas)
    # extract selected area


def test_1cf80156(input_, expected):
    islands = extract_islands(input_, ignore=0)
    result = take_first(islands)
    assert result == expected


def test_1e0a9b12(input_, expected):
    return
    # select_each_color
    # split_selection_into_connected_areas_no_diagonals / single cells
    # move all stepwise in direction bottom


def test_1f85a75f(input_, expected):
    return
    # select_each_color
    # areas = filter_selections_touching_edge(areas)
    # result = extract_selected_areas(areas)


def test_2013d3e2(input_, expected):
    return
    # selection = select_all_colors(input_)
    # extract selected area
    # split halfs horizontal
    # take first
    # split halfs vertical
    # take first


def test_23b5c85d(input_, expected):
    return
    # select_each_color
    # sort by bounds size
    # get first (smallest)
    # extract_selected_area


def test_25ff71a9(input_, expected):
    return
    selection = select_all_colors(input_)
    # move one step in direction bottom


def test_28bf18c6(input_, expected):
    return
    selection = selection_all_colors(input_)
    # extract_selected_area
    # (duplicate)
    # concatenate horizontal


def test_2dee498d(input_, expected):
    return
    # split thirds horizontal
    # take first


def test_31d5ba1a(input_, expected):
    return
    selection = select_all_colors(input_)
    # areas = split_selection_into_color_areas(grid, selection)
    areas = extract_selected_areas(areas)
    selection = selection_logical_xor(areas)
    result = colorize_selection(selection, color)


def test_32597951(input_, expected):
    selection = select_color(input_, color=8)
    bounds = extend_selection_to_bounds(selection)
    result = map_color_in_selection(input_, bounds, 1, 3)
    assert result == expected


def test_3428a4f5(input_, expected):
    islands = extract_islands(input_, ignore=4)
    merged = elementwise_xor(*islands)
    result = switch_color(merged, 2, 3)
    assert result == expected


def test_36fdfd69(input_, expected):
    return
    selection = select_color(input_, color=1)
    # fill_selection_bounds
    # select all colors in selection (ignore=2)
    # set_selected_to_color


def test_3906de3d(input_, expected):
    return
    # select_each_color
    # split selections into single cells
    # move all stepwise in direction top


def test_39a8645d(input_, expected):
    return
    # select_each_color
    # split_selections_into_connected_areas
    # sort by commonness
    # take first
    # extract selected


def test_3af2c5a8(input_, expected):
    flipped = flip_left_right(input_)
    result = concatenate_left_right(input_, flipped)
    flipped = flip_up_down(result)
    result = concatenate_top_bottom(result, flipped)
    assert result == expected


def test_4c4377d9(input_, expected):
    return
    # (duplicate)
    # concatenate vertical


def test_50cb2852(input_, expected):
    return
    # select_all_colors(result, ignore=0)
    # shrink selection


def test_5117e062(input_, expected):
    return
    # select_all_colors(result, ignore=0)
    # filter_selections_not_containing_color


def test_54d9e175(input_, expected):
    return
    # selection = select_all_colors(result, ignore=5)
    # areas = split_selection_into_connected_areas_no_diagonals(selection)
    # islands = extract_selected_areas()
    # color = get_most_common_color
    # fill_color(color)


def test_5521c0d9(input_, expected):
    return
    # selection = select_all_colors(result, ignore=0)
    # move all stepwise in direction bottom


def test_5614dbcf(input_, expected):
    return
    # selection = select_all_colors(result, ignore=5)
    # areas = split_selection_into_color_areas(grid, selection)
    # islands = extract_selected_areas(areas)
    # color = get_most_common_color
    # fill_color(color)


def test_5bd6f4ac(input_, expected):
    splits = split_left_middle_right(input_)
    right_most = take_last(splits)
    splits = split_top_middle_bottom(right_most)
    result = take_first(splits)
    assert result == expected


def test_60b61512(input_, expected):
    return
    selection = select_all_colors(input_, ignore=0)
    areas = split_selection_into_connected_areas(selection)
    # fill_selection_bounds
    # select color in selection
    # set_selected_to_color(color=7)


def test_62c24649(input_, expected):
    flipped = flip_left_right(input_)
    result = concatenate_left_right(input_, flipped)
    flipped = flip_up_down(result)
    result = concatenate_top_bottom(result, flipped)
    assert result == expected


def test_8d5021e8(input_, expected):
    return
    flipped = flip_left_right(input_)
    row = concatenate_left_right(flipped, input_)
    result = concatenate_top_bottom(result, row)
    result = concatenate_top_bottom(result, row)


def test_a740d043(input_, expected):
    return


def test_f25ffba3(input_, expected):
    splits = split_top_bottom(input_)
    bottom = take_last(splits)
    top = flip_up_down(bottom)
    result = concatenate_top_bottom(top, bottom)
    assert result == expected


def test_f2829549(input_, expected):
    mapped = map_color(input_, 0, 3)
    mapped = map_color(mapped, 7, 0)
    mapped = map_color(mapped, 5, 0)
    islands = extract_islands(mapped, ignore=1)
    result = elementwise_equal_and(*islands)
    assert result == expected


# general missing concepts
# * color as non-constant argument
# * counts as pixels (e.g. progressbar)
# * color depending on condition
# * remembered positions
# * scale invariance (pixels double sized)
# * horizontal / vertial coordinate as argument
# * associate shape
# * complex / intricate shapes vs simple shapes
# * natural pattern continuation
