import pytest

from .arguments import *
from .color import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


@pytest.fixture
def example_selection():
    return Selection([[True, False, False], [True, True, False], [False, True, True]])


def test_switch_color(example_grid):
    expected_grid = Grid([[2, 1, 3], [4, 5, 6], [7, 8, 9]])
    assert switch_color(example_grid, 1, 2) == expected_grid


def test_switch_color(example_grid, example_selection):
    expected_grid = Grid([[1, 2, 3], [1, 1, 6], [7, 1, 1]])
    assert set_selected_to_color(example_grid, example_selection, 1) == expected_grid


def test_switch_color__to_black(example_grid, example_selection):
    expected_grid = Grid([[0, 2, 3], [0, 0, 6], [7, 0, 0]])
    assert set_selected_to_color(example_grid, example_selection, 0) == expected_grid


def test_map_color(example_grid):
    expected_grid = Grid([[0, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert map_color(example_grid, 1, 0) == expected_grid


def test_map_color_in_selection(example_selection):
    example_grid = Grid([[0, 0, 2], [1, 2, 0], [1, 1, 3]])
    expected_grid = Grid([[0, 0, 2], [3, 2, 0], [1, 3, 3]])

    assert map_color_in_selection(example_grid, example_selection, 1, 3)
