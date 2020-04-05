import pytest

from ..language import *


def test_0520fde7(input_, expected):
    islands = extract_islands(input_, ignore=5)
    merged = elementwise_equal_and(*islands)
    result = switch_color(merged, 1, 2)
    assert result == expected


def test_0d3d703e(input_, expected):
    result = switch_color(input_, 3, 4)
    result = switch_color(result, 1, 5)
    result = switch_color(result, 2, 6)
    result = switch_color(result, 8, 9)
    assert result == expected


def test_1b2d62fb(input_, expected):
    islands = extract_islands(input_, ignore=1)
    merged = elementwise_equal_or(*islands)
    result = switch_color(merged, 0, 9)
    result = switch_color(result, 8, 9)
    assert result == expected


def test_3428a4f5(input_, expected):
    islands = extract_islands(input_, ignore=4)
    merged = elementwise_xor(*islands)
    result = switch_color(merged, 2, 3)


def test_1cf80156(input_, expected):
    islands = extract_islands(input_, ignore=0)
    assert islands == expected


def test_8d5021e8(input_, expected):
    # extend flip_horizontal left
    # extend identity bottom
    # extend identity bottom
    pass


def test_11852cab(input_, expected):
    selection = select_all_colors(input_, ignore=0)
    island = extract_selected_area(input_, selection)
    island = elementwise_equal_or(island, rotate(island, num_times=1))
    island = elementwise_equal_or(island, rotate(island, num_times=2))
    pass


def test_00d62c1b(input_, expected):
    selection = select_color(input_, color=0)
    areas = split_selection_into_connected_areas_no_diagonals(selection)
    areas = filter_selections_touching_edge(areas)
    selection = merge_selections(areas)
    result = set_selected_to_color(input_, selection, color=4)


# def test_31d5ba1a(input_, expected):
#     patches = extract_color_patches(input_, ignore=0)
#     pass
