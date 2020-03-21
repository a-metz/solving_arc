from itertools import chain, product, combinations, repeat
from functools import partial, wraps
from collections import namedtuple
import logging

from ..language import *
from .parameterize import parameterizers

logger = logging.getLogger(__name__)


Constraint = namedtuple("Constraint", ["source", "target"])


def solve(constraints, max_depth):
    sources, targets = zip(*constraints)

    source_function = Source(sources)
    if source_function.value == targets:
        return Solution(source_function, source_function)

    leafs = [source_function]
    for step in range(max_depth):
        leafs = valid_functions(leafs, targets)
        for leaf in leafs:
            # print(leaf, "->", leaf.value)
            if leaf.value == targets:
                return Solution(leaf, source_function)

    # print("No Solution")
    return None


class Function:
    """cached partial application"""

    def __init__(self, operation, *args, **kwargs):
        self.operation = operation
        self.args = args
        self.kwargs = kwargs

    @property
    def value(self):
        """evaluate function with cached arg values and cache result"""

        arg_values = [arg.value for arg in self.args]
        value = self.operation(*arg_values)

        # implement caching by overwriting property value for next call
        # (cached_property package is not available on kaggle docker image)
        self.__dict__["value"] = value
        return value

    def __call__(self):
        """reevaluate function with reevaluated args"""
        args = [arg() for arg in self.args]
        return self.operation(*args)

    def __str__(self):
        return "{}({})".format(self.operation.__name__, ", ".join(str(arg) for arg in self.args))

    def __repr__(self):
        return "Function({})".format(
            ", ".join([self.operation.__name__] + [repr(arg) for arg in self.args])
        )

    # def __eq__(self, other):
    #     return hash(self) == hash(other)

    # def __hash__(self):
    #     return hash(operation) ^ hash(tuple(self.args)) ^ hash(tuple(self.kwargs.items()))


def vectorize(func):
    """vectorize function for elements in tuple of first argument"""

    # TODO: vectorize over multiple arguments (argument on decorator creation?)
    @wraps(func)
    def wrapper(*arg_tuples):
        return tuple(func(*args) for args in zip(*arg_tuples))

    # wrapper.__name__ = "vectorize({})".format(func.__name__)
    return wrapper


class Source:
    """cached value source"""

    def __init__(self, value=None):
        self.value = value

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

    # def __eq__(self, other):
    #     return hash(self) == hash(other)

    # def __hash__(self):
    #     return hash(self.value)


class Constant:
    """cached value constant"""

    def __init__(self, scalar=None):
        self.value = repeat(scalar)

    def __call__(self):
        """reevaluate input after loading"""
        return self.value

    def __str__(self):
        return "const({})".format(str(self.value))

    def __repr__(self):
        # return str(self)
        return "Constant({})".format(repr(self.value))

    # def __eq__(self, other):
    #     return hash(self) == hash(other)

    # def __hash__(self):
    #     return hash(self.value)


class Solution:
    def __init__(self, function, source):
        self.function = function
        self.source = source

    def __call__(self, value):
        # run only for single element
        self.source.load((value,))
        return self.function()[0]

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
        Function(vectorize(map_color), arg, Constant(from_color), Constant(to_color),)
        for arg in scalar_grids(args)
        for from_color, to_color in product(
            used_colors(arg.value),
            used_colors(target),  # heuristic: only map to colors used in target
        )
    ]


def swap_color_functions(args, target):
    return [
        Function(vectorize(switch_color), arg, Constant(a), Constant(b),)
        for arg in scalar_grids(args)
        for a, b in combinations(used_colors(arg.value), 2)
    ]


def extract_islands_functions(args, target):
    return [
        Function(vectorize(extract_islands), arg, Constant(color))
        for arg in scalar_grids(args)
        if shape(arg.value) != shape(target)  # heuristic: if target has different shape
        for color in used_colors(arg.value)
    ]


def extract_color_patches_functions(args, target):
    return [
        Function(vectorize(extract_color_patches), arg, Constant(color))
        for arg in scalar_grids(args)
        if shape(arg.value) != shape(target)  # heuristic: if target has different shape
        for color in used_colors(arg.value)
    ]


def extract_color_patch_functions(args, target):
    return [
        Function(vectorize(extract_color_patch), arg, Constant(color))
        for arg in scalar_grids(args)
        if shape(arg.value) != shape(target)  # heuristic: if target has different shape
        for color in used_colors(arg.value)
    ]


def logic_functions(args, _):
    functions = []
    for a, b in unpack(shape_matching_grid_pairs(args), 2):
        functions.append(Function(vectorize(elementwise_equal_and), a, b))
        functions.append(Function(vectorize(elementwise_equal_or), a, b))
        functions.append(Function(vectorize(elementwise_xor), a, b))
    return functions


def scalar_grids(args):
    """filter args for grid tuples which are not nested in containers"""
    return [arg for arg in args if is_scalar(arg.value)]


def is_scalar(grid_tuple):
    return all(isinstance(grid, Grid) for grid in grid_tuple)


def used_colors(grid_tuple):
    """intersection of used colors in value tuple elements"""
    used_colors = (set(grid.used_colors()) for grid in grid_tuple)
    return set.intersection(*used_colors)


@vectorize
def shape(grid):
    return grid.shape


def shape_matching_grid_pairs(args):
    # TODO: also enumerate all combinations of two scalar grids with same shape
    return [arg for arg in args if is_matching_shape_pair(arg.value)]


def is_matching_shape_pair(grids_tuple):
    return all(
        hasattr(grids, "__len__")
        and len(grids) == 2
        and isinstance(grids[0], Grid)
        and isinstance(grids[1], Grid)
        and grids[0].shape == grids[1].shape
        for grids in grids_tuple
    )


def unpack(args, num_elements):
    return [
        [Function(vectorize(get_item), arg, Constant(index)) for index in range(num_elements)]
        for arg in args
    ]


def get_item(grids, index):
    return grids[index]
