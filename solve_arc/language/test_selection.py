import pytest

from .arguments import *
from .selection import *


@pytest.fixture
def example_selection():
    return Selection.from_string(
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


def test_split_selection_into_connected_areas(example_selection):
    areas = split_selection_into_connected_areas(example_selection)

    assert set(areas) == {
        Selection.from_string(
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
        Selection.from_string(
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
        Selection.from_string(
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


def test_split_selection_into_connected_areas_no_diagonals(example_selection):
    areas = split_selection_into_connected_areas_no_diagonals(example_selection)

    assert set(areas) == {
        Selection.from_string(
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
        Selection.from_string(
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
        Selection.from_string(
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
        Selection.from_string(
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
        Selection.from_string(
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
def example_selection__with_large_gaps():
    return Selection.from_string(
        """
        # . . . . .
        . # . . # #
        . . . . # #
        . . . . . #
        . # # . # .
        . . # . # .
        . . . . . .
        """
    )


def test_split_selection_into_connected_areas_skip_gaps(
    example_selection__with_large_gaps,
):
    areas = split_selection_into_connected_areas_skip_gaps(
        example_selection__with_large_gaps
    )

    assert set(areas) == {
        Selection.from_string(
            """
        # . . . . .
        . # . . . .
        . . . . . .
        . . . . . .
        . . . . . .
        . . . . . .
        . . . . . .
        """
        ),
        Selection.from_string(
            """
        . . . . . .
        . . . . # #
        . . . . # #
        . . . . . #
        . # # . # .
        . . # . # .
        . . . . . .
        """
        ),
    }


@pytest.fixture
def connected_areas_selections(example_selection):
    """A sequence of selections with some connected areas
    - without diagonal connection
    - with and without bordering the selection edge
    """
    return split_selection_into_connected_areas_no_diagonals(example_selection)


def test_filter_selections_touching_edge(connected_areas_selections):
    areas = filter_selections_touching_edge(connected_areas_selections)
    print("\n\n".join(str(area) for area in areas))

    assert set(areas) == {
        Selection.from_string(
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
        Selection.from_string(
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


def test_filter_selections_not_touching_edge(connected_areas_selections):
    areas = filter_selections_not_touching_edge(connected_areas_selections)
    print("\n\n".join(str(area) for area in areas))

    assert set(areas) == {
        Selection.from_string(
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
        Selection.from_string(
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
        Selection.from_string(
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


def test_merge_selections(connected_areas_selections, example_selection):
    assert merge_selections(connected_areas_selections) == example_selection


def test_extend_selection_to_bounds():
    example_selection = Selection.from_string(
        """
        . # . . .
        . # . # .
        . . . # .
        . . . . .
        """
    )
    expected_selection = Selection.from_string(
        """
        . # # # .
        . # # # .
        . # # # .
        . . . . .
        """
    )

    assert extend_selection_to_bounds(example_selection) == expected_selection


def test_extend_selections_to_bounds(example_selection):
    selections = split_selection_into_connected_areas(example_selection)

    expected_selection = Selection.from_string(
        """
        # # # . . .
        # # # . # #
        . . . . # #
        . # # . # #
        . # # . # #
        . # # . # #
        . . . . . .
        """
    )

    assert (
        merge_selections(extend_selections_to_bounds(selections)) == expected_selection
    )
