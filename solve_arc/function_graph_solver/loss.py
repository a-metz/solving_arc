from statistics import mean

from ..language import *
from .vectorize import *


def loss(node, target, expanded_count):
    depth_loss = 0.1 * (node.depth + 1)
    distance_loss = mean(distance(node(), target))
    expanded_count_loss = 0.2 * (expanded_count + 1)
    return depth_loss * distance_loss * expanded_count_loss


@vectorize
def distance(value, target):
    if isinstance(value, Grid):
        return grid_distance(value, target)

    if isinstance(value, Grids):
        wrong_type_penalty = 0.1
        return wrong_type_penalty + mean([grid_distance(grid, target) for grid in value])

    return 1


def grid_distance(grid, target):
    return mean(
        [shape_distance(grid, target), color_distance(grid, target), cells_distance(grid, target)]
    )


def shape_distance(grid, target):
    distance = 0
    # height is not equal
    if grid.shape[0] != target.shape[0]:
        distance += 0.25
    # height is not multiple
    if grid.shape[0] % target.shape[0] != 0 and target.shape[0] % grid.shape[0] != 0:
        distance += 0.25
    # width is not equal
    if grid.shape[1] != target.shape[1]:
        distance += 0.25
    # width is not multiple
    if grid.shape[1] % target.shape[1] != 0 and target.shape[1] % grid.shape[1] != 0:
        distance += 0.25
    return distance


def color_distance(grid, target):
    wrong_colors = set(grid.used_colors()) ^ set(target.used_colors())
    # at most 10 wrong colors
    return len(wrong_colors) * 0.1


def cells_distance(grid, target):
    if grid.shape != target.shape:
        return 1

    return 1 - (np.sum(grid.state == target.state) / (grid.shape[0] * grid.shape[1]))
