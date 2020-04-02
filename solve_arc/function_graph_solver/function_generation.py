from itertools import product, combinations

from .nodes import Function, Constant
from ..language import *


def generate_functions(graph, target):
    args = graph.nodes
    functions = (
        swap_color_functions(args, target)
        | map_color_functions(args, target)
        # | mask_for_color_functions(args)
        # | mask_for_all_colors_functions(args)
        # | extract_masked_area_functions(args, target)
        # | split_mask_islands_functions(args)
        | extract_islands_functions(args, target)
        | extract_color_patches_functions(args, target)
        | extract_color_patch_functions(args, target)
        | logic_functions(args)
        | symmetry_functions(args)
    )
    return functions


def map_color_functions(args, target):
    return {
        Function(vectorize(map_color), arg, Constant(from_color), Constant(to_color))
        for arg in scalars(args, Grid)
        for from_color, to_color in product(
            used_colors(arg()),
            # heuristic: only map to colors used in target
            used_colors(target),
        )
    }


def swap_color_functions(args, target):
    return {
        Function(vectorize(switch_color), arg, Constant(a), Constant(b))
        for arg in scalars(args, Grid)
        if not (isinstance(arg, Function) and arg.operation == vectorize(switch_color))
        for a, b in combinations(used_colors(arg()), 2)
    }


def mask_for_color_functions(args):
    return {
        Function(vectorize(mask_for_color), arg, Constant(color))
        for arg in scalars(args, Grid)
        for color in used_colors(arg())
    }


def mask_for_all_colors_functions(args):
    return {
        Function(vectorize(mask_for_all_colors), arg, Constant(color))
        for arg in scalars(args, Grid)
        for color in used_colors(arg())
        # 2 colors or less is covered by mask_for_color_functions
        if len(used_colors(arg())) > 2
    }


def split_mask_islands_functions(args):
    return {Function(vectorize(split_mask_islands), arg) for arg in scalars(args, Mask)}


def extract_masked_area_functions(args, target):
    grid_args = scalars(args, Grid)
    mask_args = scalars(args, Mask)
    return {
        Function(vectorize(extract_masked_area), grid_arg, mask_arg)
        for grid_arg, mask_arg in product(grid_args, mask_args)
        if shape(grid_arg()) == shape(mask_arg())
        # heuristic: if target has different shape
        and shape(grid_arg()) != shape(target)
    }


def extract_masked_areas_functions(args, target):
    grid_args = scalars(args, Grid)
    masks_args = sequences(args, Mask)
    return {
        Function(vectorize(extract_masked_area), grid_arg, mask_arg)
        for grid_arg, mask_arg in product(grid_args, mask_args)
        # shortcut: assume all masks in sequences have same shape
        if shape(grid_arg()) == shape(mask_arg()[0])
        # heuristic: if target has different shape
        and shape(grid_arg()) != shape(target)
    }


def extract_islands_functions(args, target):
    return {
        Function(vectorize(extract_islands), arg, Constant(color))
        for arg in scalars(args, Grid)
        if shape(arg.value) != shape(target)  # heuristic: if target has different shape
        for color in used_colors(arg())
    }


def extract_color_patches_functions(args, target):
    return {
        Function(vectorize(extract_color_patches), arg, Constant(color))
        for arg in scalars(args, Grid)
        # heuristic: if target has different shape
        if shape(arg()) != shape(target)
        for color in used_colors(arg())
    }


def extract_color_patch_functions(args, target):
    return {
        Function(vectorize(extract_color_patch), arg, Constant(color))
        for arg in scalars(args, Grid)
        # heuristic: if target has different shape
        if shape(arg()) != shape(target)
        for color in used_colors(arg())
    }


def logic_functions(args):
    functions = set()
    for a, b in unpack(shape_matching_pairs(args, Grid, Grid), 2):
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


# break naming conventions for consistent decorator naming
class vectorize:
    def __init__(self, func):
        self.func = func
        self.__name__ = self.func.__name__

    def __call__(self, *arg_tuples):
        return tuple(self.func(*args) for args in zip(*arg_tuples))

    def __str__(self):
        return self.func.__name__

    def __repr__(self):
        return "vectorize({})".format(self.func.__name__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.func)


def scalars(args, type_):
    """filter args for grid tuples which are not nested in containers"""
    return {arg for arg in args if is_scalar(arg(), type_)}


def is_scalar(value_tuple, type_):
    return all(isinstance(value, type_) for value in value_tuple)


def sequences(args, type_):
    """filter args for grid tuples which are not nested in containers"""
    return {arg for arg in args if is_sequence(arg(), type_)}


def is_sequence(values_tuple, type_):
    return all(
        hasattr(values, "__len__") and (isinstance(value, type_) for value in values)
        for values in values_tuple
    )


def used_colors(grid_tuple):
    """intersection of used colors in value tuple elements"""
    used_colors = (set(grid.used_colors()) for grid in grid_tuple)
    return set.intersection(*used_colors)


@vectorize
def shape(value):
    return value.shape


def shape_matching_pairs(args, type_a, type_b):
    # TODO: also enumerate all combinations of two scalar grids with same shape
    return {arg for arg in args if is_matching_shape_pair(arg(), type_a, type_b)}


def is_matching_shape_pair(values_tuple, type_a, type_b):
    return all(
        hasattr(values, "__len__")
        and len(values) == 2
        and isinstance(values[0], type_a)
        and isinstance(values[1], type_b)
        and values[0].shape == values[1].shape
        for values in values_tuple
    )


def unpack(args, num_elements):
    return {
        (Function(get_item, arg, Constant(index)) for index in range(num_elements)) for arg in args
    }


@vectorize
def get_item(values, index):
    return values[index]
