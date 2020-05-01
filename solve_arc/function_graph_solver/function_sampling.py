import random

import numpy as np

from ..language import *
from .vectorize import *
from .nodes import *


class Graph:
    def __init__(self, initial_nodes, target=None, max_expansions=10):
        self.target = target

        self.nodes = set(initial_nodes)
        self.remaining_expansions = max_expansions

    def expand(self):
        if self.remaining_expansions == 0:
            raise NoRemainingExpansions()
        self.remaining_expansions -= 1

        operation = random_choice(operation_probs)
        args = generate_args[operation](self)
        node = Function(vectorize(operation), *args)

        self.nodes.add(node)

        if node() == self.target:
            return node

        return None


def sample_map_color_args(graph):
    node = _random.choice(list(graph.nodes))
    from_color, to_color = random_permutation(color_probs, 2)
    return node, Constant(repeat(from_color)), Constant(repeat(to_color))


def random_choice(probabilities):
    return _random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]


def random_permutation(probabilities, size):
    return _np_random.choice(
        list(probabilities.keys()), size=size, replace=False, p=list(probabilities.values())
    )


# probabilities all colors
color_probs = {
    Color.BLACK: 0.55,
    Color.BLUE: 0.05,
    Color.RED: 0.05,
    Color.GREEN: 0.05,
    Color.YELLOW: 0.05,
    Color.GRAY: 0.05,
    Color.PINK: 0.05,
    Color.ORANGE: 0.05,
    Color.AZURE: 0.05,
    Color.CRIMSON: 0.05,
}

# map for operation -> function to generate args for operation
generate_args = {map_color: sample_map_color_args}

# probabilities all operations
operation_probs = {map_color: 1.0}

_random = random.Random(0)
_np_random = np.random.RandomState(0)


class NoRemainingExpansions(Exception):
    pass
