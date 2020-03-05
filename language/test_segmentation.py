import pytest

from .grid import Grid
from .segmentation import *


@pytest.fixture
def filled_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_extract_rectangle(filled_grid):
    extracted_grid = Grid([[1, 2], [4, 5], [7, 8]])
    assert extract_rectangle(filled_grid, origin=(0, 0), shape=(3, 2)) == extracted_grid
