import pytest

from .grid import *


def test_grid_create_empty():
    grid = Grid.empty(shape=(5, 5))

    assert grid.shape == (5, 5)
    assert grid[0, 0] == 0


def test_grid_create():
    grid = Grid([[1, 2], [3, 4]])

    assert grid.shape == (2, 2)
    assert grid[0, 0] == 1
    assert grid[1, 0] == 3


def test_grid_create__1darray():
    with pytest.raises(AssertionError):
        grid = Grid([1, 2])


def test_grid_create__ndarray():
    with pytest.raises(AssertionError):
        grid = Grid([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])


def test_grid_create__non_integer():
    with pytest.raises(AssertionError):
        grid = Grid([True, False])

    with pytest.raises(AssertionError):
        grid = Grid([1.0, 2.0])


def test_grid_equality():
    a = Grid([[1, 2], [3, 4]])
    b = Grid([[1, 2], [3, 4]])
    assert a == b


def test_grid_inequality():
    a = Grid([[1, 2], [3, 4]])
    b = Grid([[0, 2], [3, 4]])
    assert a != b


def test_grid_create_from_string():
    string = """
    1 2
    3 4
    """
    grid = Grid.from_string(string)

    assert grid == Grid([[1, 2], [3, 4]])


def test_grid_string_representation():
    grid = Grid([[1, 2], [3, 4]])
    expected_string = "1 2\n3 4"

    assert str(grid) == expected_string


def test_grid_copy():
    grid = Grid([[1, 2], [3, 4]])

    copy = grid.copy()
    assert copy == grid

    grid.state[0, 0] = 9
    assert copy != grid


def test_grid_enumerate():
    grid = Grid([[1, 2], [3, 4]])

    assert len(list(grid.enumerate())) == 4
    for index, value in grid.enumerate():
        assert grid[index] == value


def test_grid_used_colors():
    grid = Grid([[1, 2], [1, 4]])

    used_colors = grid.used_colors()
    expected_used_colors = {1, 2, 4}
    assert len(used_colors) == len(expected_used_colors)
    assert set(used_colors) == expected_used_colors


def test_mask_create_empty():
    mask = Mask.empty(shape=(5, 5))

    assert mask.shape == (5, 5)
    assert not mask[0, 0]


def test_mask_create():
    mask = Mask([[True, False], [False, True]])

    assert mask.shape == (2, 2)
    assert mask[0, 0]
    assert not mask[1, 0]


def test_mask_create__non_boolean():
    with pytest.raises(AssertionError):
        mask = Mask([1, 2])

    with pytest.raises(AssertionError):
        mask = Mask([1.0, 2.0])


def test_mask_any():
    assert Mask([[True, False]]).any()
    assert not Mask([[False, False]]).any()


def test_mask_create_from_indices():
    mask = Mask.from_indices(shape=(3, 2), indices=[(0, 0), (0, 1), (1, 1), (2, 0)])

    assert mask.shape == (3, 2)
    assert mask == Mask([[True, True], [False, True], [True, False]])


def test_mask_create_from_string():
    string = """
    # #
    # .
    """

    mask = Mask.from_string(string)

    assert mask == Mask([[True, True], [True, False]])


def test_mask_string_representation():
    mask = Mask([[True, True], [True, False]])
    expected_string = "# #\n# ."

    assert str(mask) == expected_string
