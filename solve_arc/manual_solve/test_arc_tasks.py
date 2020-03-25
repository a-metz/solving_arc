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
    # selection = select_islands(input_, ignore=0)
    # selection = eor(selection, rotate_ccw(selection))
    # selection = eor(selection, rotate_180(selection))
    pass


# def test_31d5ba1a(input_, expected):
#     patches = extract_color_patches(input_, ignore=0)
#     pass
