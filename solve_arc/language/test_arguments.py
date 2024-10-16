import pytest

from .arguments import *


def test_grid_create_empty():
    grid = Grid.empty(shape=(5, 5))

    assert grid.shape == (5, 5)
    assert grid[0, 0] == 0


def test_grid_create_filled():
    grid = Grid.filled(shape=(5, 5), color=3)

    assert grid.shape == (5, 5)
    assert grid[0, 0] == 3


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


def test_grid_inequality__single_column_vs_single_row():
    a = Grid([[1, 2]])
    b = Grid([[1], [2]])
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


def test_selection_create_empty():
    selection = Selection.empty(shape=(5, 5))

    assert selection.shape == (5, 5)
    assert not selection[0, 0]


def test_selection_create():
    selection = Selection([[True, False], [False, True]])

    assert selection.shape == (2, 2)
    assert selection[0, 0]
    assert not selection[1, 0]


def test_selection_create__non_boolean():
    with pytest.raises(AssertionError):
        selection = Selection([1, 2])

    with pytest.raises(AssertionError):
        selection = Selection([1.0, 2.0])


def test_selection_any():
    assert Selection([[True, False]]).any()
    assert not Selection([[False, False]]).any()


def test_selection_create_from_indices():
    selection = Selection.from_indices(
        shape=(3, 2), indices=[(0, 0), (0, 1), (1, 1), (2, 0)]
    )

    assert selection.shape == (3, 2)
    assert selection == Selection([[True, True], [False, True], [True, False]])


def test_selection_create_from_string():
    string = """
    # #
    # .
    """

    selection = Selection.from_string(string)

    assert selection == Selection([[True, True], [True, False]])


def test_selection_string_representation():
    selection = Selection([[True, True], [True, False]])
    expected_string = "# #\n# ."

    assert str(selection) == expected_string


def test_sequence_append():
    grids = Grids([Grid([[1, 2]]), Grid([[3, 4]])])

    appended = grids.append(Grid([[5, 6]]))

    assert grids == Grids([Grid([[1, 2]]), Grid([[3, 4]])])
    assert appended == Grids([Grid([[1, 2]]), Grid([[3, 4]]), Grid([[5, 6]])])


def test_sequence_apply():
    grids = Grids([Grid([[1, 2]]), Grid([[3, 4]])])

    def set_first_element_zero(grid):
        grid = grid.copy()
        grid.state[0, 0] = 0
        return grid

    applied = grids.apply(set_first_element_zero)

    assert grids == Grids([Grid([[1, 2]]), Grid([[3, 4]])])
    assert applied == Grids([Grid([[0, 2]]), Grid([[0, 4]])])


def test_sequence_shape():
    matching_grids = Grids([Grid([[1, 2]]), Grid([[3, 4]])])
    mismatching_grids = Grids([Grid([[1, 2]]), Grid([[3, 4, 5]])])

    assert matching_grids.shape == (1, 2)
    assert mismatching_grids.shape == None
