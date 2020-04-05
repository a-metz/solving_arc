"""
TODO:
* write unpack function which unpacks first, second, last(?), largest, smallest, tallest, widest, ... as new nodes
"""

from copy import copy
from collections import namedtuple
import logging

from .function_generation import Graph, generate_functions
from .nodes import Constant
from .vectorize import repeat_once

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
        # only consider nodes not yet in graph
        generated_nodes = generate_functions(graph)
        new_nodes = generate_functions(graph) - graph.nodes

        # check for solution
        for node in new_nodes:
            if node() == graph.target:
                return Solution(node, source_node)

        graph.add(new_nodes)

        logger.debug(
            "nodes generated: %d, new: %d, total: %d",
            len(generated_nodes),
            len(new_nodes),
            len(graph.nodes),
        )

    return None


class Source(Constant):
    def load(self, value):
        """replace value for transfer of program to different inputs"""
        self.value = value

    def __str__(self):
        # do not output value as that would clutter the output
        return "{}".format(self.__class__.__name__.lower())


class Solution:
    def __init__(self, function, source):
        self.function = function
        self.source = source

    def __call__(self, value):
        # run only for single element
        self.source.load(repeat_once(value))
        return self.function(use_cache=False)[0]

    def __str__(self):
        return str(self.function)

    def __repr__(self):
        return "Solution({}, {})".format(repr(self.function), repr(self.source))
