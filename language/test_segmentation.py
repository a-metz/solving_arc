import pytest

from .grid import Grid
from .segmentation import *


@pytest.fixture
def filled_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_extract_rectangle(filled_grid):
    extracted_grid = Grid([[1, 2], [4, 5], [7, 8]])
    assert extract_rectangle(filled_grid, origin=(0, 0), shape=(3, 2)) == extracted_grid


@pytest.fixture
def islands_grid():
    """ A grid with some islands
    - with diagonal connection
    - with different and same values
    - without overlapping bounding boxes
    - with and without bordering the grid edge
    """
    return Grid.from_string(
        """
        1 0 1 0 0 0
        0 1 1 0 2 2
        0 0 0 0 2 2
        0 1 0 0 2 2
        0 1 1 0 0 0
        0 0 1 1 0 0
        0 0 0 0 0 0
        """
    )


def test_extract_islands(islands_grid):
    islands = extract_islands(islands_grid)

    assert len(islands) == 3
    assert (
        Grid.from_string(
            """
            1 0 1
            0 1 1
            """
        )
        in islands
    )
    assert (
        Grid.from_string(
            """
            2 2
            2 2
            2 2
            """
        )
        in islands
    )
    assert (
        Grid.from_string(
            """
            1 0 0
            1 1 0
            0 1 1
            """
        )
        in islands
    )


def test_parameterize():
    grid = Grid([[0, 1, 1]])
    extract_island_functions = parameterize(grid)

    assert len(extract_island_functions) == 2

    islands = {island for func in extract_island_functions for island in func(grid)}
    assert islands == {Grid([[0]]), Grid([[1, 1]])}
