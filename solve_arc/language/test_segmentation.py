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


def test_concatenate_left_right(horizonal_grid):
    a, b = split_left_right(horizonal_grid)

    assert concatenate_left_right(a, b) == horizonal_grid


def test_concatenate_left_to_right(horizonal_grid):
    grids = split_left_middle_right(horizonal_grid)

    assert concatenate_left_to_right(grids) == horizonal_grid


def test_concatenate_top_bottom(horizonal_grid):
    a, b = split_top_bottom(horizonal_grid)

    assert concatenate_top_bottom(a, b) == horizonal_grid


def test_concatenate_top_to_bottom(vertical_grid):
    grids = split_top_middle_bottom(vertical_grid)

    assert concatenate_top_to_bottom(grids) == vertical_grid


@pytest.fixture
def same_shape_grids():
    return Grids(
        [
            Grid.from_string(
                """
                1 1
                2 2
                """
            ),
            Grid.from_string(
                """
                3 3
                4 4
                """
            ),
        ]
    )


@pytest.fixture
def same_shape_mask():
    return Selection.from_string(
        """
        # .
        . #
        """
    )


def test_merge_grids_with_mask(same_shape_grids, same_shape_mask):
    a, b = same_shape_grids
    expected = Grid.from_string(
        """
        1 3
        4 2
        """
    )

    assert merge_grids_with_mask(a, b, same_shape_mask) == expected


@pytest.fixture
def different_size_grids():
    small = Grid.from_string(
        """
        1
        """
    )
    medium = Grid.from_string(
        """
        1 1 1
        """
    )
    large = Grid.from_string(
        """
        1 1
        1 1
        """
    )
    return small, medium, large


def test_sort_by_area(different_size_grids):
    small, medium, large = different_size_grids
    unsorted_grids = Grids([large, small, medium])

    sorted_grids = sort_by_area(unsorted_grids)

    assert sorted_grids == Grids([small, medium, large])


@pytest.fixture
def different_colored_grids():
    same_colors_0 = Grid.from_string(
        """
        0 1
        """
    )
    same_colors_1 = Grid.from_string(
        """
        1 0
        """
    )
    unique_colors = Grid.from_string(
        """
        2 0
        """
    )
    return Grids([same_colors_0, same_colors_1, unique_colors])


def test_take_grid_with_unique_color(different_colored_grids):
    same_colors_0, same_colors_1, unique_colors = different_colored_grids
    grids = Grids([same_colors_0, unique_colors, same_colors_1])

    assert take_grid_with_unique_colors(grids) == unique_colors


@pytest.fixture
def no_unique_colors_grids():
    return Grids(
        [
            Grid.from_string(
                """
                0 1
                """
            ),
            Grid.from_string(
                """
                1 0
                """
            ),
            Grid.from_string(
                """
                2 0
                """
            ),
            Grid.from_string(
                """
                0 2
                """
            ),
        ]
    )


def test_take_grid_with_unique_color__no_unique(no_unique_colors_grids):
    assert take_grid_with_unique_colors(no_unique_colors_grids) == None
