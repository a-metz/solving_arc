from ..language import *


def distance(grid, target):
    return (
        shape_distance(grid, target) + color_distance(grid, target) + cells_distance(grid, target)
    ) / 3


def shape_distance(grid, target):
    distance = 0
    if grid.shape[0] != target.shape[0]:
        distance += 0.50
    if grid.shape[1] != target.shape[1]:
        distance += 0.50
    return distance


def color_distance(grid, target):
    wrong_colors = set(grid.used_colors()) ^ set(target.used_colors())
    # at most 10 wrong colors
    return len(wrong_colors) * 0.1


def cells_distance(grid, target):
    if grid.shape != target.shape:
        return 1

    return 1 - (np.sum(grid.state == target.state) / (grid.shape[0] * grid.shape[1]))
