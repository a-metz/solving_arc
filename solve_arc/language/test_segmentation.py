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


@pytest.fixture
def example_mask():
    return Mask.from_string(
        """
        # . . . . .
        . # # . # #
        . . . . # #
        . # . . . #
        . # # . # .
        . . # . # .
        . . . . . .
        """
    )


def test_split_mask_into_connected_areas(example_mask):
    areas = split_mask_into_connected_areas(example_mask)

    assert set(areas) == {
        Mask.from_string(
            """
            # . . . . .
            . # # . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . # #
            . . . . # #
            . . . . . #
            . . . . # .
            . . . . # .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . . .
            . . . . . .
            . # . . . .
            . # # . . .
            . . # . . .
            . . . . . .
            """
        ),
    }


def test_split_mask_into_connected_areas_no_diagonals(example_mask):
    areas = split_mask_into_connected_areas_no_diagonals(example_mask)

    assert set(areas) == {
        Mask.from_string(
            """
            # . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . # # . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . # #
            . . . . # #
            . . . . . #
            . . . . . .
            . . . . . .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . # .
            . . . . # .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . . .
            . . . . . .
            . # . . . .
            . # # . . .
            . . # . . .
            . . . . . .
            """
        ),
    }


@pytest.fixture
def connected_areas_masks(example_mask):
    """ A sequence of masks with some connected areas
    - without diagonal connection
    - with and without bordering the mask edge
    """
    return split_mask_into_connected_areas_no_diagonals(example_mask)


def test_filter_masks_touching_edge(connected_areas_masks):
    areas = filter_masks_touching_edge(connected_areas_masks)
    print("\n\n".join(str(area) for area in areas))

    assert set(areas) == {
        Mask.from_string(
            """
            # . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . # #
            . . . . # #
            . . . . . #
            . . . . . .
            . . . . . .
            . . . . . .
            """
        ),
    }


def test_filter_masks_not_touching_edge(connected_areas_masks):
    areas = filter_masks_not_touching_edge(connected_areas_masks)
    print("\n\n".join(str(area) for area in areas))

    assert set(areas) == {
        Mask.from_string(
            """
            . . . . . .
            . # # . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . . .
            . . . . # .
            . . . . # .
            . . . . . .
            """
        ),
        Mask.from_string(
            """
            . . . . . .
            . . . . . .
            . . . . . .
            . # . . . .
            . # # . . .
            . . # . . .
            . . . . . .
            """
        ),
    }


def test_merge_masks(connected_areas_masks, example_mask):
    assert merge_masks(connected_areas_masks) == example_mask
