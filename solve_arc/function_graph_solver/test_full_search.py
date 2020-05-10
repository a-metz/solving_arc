import pytest

from .full_search import *
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
    assert nodes.of_type(Grid) == {grid_node}
    assert nodes.of_type(Grids) == {grids_node}
    assert nodes.of_type(Selection) == {selection_node_1, selection_node_2}
    assert nodes.of_type(Selections) == {selections_node}


@pytest.fixture
def graph():
    class Graph:
        target = repeat_once(
            Grid.from_string(
                """
                1 2
                1 1
                """
            )
        )

    return Graph()


def test_extract_selected_area_functions(graph, grid_node, selection_node_1, selection_node_2):
    nodes = NodeCollection([grid_node, selection_node_1, selection_node_2])
    functions = extract_selected_area_functions(nodes, graph)

    assert functions == {
        Function(vectorize(extract_selected_area), grid_node, selection_node_1),
        Function(vectorize(extract_selected_area), grid_node, selection_node_2),
    }


def test_set_selected_to_color_functions(graph, grid_node, selection_node_1, selection_node_2):
    nodes = NodeCollection([grid_node, selection_node_1, selection_node_2])
    functions = set_selected_to_color_functions(nodes, graph)

    assert functions == {
        Function(
            vectorize(set_selected_to_color), grid_node, selection_node_1, Constant(repeat_once(1)),
        ),
        Function(
            vectorize(set_selected_to_color), grid_node, selection_node_2, Constant(repeat_once(1)),
        ),
        Function(
            vectorize(set_selected_to_color), grid_node, selection_node_1, Constant(repeat_once(2)),
        ),
        Function(
            vectorize(set_selected_to_color), grid_node, selection_node_2, Constant(repeat_once(2)),
        ),
    }
