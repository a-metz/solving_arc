from ..utilities.hashable_partial import partial

from .grid import Grid
from .argument import expect_scalar


@expect_scalar(on_error_return=[])
def parameterize(grid):
    """partially apply switch color with sensible parameter combinations"""

    valid_colors = range(10)

    parameterized = []
    for source_color in grid.used_colors():
        for target_color in valid_colors:
            if source_color == target_color:
                continue
            parameterized.append(partial(switch_color, a=source_color, b=target_color))

    return parameterized


@expect_scalar(on_error_return=None)
def switch_color(grid, a, b):
    mapped = grid.copy()
    mapped.state[grid.state == a] = b
    mapped.state[grid.state == b] = a
    return mapped


@expect_scalar(on_error_return=None)
def map_color(grid, from_, to):
    mapped = grid.copy()
    mapped.state[mapped.state == from_] = to
    return mapped
