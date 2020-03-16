from ..language import Grid
from .parameterize import *


def test_parameterize_segmentation():
    grid = Grid([[1, 1, 0]])
    segmentation_functions = parameterize_segmentation(grid)

    assert len(segmentation_functions) == 4
    assert all([func(grid) is not None for func in segmentation_functions])


def test_parameterize():
    grids = [Grid([[0, 0, 1, 1]]), Grid([[0, 1, 0, 1]])]

    logic_functions = parameterize_logic(grids)

    assert len(logic_functions) == 3
    results = {func(grids) for func in logic_functions}
    assert results == {Grid([[0, 0, 0, 1]]), Grid([[0, 1, 1, 1]]), Grid([[0, 1, 1, 0]])}


def test_parameterize__different_shapes():
    grids = [Grid([[0, 1]]), Grid([[1, 0, 1]])]

    logic_functions = parameterize_logic(grids)

    assert len(logic_functions) == 0


def test_parameterize__wrong_number_of_arguments():
    grids = [Grid([[0, 1]])]

    logic_functions = parameterize_logic(grids)

    assert len(logic_functions) == 0


def test_color_parameterize():
    grid = Grid([[1, 3]])
    color_functions = parameterize_color(grid)

    # for each source color (1 and 3) to all 9 other colors
    assert len(color_functions) == 2 * 9

    results = {func(grid) for func in color_functions}

    assert results == {
        Grid([[0, 3]]),
        Grid([[2, 3]]),
        Grid([[3, 1]]),  # may be returned mutiple times
        Grid([[4, 3]]),
        Grid([[5, 3]]),
        Grid([[6, 3]]),
        Grid([[7, 3]]),
        Grid([[8, 3]]),
        Grid([[9, 3]]),
        Grid([[1, 0]]),
        Grid([[1, 2]]),
        Grid([[1, 4]]),
        Grid([[1, 5]]),
        Grid([[1, 6]]),
        Grid([[1, 7]]),
        Grid([[1, 8]]),
        Grid([[1, 9]]),
    }
