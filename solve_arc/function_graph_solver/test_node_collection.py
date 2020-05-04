import pytest

from .node_collection import *
from .vectorize import *
from .nodes import Constant


@pytest.fixture
def invalid_node():
    return Constant(repeat_once(None))


@pytest.fixture
def grid_node_1():
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
def grid_node_2():
    return Constant(
        repeat_once(
            Grid.from_string(
                """
                1 1 1
                1 1 1
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
def selection_node_3():
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
def grids_node_different_sizes():
    return Constant(
        repeat_once(
            Grids(
                [
                    Grid.from_string(
                        """
                        1 2 3
                        4 5 6
                        7 8 9
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
    invalid_node,
    grid_node_1,
    grid_node_2,
    selection_node_1,
    selection_node_2,
    selection_node_3,
    grids_node,
    grids_node_different_sizes,
    selections_node,
):
    nodes = NodeCollection(
        [
            invalid_node,
            grid_node_1,
            grid_node_2,
            selection_node_1,
            selection_node_2,
            selection_node_3,
            grids_node,
            grids_node_different_sizes,
            selections_node,
        ]
    )

    assert len(nodes) == 9

    assert nodes.with_type(Grid) == {grid_node_1, grid_node_2}
    assert nodes.with_type(Grids) == {grids_node, grids_node_different_sizes}
    assert nodes.with_type(Selection) == {selection_node_1, selection_node_2, selection_node_3}
    assert nodes.with_type(Selections) == {selections_node}

    assert nodes.with_length(2) == {grids_node, grids_node_different_sizes, selections_node}

    assert nodes.with_shape.values == {(None,), ((3, 3),), ((2, 3),), ((2, 2),)}
    assert nodes.with_shape(((3, 3),)) == {grid_node_1, selection_node_1, selection_node_2}
    assert nodes.with_shape(((2, 3),)) == {grid_node_2}
    assert nodes.with_shape(((2, 2),)) == {selection_node_3, grids_node, selections_node}
    assert nodes.with_shape.matching_sequences == {grids_node, selections_node}

    assert nodes.with_height.values == {(None,), (3,), (2,)}
    assert nodes.with_height((3,)) == {grid_node_1, selection_node_1, selection_node_2}
    assert nodes.with_height((2,)) == {grid_node_2, selection_node_3, grids_node, selections_node}
    assert nodes.with_height.matching_sequences == {grids_node, selections_node}

    assert nodes.with_width.values == {(None,), (3,), (2,)}
    assert nodes.with_width((3,)) == {grid_node_1, grid_node_2, selection_node_1, selection_node_2}
    assert nodes.with_width((2,)) == {selection_node_3, grids_node, selections_node}
    assert nodes.with_width.matching_sequences == {grids_node, selections_node}
