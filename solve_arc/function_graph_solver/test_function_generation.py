import pytest

from .function_generation import *
from .vectorize import *
from .nodes import Constant


@pytest.fixture
def target():
    return repeat_once(
        Grid.from_string(
            """
            1 2
            1 1
            """
        )
    )


@pytest.fixture
def grid():
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
def selection_1():
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
def selection_2():
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
def selection_wrong_size():
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
def graph(target, grid, selection_1, selection_2, selection_wrong_size):
    return Graph({grid, selection_1, selection_2, selection_wrong_size}, target, max_depth=1)


def test_extract_selected_area_functions(graph, grid, selection_1, selection_2):
    functions = extract_selected_area_functions(graph)

    assert functions == {
        Function(vectorize(extract_selected_area), grid, selection_1),
        Function(vectorize(extract_selected_area), grid, selection_2),
    }


def test_set_selected_to_color_functions(graph, grid, selection_1, selection_2):
    functions = set_selected_to_color_functions(graph)

    assert functions == {
        Function(vectorize(set_selected_to_color), grid, selection_1, Constant(repeat_once(1))),
        Function(vectorize(set_selected_to_color), grid, selection_2, Constant(repeat_once(1))),
        Function(vectorize(set_selected_to_color), grid, selection_1, Constant(repeat_once(2))),
        Function(vectorize(set_selected_to_color), grid, selection_2, Constant(repeat_once(2))),
    }
