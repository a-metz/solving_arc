import time
from itertools import product, combinations, repeat, count
from functools import wraps
from collections import namedtuple

from ..language import *


Constraint = namedtuple("Constraint", ["source", "target"])


def solve(constraints, max_depth):
    sources, targets = zip(*constraints)

    source_function = Source(sources)
    if source_function.value == targets:
        return Solution(source_function, source_function)

    nodes = {source_function}
    for _ in range(max_depth):
        nodes |= valid_functions(nodes, targets)
        for node in nodes:
            # print(node, "->", node.value)
            if node.value == targets:
                return Solution(node, source_function)

    # print("No Solution")
    return None


def valid_functions(args, target):
    functions = (
        map_color_functions(args, target)
        | swap_color_functions(args, target)
        | mask_for_color_functions(args)
        | mask_for_all_colors_functions(args)
        | extract_bounding_box_functions(args)
        # | extract_islands_functions(args, target)
        # | extract_color_patches_functions(args, target)
        # | extract_color_patch_functions(args, target)
        | logic_functions(args)
        | symmetry_functions(args)
    )
    return {func for func in functions if is_valid(func.value)}


def map_color_functions(args, target):
    return {
        Function(vectorize(map_color), arg, Constant(from_color), Constant(to_color))
        for arg in scalars(args, Grid)
        for from_color, to_color in product(
            used_colors(arg.value),
            # heuristic: only map to colors used in target
            used_colors(target),
        )
    }


def swap_color_functions(args, target):
    return {
        Function(vectorize(switch_color), arg, Constant(a), Constant(b))
        for arg in scalars(args, Grid)
        for a, b in combinations(used_colors(arg.value), 2)
    }


def mask_for_color_functions(args):
    return {
        Function(vectorize(mask_for_color), arg, Constant(color))
        for arg in scalars(args, Grid)
        for color in used_colors(arg.value)
    }


def mask_for_all_colors_functions(args):
    return {
        Function(vectorize(mask_for_all_colors), arg, Constant(color))
        for arg in scalars(args, Grid)
        for color in used_colors(arg.value)
        # 2 colors or less is covered by mask_for_color_functions
        if len(used_colors(arg.value)) > 2
    }


def extract_bounding_box_functions(args):
    grid_args = scalars(args, Grid)
    mask_args = scalars(args, Mask)
    return {
        Function(vectorize(extract_bounding_box), grid_arg, mask_arg)
        for grid_arg, mask_arg in product(grid_args, mask_args)
        if shape(grid_arg.value) == shape(mask_arg.value)
    }


def extract_color_patches_functions(args, target):
    return {
        Function(vectorize(extract_color_patches), arg, Constant(color))
        for arg in scalars(args, Grid)
        # heuristic: if target has different shape
        if shape(arg.value) != shape(target)
        for color in used_colors(arg.value)
    }


def extract_color_patch_functions(args, target):
    return {
        Function(vectorize(extract_color_patch), arg, Constant(color))
        for arg in scalars(args, Grid)
        # heuristic: if target has different shape
        if shape(arg.value) != shape(target)
        for color in used_colors(arg.value)
    }


def logic_functions(args):
    functions = set()
    for a, b in unpack(shape_matching_pairs(args, Grid), 2):
        functions.add(Function(vectorize(elementwise_equal_and), a, b))
        functions.add(Function(vectorize(elementwise_equal_or), a, b))
        functions.add(Function(vectorize(elementwise_xor), a, b))
    return functions


def symmetry_functions(args):
    functions = set()
    for arg in scalars(args, Grid):
        functions.add(Function(vectorize(flip_up_down), arg))
        functions.add(Function(vectorize(flip_left_right), arg))
        functions.add(Function(vectorize(rotate), arg, Constant(1)))
        functions.add(Function(vectorize(rotate), arg, Constant(2)))
        functions.add(Function(vectorize(rotate), arg, Constant(3)))
    return functions


class Function:
    """cached partial application"""

    def __init__(self, operation, *args):
        self.operation = operation
        self.args = args
        self.called = False

    @property
    def value(self):
        """evaluate function with cached arg values and cache result"""

        arg_values = [arg.value for arg in self.args]
        value = self.operation(*arg_values)

        # TODO: does not cache
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

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.operation) ^ hash(tuple(self.args))


class Source:
    """cached value source"""

    def __init__(self, value):
        self.value = value

    def load(self, value):
        self.value = value

    def __call__(self):
        """reevaluate input after loading"""
        return self.value

    def __str__(self):
        return "source()"

    def __repr__(self):
        return "Source({})".format(repr(self.value))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.value)


class Constant:
    """cached value constant"""

    def __init__(self, scalar):
        self.scalar = scalar
        self.value = repeat(scalar)

    def __call__(self):
        """return scalar wrapped in iterator for use as arguments for vectorized operations"""
        return self.value

    def __str__(self):
        return "constant({})".format(str(self.scalar))

    def __repr__(self):
        return "Constant({})".format(repr(self.value))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.scalar)


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


# break naming conventions for consistent decorator naming
class vectorize:
    def __init__(self, func):
        self.func = func
        self.__name__ = self.func.__name__

    def __call__(self, *arg_tuples):
        return tuple(self.func(*args) for args in zip(*arg_tuples))

    def __hash__(self):
        return hash(self.func)

    def __str__(self):
        return self.func.__name__

    def __repr__(self):
        return "vectorize({})".format(self.func.__name__)


def scalars(args, type_):
    """filter args for grid tuples which are not nested in containers"""
    return {arg for arg in args if is_scalar(arg.value, type_)}


def is_scalar(value_tuple, type_):
    return all(isinstance(value, type_) for value in value_tuple)


def used_colors(grid_tuple):
    """intersection of used colors in value tuple elements"""
    used_colors = (set(grid.used_colors()) for grid in grid_tuple)
    return set.intersection(*used_colors)


@vectorize
def shape(value):
    return value.shape


def shape_matching_pairs(args, type_):
    # TODO: also enumerate all combinations of two scalar grids with same shape
    return {arg for arg in args if is_matching_shape_pair(arg.value, type_)}


def is_matching_shape_pair(value_tuple, type_):
    return all(
        hasattr(value, "__len__")
        and len(value) == 2
        and isinstance(value[0], type_)
        and isinstance(value[1], type_)
        and value[0].shape == value[1].shape
        for value in value_tuple
    )


def unpack(args, num_elements):
    return {
        (Function(get_item, arg, Constant(index)) for index in range(num_elements)) for arg in args
    }


@vectorize
def get_item(values, index):
    return values[index]


def is_valid(value_tuple):
    return all(value is not None for value in value_tuple)
