"""
TODO:
* write unpack function which unpacks first, second, last(?), ...(?) as new nodes
* add cached counters to functions to count number of operations in evaluation subtree (as heuristic for function gen)
Not worth it:
* move f(arg) helper functions (e.g. shape, is_scalar, used_colors(?), ...) to Function Subclass and cache
"""

from copy import copy
from collections import namedtuple, defaultdict
import logging

from .function_generation import generate_functions
from .nodes import Source
from ..language import Grid, Mask

logger = logging.getLogger(__name__)

Constraint = namedtuple("Constraint", ["source", "target"])


def solve(constraints, max_depth):
    source, target = zip(*constraints)
    source_node = Source(source)

    graph = Graph(target)
    solution = graph.add({source_node})
    if solution is not None:
        return Solution(source_node, source_node)

    for _ in range(max_depth):
        solution = graph.add(generate_functions(graph))
        if solution is not None:
            return Solution(solution, source_node)

    return None


class Graph:
    def __init__(self, target):
        self.target = target
        self.nodes = set()

        # special node types for faster access
        self._scalars = defaultdict(set)
        self._sequences = defaultdict(set)

    def add(self, added_nodes):
        # only consider nodes not yet in graph
        new_nodes = added_nodes - self.nodes

        # check for solution
        for node in new_nodes:
            if node() == self.target:
                return node

        # filter valid
        valid_nodes = {node for node in new_nodes if is_valid(node)}
        self.nodes |= valid_nodes

        logger.debug(
            "nodes added: %d, new: %d, valid: %d, total: %d",
            len(added_nodes),
            len(new_nodes),
            len(valid_nodes),
            len(self.nodes),
        )

        # filter special node types
        self._scalars[Grid] |= {node for node in valid_nodes if is_scalar(node, Grid)}
        self._scalars[Mask] |= {node for node in valid_nodes if is_scalar(node, Mask)}
        self._sequences[Grid] |= {node for node in valid_nodes if is_sequence(node, Grid)}
        self._sequences[Mask] |= {node for node in valid_nodes if is_sequence(node, Mask)}

        # no solution found
        return None

    def scalars(type_):
        return self._scalars[type_]

    def sequences(type_):
        return self._sequences[type_]


class Solution:
    def __init__(self, function, source):
        self.function = function
        self.source = source

    def __call__(self, value):
        # run only for single element
        self.source.load((value,))
        return self.function(use_cache=False)[0]

    def __str__(self):
        return str(self.function)

    def __repr__(self):
        return "Solution({}, {})".format(repr(self.function), repr(self.source))


def is_valid(node):
    return all(element is not None for element in node())


def is_scalar(node, type_):
    return all(isinstance(element, type_) for element in node())


def is_sequence(node, type_):
    return all(
        hasattr(elements, "__len__") and (isinstance(element, type_) for element in elements)
        for elements in node()
    )
