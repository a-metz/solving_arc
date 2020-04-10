import pytest

from ..language import *
from .loss import *


@pytest.fixture
def example_target():
    return Grid.from_string(
        """
        1 2 3
        3 2 1
        """
    )


def test_distance__equal(example_target):
    assert distance(example_target, example_target) == 0


def test_distance__monotonic_with_wrong_cells(example_target):
    one_wrong_cell = Grid.from_string(
        """
        1 2 3
        3 3 1
        """
    )
    two_wrong_cells = Grid.from_string(
        """
        1 2 3
        3 3 3
        """
    )

    assert (
        0
        == distance(example_target, example_target)
        < distance(one_wrong_cell, example_target)
        < distance(two_wrong_cells, example_target)
        <= 1
    )


def test_distance__monotonic_with_wrong_shape_dimensions(example_target):
    correct_shape = Grid.from_string(
        """
        4 5 6
        6 5 4
        """
    )
    wrong_width = Grid.from_string(
        """
        6 5
        4 5
        """
    )
    wrong_height = Grid.from_string(
        """
        6 5 4
        4 5 6
        6 5 4
        """
    )
    wrong_shape = Grid.from_string(
        """
        6 5
        4 5
        6 5
        """
    )

    assert (
        0
        <= distance(correct_shape, example_target)
        < distance(wrong_width, example_target)
        < distance(wrong_shape, example_target)
        <= 1
    )
    assert (
        0
        <= distance(correct_shape, example_target)
        < distance(wrong_height, example_target)
        < distance(wrong_shape, example_target)
        <= 1
    )


def test_distance__wrong_colors(example_target):
    wrong_colors = Grid.from_string(
        """
        4 5 6
        6 5 4
        """
    )

    assert 0 <= distance(wrong_colors, example_target) <= 1


def test_distance__monotonic_with_additional_colors(example_target):
    same_colors = Grid.from_string(
        """
        3 2 1 1
        1 2 3 1
        """
    )
    one_color_more = Grid.from_string(
        """
        3 2 1 1
        1 2 4 1
        """
    )
    two_colors_more = Grid.from_string(
        """
        3 2 1 1
        5 5 4 1
        """
    )

    assert (
        0
        <= distance(same_colors, example_target)
        < distance(one_color_more, example_target)
        < distance(two_colors_more, example_target)
        <= 1
    )


def test_distance__monotonic_with_missing_colors(example_target):
    same_colors = Grid.from_string(
        """
        3 2 1 1
        1 2 3 1
        """
    )
    one_color_less = Grid.from_string(
        """
        1 2 1 1
        1 2 1 1
        """
    )
    two_colors_less = Grid.from_string(
        """
        1 1 1 1
        1 1 1 1
        """
    )

    assert (
        0
        <= distance(same_colors, example_target)
        < distance(one_color_less, example_target)
        < distance(two_colors_less, example_target)
        <= 1
    )
