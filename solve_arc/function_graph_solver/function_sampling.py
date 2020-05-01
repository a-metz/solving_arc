import random

import numpy as np

from ..language import *
from .vectorize import *
from .nodes import *
from .node_collection import *


# TODO: extend to replace function_generation.Graph
class Graph:
    def __init__(self, initial_nodes, target=None, max_expansions=10):
        self.target = target
        self.function_sampler = FunctionSampler()

        self.nodes = NodeCollection(initial_nodes)
        self.remaining_expansions = max_expansions

    def expand(self):
        if self.remaining_expansions == 0:
            raise NoRemainingExpansions()
        self.remaining_expansions -= 1

        try:
            node = self.function_sampler(self)
            self.nodes.add(node)

            if node() == self.target:
                return node

        except NoSample:
            pass

        return None


class NoRemainingExpansions(Exception):
    pass


class FunctionSampler:
    def __init__(self):
        # probabilities all colors
        self.color_probs = {
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

        # probabilities all operations
        self.operation_probs = {map_color: 0.5, map_color_in_selection: 0.5}

        # map for operation -> function to generate args for operation
        self.generate_args = {
            map_color: self.sample_map_color_args,
            map_color_in_selection: self.sample_map_color_in_selection_args,
        }

    def __call__(self, graph):
        operation = sample(self.operation_probs)
        args = self.generate_args[operation](graph)
        return Function(vectorize(operation), *args)

    def sample_map_color_args(self, graph):
        node = sample_uniform(graph.nodes.with_type(Grid))
        from_color, to_color = sample_permutation(self.color_probs, 2)
        return node, Constant(repeat(from_color)), Constant(repeat(to_color))

    def sample_map_color_in_selection_args(self, graph):
        grid_node = sample_uniform(graph.nodes.with_type(Grid))
        selection_node = sample_uniform(
            graph.nodes.with_type(Selection) & graph.nodes.with_shape(shape(grid_node()))
        )
        from_color, to_color = sample_permutation(self.color_probs, 2)
        return grid_node, selection_node, Constant(repeat(from_color)), Constant(repeat(to_color))


def sample_uniform(iterable):
    if len(iterable) == 0:
        raise NoSample()

    return _py_random.choice(list(iterable))


def sample(probs):
    return _py_random.choices(list(probs.keys()), weights=list(probs.values()))[0]


def sample_permutation(probs, size):
    return _np_random.choice(list(probs.keys()), size=size, replace=False, p=list(probs.values()))


class NoSample(Exception):
    pass


_py_random = random.Random(0)
_np_random = np.random.RandomState(0)
