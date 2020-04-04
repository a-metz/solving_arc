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
def mask_1():
    return Constant(
        repeat_once(
            Mask.from_string(
                """
                # # .
                . # #
                . . #
                """
            )
        )
    )


@pytest.fixture
def mask_2():
    return Constant(
        repeat_once(
            Mask.from_string(
                """
                # # #
                # . .
                # . .
                """
            )
        )
    )


@pytest.fixture
def mask_wrong_size():
    return Constant(
        repeat_once(
            Mask.from_string(
                """
                # #
                # #
                """
            )
        )
    )


@pytest.fixture
def graph(target, grid, mask_1, mask_2, mask_wrong_size):
    graph = Graph(target)
    graph.add({grid, mask_1, mask_2, mask_wrong_size})
    return graph


def test_extract_masked_area_functions(graph, grid, mask_1, mask_2):
    functions = extract_masked_area_functions(graph)

    assert functions == {
        Function(vectorize(extract_masked_area), grid, mask_1),
        Function(vectorize(extract_masked_area), grid, mask_2),
    }


def test_set_mask_to_color_functions(graph, grid, mask_1, mask_2):
    functions = set_mask_to_color_functions(graph)

    assert functions == {
        Function(vectorize(set_mask_to_color), grid, mask_1, Constant(repeat_once(1))),
        Function(vectorize(set_mask_to_color), grid, mask_2, Constant(repeat_once(1))),
        Function(vectorize(set_mask_to_color), grid, mask_1, Constant(repeat_once(2))),
        Function(vectorize(set_mask_to_color), grid, mask_2, Constant(repeat_once(2))),
    }
