import pytest

from grid import Grid
from transform import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_noop(example_grid):
    assert noop(example_grid) == example_grid


def test_extract_rect(example_grid):
    extracted_grid = Grid([[1, 2], [4, 5], [7, 8]])
    assert extract_rect(example_grid, origin=(0, 0), shape=(3, 2)) == extracted_grid
