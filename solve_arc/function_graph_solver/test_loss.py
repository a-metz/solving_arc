import pytest

from ..language import *
from .loss import *
from .vectorize import *
from .nodes import *


@pytest.fixture
def example_target():
    return Grid.from_string(
        """
        1 2 3
        3 2 1
        """
    )


def test_loss__monotonic_with_depth(example_target):
    example_source = Grid.from_string(
        """
        3 2 1
        1 2 3
        """
    )
    node_depth_0 = Constant(repeat_once(example_source))
    node_depth_1 = Function(lambda x: x, node_depth_0)
    node_depth_2 = Function(lambda x: x, node_depth_1)

    assert (
        0
        <= loss(node_depth_0, repeat_once(example_target), expanded_count=1)
        < loss(node_depth_1, repeat_once(example_target), expanded_count=1)
        < loss(node_depth_2, repeat_once(example_target), expanded_count=1)
        <= 1
    )


def test_loss__monotonic_with_expanded_count(example_target):
    example_source = Grid.from_string(
        """
        3 2 1
        1 2 3
        """
    )
    node = Function(lambda x: x, Constant(repeat_once(example_source)))
    target = repeat_once(example_target)

    assert (
        0
        <= loss(node, target, expanded_count=0)
        < loss(node, target, expanded_count=1)
        < loss(node, target, expanded_count=2)
        <= 1
    )


def test_cells_distance__equal(example_target):
    assert cells_distance(example_target, example_target) == 0


def test_cells_distance__monotonic_with_wrong_cells(example_target):
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
        == cells_distance(example_target, example_target)
        < cells_distance(one_wrong_cell, example_target)
        < cells_distance(two_wrong_cells, example_target)
        <= 1
    )


def test_shape_distance__monotonic_with_wrong_shape_dimensions(example_target):
    correct_shape = Grid.from_string(
        """
        4 5 6
        6 5 4
        """
    )
    height_multiple = Grid.from_string(
        """
        6 5 4
        4 5 6
        6 5 4
        4 5 6
        """
    )
    width_multiple = Grid.from_string(
        """
        6
        4
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
        <= shape_distance(correct_shape, example_target)
        < shape_distance(width_multiple, example_target)
        < shape_distance(wrong_width, example_target)
        < shape_distance(wrong_shape, example_target)
        <= 1
    )
    assert (
        0
        <= shape_distance(correct_shape, example_target)
        < shape_distance(height_multiple, example_target)
        < shape_distance(wrong_height, example_target)
        < shape_distance(wrong_shape, example_target)
        <= 1
    )


def test_color_distance__wrong_colors(example_target):
    wrong_colors = Grid.from_string(
        """
        4 5 6
        6 5 4
        """
    )

    assert 0 <= color_distance(wrong_colors, example_target) <= 1


def test_color_distance__monotonic_with_additional_colors(example_target):
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
        <= color_distance(same_colors, example_target)
        < color_distance(one_color_more, example_target)
        < color_distance(two_colors_more, example_target)
        <= 1
    )


def test_color_distance__monotonic_with_missing_colors(example_target):
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
        <= color_distance(same_colors, example_target)
        < color_distance(one_color_less, example_target)
        < color_distance(two_colors_less, example_target)
        <= 1
    )
