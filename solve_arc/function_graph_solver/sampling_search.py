from copy import copy
from itertools import count
from collections import defaultdict, namedtuple
from statistics import mean
import logging


from .function_generation import Graph
from .nodes import *
from .vectorize import repeat_once, Vector

logger = logging.getLogger(__name__)

Constraint = namedtuple("Constraint", ["source", "target"])


def solve(constraints, max_depth):
    target = Vector(constraint.target for constraint in constraints)
    source_node = Source(Vector(constraint.source for constraint in constraints))

    if source_node() == target:
        return Solution(source_node, source_node)

    graph = Graph({source_node}, target, max_depth)

    for step in count():
        # only consider nodes not yet in graph
        new_nodes = graph.expand()

        if len(new_nodes) == 0:
            # no new nodes can be generated
            logger.debug("no futher graph expansion possible")
            break

        # check for solution
        for node in new_nodes:
            if node() == graph.target:
                statistics = Statistics.from_graph(node, graph)
                logger.debug("solution statistics: %s", str(statistics))
                return Solution(node, source_node, statistics)

    return None


class Source(Constant):
    def load(self, value):
        """replace value for transfer of program to different inputs"""
        self.value = value

    def __str__(self):
        # do not output value as that would clutter the output
        return "{}".format(self.__class__.__name__.lower())


class Solution:
    def __init__(self, function, source, statistics=None):
        self.function = function
        self.source = source
        self.statistics = statistics

    def __call__(self, value):
        # run only for single element
        self.source.load(repeat_once(value))
        return next(iter(self.function(use_cache=False)))

    def __str__(self):
        return str(self.function)

    def __repr__(self):
        return "Solution({}, {})".format(repr(self.function), repr(self.source))


class Statistics(namedtuple("Statistics", ["depth", "branching_factor", "nodes_count"])):
    @classmethod
    def from_graph(cls, node, graph):
        statistics = cls(
            depth=node.depth(),
            branching_factor=branching_factor(graph),
            nodes_count=len(graph.nodes()),
        )
        return statistics

    def __str__(self):
        return ", ".join("{}: {:.2f}".format(field, getattr(self, field)) for field in self._fields)


def branching_factor(graph):
    children = defaultdict(set)
    for node in graph.nodes():
        if isinstance(node, Function):
            for parent in node.args:
                children[parent].add(node)

    return mean(len(c) for c in children.values())
