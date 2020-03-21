from .sampling_search import GridTuple, walk
from ..language import Grid


def test_walk():
    structure = [1, [2, 3], [[[4]], 5], [6]]

    assert list(walk(structure)) == [1, 2, 3, 4, 5, 6]


def test_used_colors():
    grid_1 = Grid([[1, 2, 3]])
    grid_2 = Grid([[2, 3, 4]])
    grid_value = GridTuple([grid_1, grid_2])

    assert grid_value.used_colors() == ({2, 3}, {2, 3})
