from ..utilities.hashable_partial import partial

from .grid import Grid
from .argument import extract_scalar, ArgumentError


def parameterize(args):
    """partially apply switch color with sensible parameter combinations"""
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return []

    valid_colors = range(10)

    parameterized = []
    for source_color in grid.used_colors():
        for target_color in valid_colors:
            if source_color == target_color:
                continue
            parameterized.append(partial(switch_color, a=source_color, b=target_color))

    return parameterized


def switch_color(args, a, b):
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return None

    return _switch_color(grid, a, b)


def map_color(args, from_, to):
    try:
        grid = extract_scalar(args)
    except ArgumentError:
        return None

    return _map_color(grid, from_, to)


def _switch_color(grid, a, b):
    mapped = grid.copy()
    mapped.state[grid.state == a] = b
    mapped.state[grid.state == b] = a
    return mapped


def _map_color(grid, from_, to):
    mapped = grid.copy()
    mapped.state[mapped.state == from_] = to
    return mapped
