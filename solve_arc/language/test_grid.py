import pytest

from .grid import *


def test_create_empty():
    grid = Grid.empty(shape=(5, 5))

    assert grid.shape == (5, 5)
    assert grid[0, 0] == 0


def test_create():
    grid = Grid([[1, 2], [3, 4]])

    assert grid.shape == (2, 2)
    assert grid[0, 0] == 1
    assert grid[1, 0] == 3


def test_create__1darray():
    with pytest.raises(AssertionError):
        grid = Grid([1, 2])


def test_create__ndarray():
    with pytest.raises(AssertionError):
        grid = Grid([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])


def test_equality():
    a = Grid([[1, 2], [3, 4]])
    b = Grid([[1, 2], [3, 4]])
    assert a == b


def test_inequality():
    a = Grid([[1, 2], [3, 4]])
    b = Grid([[0, 2], [3, 4]])
    assert a != b


def test_create_from_string():
    string = """
    1 2
    3 4
    """
    grid = Grid.from_string(string)

    assert grid == Grid([[1, 2], [3, 4]])


def test_string_representation():
    grid = Grid([[1, 2], [3, 4]])
    expected_string = "1 2\n3 4"

    assert str(grid) == expected_string


def test_copy():
    grid = Grid([[1, 2], [3, 4]])

    copy = grid.copy()
    assert copy == grid

    grid.state[0, 0] = 9
    assert copy != grid


def test_enumerate():
    grid = Grid([[1, 2], [3, 4]])

    assert len(list(grid.enumerate())) == 4
    for index, value in grid.enumerate():
        assert grid[index] == value


def test_used_colors():
    grid = Grid([[1, 2], [1, 4]])

    used_colors = grid.used_colors()
    expected_used_colors = {1, 2, 4}
    assert len(used_colors) == len(expected_used_colors)
    assert set(used_colors) == expected_used_colors
