from itertools import chain, product, combinations
from functools import partial
from collections import namedtuple
import logging

from ..language import *
from .parameterize import parameterizers

logger = logging.getLogger(__name__)


Constraint = namedtuple("Constraint", ["source", "target"])


def solve(constraints, max_depth):
    source, target = constraints[0]

    source_function = Source(source)
    if source_function.result == target:
        return Solution(source_function, source_function)

    leafs = [source_function]
    for step in range(max_depth):
        leafs = valid_functions(leafs, target)
        for leaf in leafs:
            if not hasattr(leaf.result, "__len__") and leaf.result == target:
                return Solution(leaf, source_function)


class Function:
    """cached partial application"""

    def __init__(self, operation, *args, **kwargs):
        self.operation = operation
        self.args = args
        self.kwargs = kwargs

    @property
    def result(self):
        """evaluate function with cached args and update cache"""

        cached_args = [arg.result for arg in self.args]
        cached_kwargs = {key: arg.result for key, arg in self.kwargs.items()}
        result = self.operation(*cached_args, **cached_kwargs)

        # implement caching by overwriting property result for next call
        # (cached_property package is not available on kaggle docker image)
        self.__dict__["result"] = result

        return result

    def __call__(self):
        """evaluate function with real args"""
        real_args = [arg() for arg in self.args]
        real_kwargs = {key: arg() for key, arg in self.kwargs.items()}
        return self.operation(*real_args, **real_kwargs)

    def __str__(self):
        return "{}({})".format(self.operation.__name__, ", ".join(self.format_arguments(str)))

    def __repr__(self):
        return "Function({})".format(
            ", ".join([self.operation.__name__] + self.format_arguments(repr))
        )

    def format_arguments(self, value_formatter):
        args_strings = [value_formatter(arg) for arg in self.args]
        kwargs_strings = [
            "{}={}".format(key, value_formatter(value)) for key, value in self.kwargs.items()
        ]
        return args_strings + kwargs_strings

    # def __eq__(self, other):
    #     return hash(self) == hash(other)

    # def __hash__(self):
    #     return hash(operation) ^ hash(tuple(self.args)) ^ hash(tuple(self.kwargs.items()))


class Source:
    """cached value source"""

    def __init__(self, value=None):
        self.value = value
        self.result = value

    def load(self, value):
        self.value = value

    def __call__(self):
        """reevaluate input after loading"""
        return self.value

    def __str__(self):
        return "source()"

    def __repr__(self):
        # return str(self)
        return "Source({})".format(repr(self.value))


class Constant:
    """cached value source"""

    def __init__(self, value=None):
        self.value = value
        self.result = value

    def __call__(self):
        """reevaluate input after loading"""
        return self.value

    def __str__(self):
        return "const({})".format(str(self.value))

    def __repr__(self):
        # return str(self)
        return "Constant({})".format(repr(self.value))


class Solution:
    def __init__(self, function, source):
        self.function = function
        self.source = source

    def __call__(self, value):
        self.source.load(value)
        return self.function()

    def __str__(self):
        return str(self.function)

    def __repr__(self):
        return "Solution({}, {})".format(repr(self.function), repr(self.source))


def valid_functions(args, target):
    return (
        map_color_functions(args, target)
        + swap_color_functions(args, target)
        + extract_islands_functions(args, target)
        + extract_color_patches_functions(args, target)
        + extract_color_patch_functions(args, target)
        + logic_functions(args, target)
    )


def map_color_functions(args, target):
    return [
        Function(map_color, arg, from_color, to_color)
        for arg in scalar_grids(args)
        for from_color, to_color in product(
            used_colors(arg.result),
            used_colors(target),  # heuristic: only map to colors used in target
        )
    ]


def swap_color_functions(args, target):
    return [
        Function(switch_color, arg, a, b)
        for arg in scalar_grids(args)
        for a, b in combinations(used_colors(arg.result), 2)
    ]


def extract_islands_functions(args, target):
    return [
        Function(extract_islands, arg, ignore=color)
        for arg in scalar_grids(args)
        if arg.result.shape != target.shape  # heuristic: if target has different shape
        for color in used_colors(arg.result)
    ]


def extract_color_patches_functions(args, target):
    return [
        Function(extract_color_patches, arg, ignore=color)
        for arg in scalar_grids(args)
        if arg.result.shape != target.shape  # heuristic: if target has different shape
        for color in used_colors(arg.result)
    ]


def extract_color_patch_functions(args, target):
    return [
        Function(extract_color_patch, arg, color)
        for arg in scalar_grids(args)
        if arg.result.shape != target.shape  # heuristic: if target has different shape
        for color in used_colors(arg.result)
    ]


def logic_functions(args, _):
    functions = []
    for a, b in unpack(shape_matching_grid_pairs(args), 2):
        functions.append(Function(elementwise_equal_and, a, b))
        functions.append(Function(elementwise_equal_or, a, b))
        functions.append(Function(elementwise_xor, a, b))
    return functions


def scalar_grids(args):
    return [arg for arg in args if isinstance(arg.result, Grid)]


def used_colors(grid):
    return [Constant(color) for color in grid.used_colors()]


def shape_matching_grid_pairs(args):
    # TODO: also enumerate all combinations of two scalar grids with same shape
    return [
        arg
        for arg in args
        if hasattr(arg.result, "__len__")
        and len(arg.result) == 2
        and isinstance(arg.result[0], Grid)
        and isinstance(arg.result[1], Grid)
        and arg.result[0].shape == arg.result[1].shape
    ]


def unpack(args, num_elements):
    return [[Function(get_item(index), arg) for index in range(num_elements)] for arg in args]


def get_item(index):
    # TODO: implement as class with hash function dependent on only on argument
    function = lambda container: container[index]
    function.__name__ = "get_item_{}".format(index)
    return function
