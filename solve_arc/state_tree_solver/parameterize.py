from .argument import expect_scalar, expect_tuple
from .hashable_partial import partial
from ..language import *


_extract_islands = expect_scalar(on_error_return=None)(extract_islands)
_extract_color_patches = expect_scalar(on_error_return=None)(extract_color_patches)
_extract_color_patch = expect_scalar(on_error_return=None)(extract_color_patch)


@expect_scalar(on_error_return=[])
def parameterize_segmentation(grid):
    """partially apply segmentation with sensible parameter combinations"""
    extract_islands_functions = [
        partial(_extract_islands, ignore=color) for color in grid.used_colors()
    ]
    extract_color_patches_functions = [
        partial(_extract_color_patches, ignore=color) for color in grid.used_colors()
    ]
    extract_color_patch_functions = [
        partial(_extract_color_patch, color=color) for color in grid.used_colors()
    ]
    return extract_islands_functions + extract_color_patches_functions


_elementwise_equal_and = expect_tuple(length=2, on_error_return=None)(elementwise_equal_and)
_elementwise_equal_or = expect_tuple(length=2, on_error_return=None)(elementwise_equal_or)
_elementwise_xor = expect_tuple(length=2, on_error_return=None)(elementwise_xor)


@expect_tuple(length=2, on_error_return=[])
def parameterize_logic(a, b):
    if a.shape != b.shape:
        return []

    return [
        _elementwise_equal_and,
        _elementwise_equal_or,
        _elementwise_xor,
    ]


_switch_color = expect_scalar(on_error_return=None)(switch_color)


@expect_scalar(on_error_return=[])
def parameterize_color(grid):
    """partially apply switch color with sensible parameter combinations"""

    valid_colors = range(10)

    parameterized = []
    for source_color in grid.used_colors():
        for target_color in valid_colors:
            if source_color == target_color:
                continue
            parameterized.append(partial(_switch_color, a=source_color, b=target_color,))

    return parameterized


parameterizers = [parameterize_segmentation, parameterize_logic, parameterize_color]
