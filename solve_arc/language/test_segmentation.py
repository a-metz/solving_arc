import pytest

from .arguments import *
from .segmentation import *


@pytest.fixture
def example_grid():
    return Grid.from_string(
        """
        1 0 1 0
        2 1 1 2
        0 2 2 0
        """
    )


@pytest.fixture
def example_selection():
    return Selection.from_string(
        """
        . . . .
        # . # .
        . # # .
        """
    )


def test_extract_selected_area(example_grid, example_selection):
    expected = Grid.from_string(
        """
        2 1 1
        0 2 2
        """
    )

    assert extract_selected_area(example_grid, example_selection) == expected


@pytest.fixture
def horizonal_grid():
    return Grid.from_string(
        """
        1 0 2 3 4 5
        0 1 2 3 4 4
        """
    )


def test_split_left_right(horizonal_grid):
    expected = Grids(
        [
            Grid.from_string(
                """
                1 0 2
                0 1 2
                """
            ),
            Grid.from_string(
                """
                3 4 5
                3 4 4
                """
            ),
        ]
    )

    assert split_left_right(horizonal_grid) == expected


def test_split_left_middle_right(horizonal_grid):
    expected = Grids(
        [
            Grid.from_string(
                """
                1 0
                0 1
                """
            ),
            Grid.from_string(
                """
                2 3
                2 3
                """
            ),
            Grid.from_string(
                """
                4 5
                4 4
                """
            ),
        ]
    )

    assert split_left_middle_right(horizonal_grid) == expected


def test_split_top_bottom(horizonal_grid):
    expected = Grids(
        [
            Grid.from_string(
                """
                1 0 2 3 4 5
                """
            ),
            Grid.from_string(
                """
                0 1 2 3 4 4
                """
            ),
        ]
    )

    assert split_top_bottom(horizonal_grid) == expected


@pytest.fixture
def vertical_grid():
    return Grid.from_string(
        """
        1 4
        2 5
        3 6
        """
    )


def test_split_top_middle_bottom(vertical_grid):
    expected = Grids(
        [
            Grid.from_string(
                """
                1 4
                """
            ),
            Grid.from_string(
                """
                2 5
                """
            ),
            Grid.from_string(
                """
                3 6
                """
            ),
        ]
    )

    assert split_top_middle_bottom(vertical_grid) == expected
