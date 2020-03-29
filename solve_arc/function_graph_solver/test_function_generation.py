import pytest

from .function_generation import *


class SingleElementConstant(Constant):
    def __init__(self, scalar):
        self.scalar = scalar
        self.value = (scalar,)


@pytest.fixture
def dummy_target():
    return (Grid.empty(shape=(1, 1)),)


def test_extract_masked_area_functions(dummy_target):
    grid_arg = SingleElementConstant(
        Grid.from_string(
            """
            1 2 3
            4 5 6
            7 8 9
            """
        )
    )
    mask_arg = SingleElementConstant(
        Mask.from_string(
            """
            # # .
            . # #
            . . #
            """
        )
    )
    wrong_size_mask_arg = SingleElementConstant(
        Mask.from_string(
            """
            # #
            # #
            """
        )
    )
    args = {grid_arg, mask_arg, wrong_size_mask_arg}

    functions = extract_masked_area_functions(args, dummy_target)

    assert functions == {Function(vectorize(extract_masked_area), grid_arg, mask_arg)}
