import pytest

from grid import *


def test_create_empty():
    grid = Grid.empty(shape=(5, 5))

    assert grid.shape == (5, 5)
    assert grid.state[0, 0] == 0


def test_create_from_2darray():
    grid = Grid([[1, 2], [3, 4]])

    assert grid.shape == (2, 2)
    assert grid.state[0, 0] == 1
    assert grid.state[1, 0] == 3


def test_create_from_2darray__1darray():
    with pytest.raises(ValueError):
        grid = Grid([1, 2])


def test_create_from_2darray__ndarray():
    with pytest.raises(ValueError):
        grid = Grid([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])


def test_equality():
    a = Grid([[1, 2], [3, 4]])
    b = Grid([[1, 2], [3, 4]])
    assert a == b


def test_inequality():
    a = Grid([[1, 2], [3, 4]])
    b = Grid([[0, 2], [3, 4]])
    assert a != b


def test_string_representation():
    grid = Grid([[1, 2], [3, 4]])
    expected_string = "1 2\n3 4"

    assert str(grid) == expected_string
