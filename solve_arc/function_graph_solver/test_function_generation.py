import pytest

from .function_generation import *
from .nodes import Source
from .sampling_search import Graph


@pytest.fixture
def dummy_target():
    return (Grid.empty(shape=(1, 1)),)


def test_extract_masked_area_functions(dummy_target):
    grid_arg = Source.from_scalar(
        Grid.from_string(
            """
            1 2 3
            4 5 6
            7 8 9
            """
        )
    )
    mask_arg = Source.from_scalar(
        Mask.from_string(
            """
            # # .
            . # #
            . . #
            """
        )
    )
    wrong_size_mask_arg = Source.from_scalar(
        Mask.from_string(
            """
            # #
            # #
            """
        )
    )
    graph = Graph(dummy_target)
    graph.add({grid_arg, mask_arg, wrong_size_mask_arg})

    functions = extract_masked_area_functions(graph)

    assert functions == {Function(vectorize(extract_masked_area), grid_arg, mask_arg)}
