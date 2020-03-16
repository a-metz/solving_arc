from .argument import expect_scalar


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
