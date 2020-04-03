import pytest

from .function_generation import *
from .nodes import Source
from .sampling_search import Graph


@pytest.fixture
def target():
    return (
        Grid.from_string(
            """
            1 2
            1 1
            """
        ),
    )


@pytest.fixture
def grid():
    return Source.from_scalar(
        Grid.from_string(
            """
            1 2 3
            4 5 6
            7 8 9
            """
        )
    )


@pytest.fixture
def mask_1():
    return Source.from_scalar(
        Mask.from_string(
            """
            # # .
            . # #
            . . #
            """
        )
    )


@pytest.fixture
def mask_2():
    return Source.from_scalar(
        Mask.from_string(
            """
            # # #
            # . .
            # . .
            """
        )
    )


@pytest.fixture
def mask_wrong_size():
    return Source.from_scalar(
        Mask.from_string(
            """
            # #
            # #
            """
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
        Function(vectorize(set_mask_to_color), grid, mask_1, Constant(1)),
        Function(vectorize(set_mask_to_color), grid, mask_2, Constant(1)),
        Function(vectorize(set_mask_to_color), grid, mask_1, Constant(2)),
        Function(vectorize(set_mask_to_color), grid, mask_2, Constant(2)),
    }
