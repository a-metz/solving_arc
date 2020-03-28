from .sampling_search import *


class SingleElementConstant(Constant):
    def __init__(self, scalar):
        self.scalar = scalar
        self.value = (scalar,)


def test_extract_bounding_box_functions():
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

    functions = extract_bounding_box_functions(args)

    assert functions == {Function(vectorize(extract_bounding_box), grid_arg, mask_arg)}
