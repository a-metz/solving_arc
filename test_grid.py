from grid import *


def test_create_empty_grid():
    grid = Grid.empty(shape=(5, 5))

    assert grid.shape == (5, 5)
    assert grid[0, 0] == 0


def test_create_grid_from_2darray():
    grid = Grid([[1, 2], [3, 4]])

    assert grid.shape == (2, 2)
    assert grid[0, 0] == 1
    assert grid[1, 0] == 3
