import pytest

from .grid import Grid
from .segmentation import *


@pytest.fixture
def filled_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


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


@pytest.fixture
def patches_grid():
    """ A grid with some color_patches
    - discontinuous patches
    - neighboring other colors
    - without overlapping bounding boxes
    - with and without bordering the grid edge
    """
    return Grid.from_string(
        """
        1 0 1 0 0 0
        0 1 1 0 2 2
        0 0 0 0 2 2
        0 1 1 2 2 0
        0 0 1 2 2 0
        1 0 0 0 0 0
        """
    )


def test_extract_color_patches(patches_grid):
    patches = extract_color_patches(patches_grid)

    assert len(patches) == 2
    assert (
        Grid.from_string(
            """
            1 0 1
            0 1 1
            0 0 0
            0 1 1
            0 0 1
            1 0 0
            """
        )
        in patches
    )
    assert (
        Grid.from_string(
            """
            0 2 2
            0 2 2
            2 2 0
            2 2 0
            """
        )
        in patches
    )


def test_parameterize():
    grid = Grid([[1, 1, 0]])
    segmentation_functions = parameterize(grid)

    assert len(segmentation_functions) == 4
    assert all([func(grid) is not None for func in segmentation_functions])
