import numpy as np

from .grid import Grid


def extract_rectangle(grid, origin, shape):
    return grid[origin[0] : shape[0] - origin[0], origin[1] : shape[1] - origin[1]]


def _neighbors(index):
    y, x = index
    return [
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
        (y, x - 1),
        (y, x + 1),
        (y + 1, x - 1),
        (y + 1, x),
        (y + 1, x + 1),
    ]


def extract_islands(grid, water=0):
    unassigned = {index for index, value in np.ndenumerate(grid.state) if value != water}

    def discover_island_bounds(index):
        top, left = index
        bottom, right = index[0] + 1, index[1] + 1

        for neighbor in _neighbors(index):
            if neighbor in unassigned:
                unassigned.remove(neighbor)
                top_, left_, bottom_, right_ = discover_island_bounds(neighbor)
                top = min(top, top_)
                left = min(left, left_)
                bottom = max(bottom, bottom_)
                right = max(right, right_)

        return top, left, bottom, right

    islands = []
    while len(unassigned) > 0:
        top, left, bottom, right = discover_island_bounds(unassigned.pop())
        island = Grid(grid.state[top:bottom, left:right])
        islands.append(island)

    return islands
