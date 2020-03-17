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


def valid_functions(leafs, target):
    return (
        map_color_functions(leafs, target)
        + swap_color_functions(leafs, target)
        + extract_islands_functions(leafs, target)
        + extract_color_patches_functions(leafs, target)
        + extract_color_patch_functions(leafs, target)
        + logic_functions(leafs, target)
    )


def map_color_functions(leafs, target):
    return [
        Function(map_color, leaf, from_color, to_color)
        for leaf in scalar_grids(leafs)
        for from_color, to_color in product(
            used_colors(leaf.result),
            used_colors(target),  # heuristic: only map to colors used in target
        )
    ]


def swap_color_functions(leafs, target):
    return [
        Function(switch_color, leaf, a, b)
        for leaf in scalar_grids(leafs)
        for a, b in combinations(used_colors(leaf.result), 2)
    ]


def extract_islands_functions(leafs, target):
    return [
        Function(extract_islands, leaf, ignore=color)
        for leaf in scalar_grids(leafs)
        if leaf.result.shape != target.shape  # heuristic: if target has different shape
        for color in used_colors(leaf.result)
    ]


def extract_color_patches_functions(leafs, target):
    return [
        Function(extract_color_patches, leaf, ignore=color)
        for leaf in scalar_grids(leafs)
        if leaf.result.shape != target.shape  # heuristic: if target has different shape
        for color in used_colors(leaf.result)
    ]


def extract_color_patch_functions(leafs, target):
    return [
        Function(extract_color_patch, leaf, color)
        for leaf in scalar_grids(leafs)
        if leaf.result.shape != target.shape  # heuristic: if target has different shape
        for color in used_colors(leaf.result)
    ]


def logic_functions(leafs, _):
    functions = []
    for a, b in unpack(shape_matching_grid_pairs(leafs), 2):
        functions.append(Function(elementwise_equal_and, a, b))
        functions.append(Function(elementwise_equal_or, a, b))
        functions.append(Function(elementwise_xor, a, b))
    return functions


def scalar_grids(leafs):
    return [leaf for leaf in leafs if isinstance(leaf.result, Grid)]


def used_colors(grid):
    return [Constant(color) for color in grid.used_colors()]


def shape_matching_grid_pairs(leafs):
    # TODO: also enumerate all combinations of two scalar grids with same shape
    return [
        leaf
        for leaf in leafs
        if hasattr(leaf.result, "__len__")
        and len(leaf.result) == 2
        and isinstance(leaf.result[0], Grid)
        and isinstance(leaf.result[1], Grid)
        and leaf.result[0].shape == leaf.result[1].shape
    ]


def unpack(leafs, num_elements):
    return [[Function(get_item(index), leaf) for index in range(num_elements)] for leaf in leafs]


def get_item(index):
    # TODO: implement as class with hash function dependent on only on argument
    function = lambda container: container[index]
    function.__name__ = "get_item_{}".format(index)
    return function


def format_function_call(function, result, depth):
    indent = "    " * depth
    return "{}{} = {}".format(indent, format_function(function), repr(result))


def format_function(function):
    if isinstance(function, partial):
        return format_partial(function)
    else:
        return function.__name__ + "()"


def format_partial(function):
    """format partial applied function created with functools.partial"""

    positional_args = [repr(arg) for arg in function.args]
    keyword_args = ["{}={}".format(key, repr(value)) for key, value in function.keywords.items()]
    args = ", ".join(positional_args + keyword_args)

    return "{}({})".format(function.func.__name__, args)
