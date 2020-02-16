import pytest

from grid import Grid
from operation import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_noop(example_grid):
    assert noop(example_grid) == example_grid


def test_extract_rectangle(example_grid):
    extracted_grid = Grid([[1, 2], [4, 5], [7, 8]])
    assert extract_rectangle(example_grid, origin=(0, 0), shape=(3, 2)) == extracted_grid


def test_elementwise_operation__different_shapes():
    a = Grid([[1, 2]])
    b = Grid([[1, 2], [3, 4]])

    with pytest.raises(ValueError):
        elementwise_eand(a, b)


def test_elementwise_eand():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 4]])

    assert elementwise_eand(a, b) == Grid([[0, 0], [0, 4]])


def test_elementwise_eand__inequal_nonzero_elements():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 5]])

    with pytest.raises(Exception):
        elementwise_eand(a, b)


def test_elementwise_eor():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 4]])

    assert elementwise_eor(a, b) == Grid([[0, 2], [3, 4]])


def test_elementwise_eor__inequal_nonzero_elements():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 5]])

    with pytest.raises(Exception):
        elementwise_eor(a, b)


def test_elementwise_xor():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 4]])

    assert elementwise_xor(a, b) == Grid([[0, 2], [3, 0]])
