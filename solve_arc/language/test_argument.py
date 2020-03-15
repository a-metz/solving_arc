import pytest

from .argument import *
from .grid import Grid


@pytest.fixture
def grid():
    return Grid([[1, 2, 3]])


@pytest.fixture
def another_grid():
    return Grid([[4, 5, 6]])


def test_extract_scalar(grid, another_grid):
    assert extract_scalar(grid) == grid
    assert extract_scalar([grid]) == grid
    assert extract_scalar([[grid]]) == grid

    with pytest.raises(ArgumentError):
        extract_scalar(None)
    with pytest.raises(ArgumentError):
        extract_scalar([])
    with pytest.raises(ArgumentError):
        extract_scalar([grid, another_grid])


def test_extract_tuple(grid, another_grid):
    assert extract_tuple([grid, another_grid], length=2) == (grid, another_grid)
    assert extract_tuple([[grid, another_grid]], length=2) == (grid, another_grid)
    assert extract_tuple([[grid], another_grid], length=2) == (grid, another_grid)

    with pytest.raises(ArgumentError):
        extract_tuple(None, length=2)
    with pytest.raises(ArgumentError):
        extract_tuple([], length=2)
    with pytest.raises(ArgumentError):
        extract_tuple([grid], length=2)
    with pytest.raises(ArgumentError):
        extract_tuple([grid, None], length=2)
