from .grid import Grid


def noop(grid):
    return grid


def map_color(grid, from_, to):
    mapped = grid.copy()
    mapped.state[mapped.state == from_] = to
    return mapped
