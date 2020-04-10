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
