import pytest

from .node_collection import *
from .vectorize import *
from .nodes import Constant


@pytest.fixture
def invalid_node():
    return Constant(repeat_once(None))


@pytest.fixture
def grid_node():
    return Constant(
        repeat_once(
            Grid.from_string(
                """
                1 2 3
                4 5 6
                7 8 9
                """
            )
        )
    )


@pytest.fixture
def selection_node_1():
    return Constant(
        repeat_once(
            Selection.from_string(
                """
                # # .
                . # #
                . . #
                """
            )
        )
    )


@pytest.fixture
def selection_node_2():
    return Constant(
        repeat_once(
            Selection.from_string(
                """
                # # #
                # . .
                # . .
                """
            )
        )
    )


@pytest.fixture
def selection_node_wrong_size():
    return Constant(
        repeat_once(
            Selection.from_string(
                """
                # #
                # #
                """
            )
        )
    )


@pytest.fixture
def grids_node():
    return Constant(
        repeat_once(
            Grids(
                [
                    Grid.from_string(
                        """
                        1 1
                        1 0
                        """
                    ),
                    Grid.from_string(
                        """
                        0 1
                        1 0
                        """
                    ),
                ]
            )
        )
    )


@pytest.fixture
def selections_node():
    return Constant(
        repeat_once(
            Selections(
                [
                    Selection.from_string(
                        """
                        # #
                        # .
                        """
                    ),
                    Selection.from_string(
                        """
                        . #
                        # .
                        """
                    ),
                ]
            )
        )
    )


def test_node_collections(
    invalid_node, grid_node, grids_node, selection_node_1, selection_node_2, selections_node
):
    nodes = NodeCollection(
        [invalid_node, grid_node, grids_node, selection_node_1, selection_node_2, selections_node]
    )

    assert len(nodes) == 6
    assert nodes.with_type(Grid) == {grid_node}
    assert nodes.with_type(Grids) == {grids_node}
    assert nodes.with_type(Selection) == {selection_node_1, selection_node_2}
    assert nodes.with_type(Selections) == {selections_node}
    assert nodes.with_shape(((3, 3),)) == {grid_node, selection_node_1, selection_node_2}
