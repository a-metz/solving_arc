import pytest

from .grid import Grid
from .control import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_noop(example_grid):
    assert noop(example_grid) == example_grid
