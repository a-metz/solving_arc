import pytest

from .grid import Grid
from .color import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_map_color(example_grid):
    expected_grid = Grid([[0, 2, 3], [4, 5, 6], [7, 8, 9]])

    assert map_color(example_grid, 1, 0) == expected_grid


def test_switch_color(example_grid):
    expected_grid = Grid([[2, 1, 3], [4, 5, 6], [7, 8, 9]])

    assert switch_color(example_grid, 1, 2) == expected_grid


def test_switch_color_parameterize():
    grid = Grid([[1, 3]])
    switch_color_functions = switch_color.parameterize(grid)

    # for each source color (1 and 3) to all 9 other colors
    assert len(switch_color_functions) == 2 * 9

    results = {func(grid) for func in switch_color_functions}

    assert results == {
        Grid([[0, 3]]),
        Grid([[2, 3]]),
        Grid([[3, 1]]),  # may be returned mutiple times
        Grid([[4, 3]]),
        Grid([[5, 3]]),
        Grid([[6, 3]]),
        Grid([[7, 3]]),
        Grid([[8, 3]]),
        Grid([[9, 3]]),
        Grid([[1, 0]]),
        Grid([[1, 2]]),
        Grid([[1, 4]]),
        Grid([[1, 5]]),
        Grid([[1, 6]]),
        Grid([[1, 7]]),
        Grid([[1, 8]]),
        Grid([[1, 9]]),
    }
