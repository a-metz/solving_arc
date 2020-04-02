"""
TODO:
* move f(arg) helper functions (e.g. shape, is_scalar, used_colors(?), ...) to Function Subclass and cache
* wrap node set in proper object, move f(args, [target]) helper functions there and cache
* write unpack function which unpacks first, second, last(?), ...(?) as new nodes
* add cached counters to functions to count number of operations in evaluation subtree (as heuristic for function gen)
"""

from copy import copy
from collections import namedtuple
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
        self.scalar_masks = set()
        self.scalar_grids = set()
        self.sequence_masks = set()
        self.sequence_grids = set()

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
        self.scalar_masks |= {node for node in valid_nodes if is_scalar(node, Mask)}
        self.scalar_grids |= {node for node in valid_nodes if is_scalar(node, Grid)}
        self.sequence_masks |= {node for node in valid_nodes if is_sequence(node, Mask)}
        self.sequence_grids |= {node for node in valid_nodes if is_sequence(node, Grid)}

        # no solution found
        return None


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
