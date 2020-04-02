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
from .graph import Source

logger = logging.getLogger(__name__)

Constraint = namedtuple("Constraint", ["source", "target"])


def solve(constraints, max_depth):
    sources, targets = zip(*constraints)

    source_function = Source(sources)
    if source_function() == targets:
        return Solution(source_function, source_function)

    nodes = {source_function}
    for _ in range(max_depth):
        generated_nodes = generate_functions(nodes, targets)
        new_nodes = generated_nodes - nodes

        invalid = set()
        # only check new nodes
        for node in new_nodes:
            if not is_valid(node()):
                invalid.add(node)

        nodes |= new_nodes - invalid

        logger.debug(
            "nodes generated: %d, new: %d, invalid: %d, total: %d",
            len(generated_nodes),
            len(new_nodes),
            len(invalid),
            len(nodes),
        )

        for node in nodes:
            # print(node, "->", node())
            if node() == targets:
                return Solution(node, source_function)

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


def is_valid(value_tuple):
    return all(value is not None for value in value_tuple)
