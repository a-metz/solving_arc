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
    assert rotate(example_grid, num_times=1) == Grid([[2, 4], [1, 3]])
    assert rotate(example_grid, num_times=2) == Grid([[4, 3], [2, 1]])
    assert rotate(example_grid, num_times=3) == Grid([[3, 1], [4, 2]])
    assert rotate(example_grid, num_times=4) == example_grid
