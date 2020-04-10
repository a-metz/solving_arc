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
    extracted = extract_selected_area(example_grid, example_selection)

    assert extracted == expected
