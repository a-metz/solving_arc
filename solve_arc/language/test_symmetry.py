import pytest

from .arguments import *
from .symmetry import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2], [3, 4]])


def test_flip_up_down(example_grid):
    assert flip_up_down(example_grid) == Grid([[3, 4], [1, 2]])


def test_flip_left_right(example_grid):
    assert flip_left_right(example_grid) == Grid([[2, 1], [4, 3]])


def test_rotate(example_grid):
    assert rotate_90(example_grid) == Grid([[2, 4], [1, 3]])
    assert rotate_180(example_grid) == Grid([[4, 3], [2, 1]])
    assert rotate_270(example_grid) == Grid([[3, 1], [4, 2]])


@pytest.fixture
def grid_with_island():
    return Grid.from_string(
        """
        0 0 0
        0 1 2
        0 3 4
        """
    )


@pytest.fixture
def selected_island():
    return Selection.from_string(
        """
        . . .
        . # #
        . # #
        """
    )


@pytest.fixture
def selected_incomplete():
    return Selection.from_string(
        """
        . . .
        . # .
        . # #
        """
    )


@pytest.fixture
def selected_all():
    return Selection.from_string(
        """
        # # #
        # # #
        # # #
        """
    )


@pytest.fixture
def selected_non_square():
    return Selection.from_string(
        """
        # # #
        # # #
        . . .
        """
    )


def test_flip_up_down_within_bounds(grid_with_island, selected_island):
    expected = Grid.from_string(
        """
        0 0 0
        0 3 4
        0 1 2
        """
    )

    assert flip_up_down_within_bounds(grid_with_island, selected_island) == expected


def test_flip_left_right_within_bounds__incomplete_selection(grid_with_island, selected_incomplete):
    expected = Grid.from_string(
        """
        0 0 0
        0 2 1
        0 4 3
        """
    )

    assert flip_left_right_within_bounds(grid_with_island, selected_incomplete) == expected


def test_rotate_90_within_bounds(grid_with_island, selected_island):
    expected = Grid.from_string(
        """
        0 0 0
        0 2 4
        0 1 3
        """
    )
    assert rotate_90_within_bounds(grid_with_island, selected_island) == expected


def test_rotate_90_within_bounds__all_selected(grid_with_island, selected_all):
    assert rotate_90_within_bounds(grid_with_island, selected_all) is None


def test_rotate_90_within_bounds__non_square(grid_with_island, selected_non_square):
    assert rotate_90_within_bounds(grid_with_island, selected_non_square) is None
