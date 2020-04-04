from itertools import product, combinations

from .graph import Function, Constant
from ..language import *


def generate_functions(graph):
    functions = (
        swap_color_functions(graph)
        | map_color_functions(graph)
        | mask_for_color_functions(graph)
        | mask_for_all_colors_functions(graph)
        | extract_masked_area_functions(graph)
        | split_mask_islands_functions(graph)
        | extract_islands_functions(graph)
        | extract_color_patches_functions(graph)
        | extract_color_patch_functions(graph)
        | logic_functions(graph)
        | symmetry_functions(graph)
    )
    return functions


def map_color_functions(graph):
    return {
        Function(vectorize(map_color), arg, Constant(from_color), Constant(to_color))
        for arg in graph.scalars(Grid)
        for from_color, to_color in product(
            used_colors(arg()),
            # heuristic: only map to colors used in target
            used_colors(graph.target),
        )
    }


def swap_color_functions(graph):
    return {
        Function(vectorize(switch_color), arg, Constant(a), Constant(b))
        for arg in graph.scalars(Grid)
        if not (isinstance(arg, Function) and arg.operation == vectorize(switch_color))
        for a, b in combinations(used_colors(arg()), 2)
    }


def mask_for_color_functions(graph):
    return {
        Function(vectorize(mask_for_color), arg, Constant(color))
        for arg in graph.scalars(Grid)
        for color in used_colors(arg())
    }


def mask_for_all_colors_functions(graph):
    return {
        Function(vectorize(mask_for_all_colors), arg, Constant(color))
        for arg in graph.scalars(Grid)
        for color in used_colors(arg())
        # 2 colors or less is covered by mask_for_color_functions
        if len(used_colors(arg())) > 2
    }


def split_mask_islands_functions(graph):
    return {Function(vectorize(split_mask_islands), arg) for arg in graph.scalars(Mask)}


def set_mask_to_color_functions(graph):
    return {
        Function(vectorize(set_mask_to_color), grid_arg, mask_arg, Constant(color))
        for grid_arg, mask_arg in product(graph.scalars(Grid), graph.scalars(Mask))
        if shape(grid_arg()) == shape(mask_arg())
        # heuristic: if target has different shape
        and shape(grid_arg()) != shape(graph.target)
        for color in used_colors(graph.target)
    }


def extract_masked_area_functions(graph):
    return {
        Function(vectorize(extract_masked_area), grid_arg, mask_arg)
        for grid_arg, mask_arg in product(graph.scalars(Grid), graph.scalars(Mask))
        if shape(grid_arg()) == shape(mask_arg())
        # heuristic: if target has different shape
        and shape(grid_arg()) != shape(graph.target)
    }


def extract_masked_areas_functions(graph):
    return {
        Function(vectorize(extract_masked_area), grid_arg, masks_arg)
        for grid_arg, masks_arg in product(graph.scalars(Grid), graph.sequences(Mask))
        # shortcut: assume all masks in sequences have same shape
        if shape(grid_arg()) == shape(masks_arg()[0])
        # heuristic: if target has different shape
        and shape(grid_arg()) != shape(graph.target)
    }


def extract_islands_functions(graph):
    return {
        Function(vectorize(extract_islands), arg, Constant(color))
        for arg in graph.scalars(Grid)
        # heuristic: if target has different shape
        if shape(arg.value) != shape(graph.target)
        for color in used_colors(arg())
    }


def extract_color_patches_functions(graph):
    return {
        Function(vectorize(extract_color_patches), arg, Constant(color))
        for arg in graph.scalars(Grid)
        # heuristic: if target has different shape
        if shape(arg()) != shape(graph.target)
        for color in used_colors(arg())
    }


def extract_color_patch_functions(graph):
    return {
        Function(vectorize(extract_color_patch), arg, Constant(color))
        for arg in graph.scalars(Grid)
        # heuristic: if target has different shape
        if shape(arg()) != shape(graph.target)
        for color in used_colors(arg())
    }


def logic_functions(graph):
    functions = set()
    for a, b in unpack(shape_matching_pairs(graph.sequences(Grid), Grid, Grid), 2):
        functions.add(Function(vectorize(elementwise_equal_and), a, b))
        functions.add(Function(vectorize(elementwise_equal_or), a, b))
        functions.add(Function(vectorize(elementwise_xor), a, b))
    return functions


def symmetry_functions(graph):
    functions = set()
    for arg in graph.scalars(Grid):
        functions.add(Function(vectorize(flip_up_down), arg))
        functions.add(Function(vectorize(flip_left_right), arg))
        functions.add(Function(vectorize(rotate), arg, Constant(1)))
        functions.add(Function(vectorize(rotate), arg, Constant(2)))
        functions.add(Function(vectorize(rotate), arg, Constant(3)))
    return functions


# break naming conventions for consistent decorator naming
class vectorize:
    """vectorize decorator with hash only dependent on wrapped function"""

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
        len(values) == 2
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
