import pytest

from .grid import Grid
from .misc import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_noop(example_grid):
    assert noop(example_grid) == example_grid


def test_map_color(example_grid):
    expected_grid = Grid([[0, 2, 3], [4, 5, 6], [7, 8, 9]])

    assert map_color(example_grid, 1, 0) == expected_grid
