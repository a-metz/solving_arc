from grid import Grid


def noop(grid):
    return grid


def extract_rect(grid, origin, shape):
    rect = grid[origin[0] : shape[0] - origin[0], origin[1] : shape[1] - origin[1]]
    return Grid(rect)
