from .hashable_partial import partial
from ..language import *


@expect_scalar(on_error_return=[])
def parameterize_segmentation(grid):
    """partially apply segmentation with sensible parameter combinations"""
    extract_islands_functions = [
        partial(extract_islands, ignore=color) for color in grid.used_colors()
    ]
    extract_color_patches_functions = [
        partial(extract_color_patches, ignore=color) for color in grid.used_colors()
    ]
    return extract_islands_functions + extract_color_patches_functions


@expect_tuple(length=2, on_error_return=[])
def parameterize_logic(a, b):
    if a.shape != b.shape:
        return []

    return [
        elementwise_equal_and,
        elementwise_equal_or,
        elementwise_xor,
    ]


@expect_scalar(on_error_return=[])
def parameterize_color(grid):
    """partially apply switch color with sensible parameter combinations"""

    valid_colors = range(10)

    parameterized = []
    for source_color in grid.used_colors():
        for target_color in valid_colors:
            if source_color == target_color:
                continue
            parameterized.append(partial(switch_color, a=source_color, b=target_color))

    return parameterized


parameterizers = [parameterize_segmentation, parameterize_logic, parameterize_color]
