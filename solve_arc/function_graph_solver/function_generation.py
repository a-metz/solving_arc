from collections import defaultdict
from itertools import product, combinations

from ..language import *
from .nodes import Function, Constant
from .vectorize import *


def generate_functions(graph):
    functions = (
        switch_color_functions(graph)
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


class Graph:
    def __init__(self, target):
        self.target = target
        self.nodes = set()

        # special node types for faster access
        self._scalars = defaultdict(set)
        self._sequences = defaultdict(set)

    def add(self, nodes):
        # filter valid
        valid_nodes = {node for node in nodes if is_valid(node)}
        self.nodes |= valid_nodes

        # filter special node types
        self._scalars[Grid] |= {node for node in valid_nodes if is_scalar(node, Grid)}
        self._scalars[Mask] |= {node for node in valid_nodes if is_scalar(node, Mask)}
        self._sequences[Grid] |= {node for node in valid_nodes if is_sequence(node, Grid)}
        self._sequences[Mask] |= {node for node in valid_nodes if is_sequence(node, Mask)}

    def scalars(self, type_):
        return self._scalars[type_]

    def sequences(self, type_):
        return self._sequences[type_]


def map_color_functions(graph):
    return {
        Function(vectorize(map_color), arg, Constant(repeat(a)), Constant(repeat(b)))
        for arg in graph.scalars(Grid)
        for a, b in product(
            used_colors(arg()),
            # heuristic: only map to colors used in target
            used_colors(graph.target),
        )
    }


def switch_color_functions(graph):
    return {
        Function(vectorize(switch_color), arg, Constant(repeat(a)), Constant(repeat(b)))
        for arg in graph.scalars(Grid)
        if not (isinstance(arg, Function) and arg.operation == vectorize(switch_color))
        for a, b in combinations(used_colors(arg()), 2)
    }


def mask_for_color_functions(graph):
    return {
        Function(vectorize(mask_for_color), arg, Constant(repeat(color)))
        for arg in graph.scalars(Grid)
        for color in used_colors(arg())
    }


def mask_for_all_colors_functions(graph):
    return {
        Function(vectorize(mask_for_all_colors), arg, Constant(repeat(color)))
        for arg in graph.scalars(Grid)
        for color in used_colors(arg())
        # 2 colors or less is covered by mask_for_color_functions
        if len(used_colors(arg())) > 2
    }


def split_mask_islands_functions(graph):
    return {Function(vectorize(split_mask_islands), arg) for arg in graph.scalars(Mask)}


def set_mask_to_color_functions(graph):
    return {
        Function(vectorize(set_mask_to_color), grid_arg, mask_arg, Constant(repeat(color)))
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
        Function(vectorize(extract_islands), arg, Constant(repeat(color)))
        for arg in graph.scalars(Grid)
        # heuristic: if target has different shape
        if shape(arg()) != shape(graph.target)
        for color in used_colors(arg())
    }


def extract_color_patches_functions(graph):
    return {
        Function(vectorize(extract_color_patches), arg, Constant(repeat(color)))
        for arg in graph.scalars(Grid)
        # heuristic: if target has different shape
        if shape(arg()) != shape(graph.target)
        for color in used_colors(arg())
    }


def extract_color_patch_functions(graph):
    return {
        Function(vectorize(extract_color_patch), arg, Constant(repeat(color)))
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
        functions.add(Function(vectorize(rotate), arg, Constant(repeat(1))))
        functions.add(Function(vectorize(rotate), arg, Constant(repeat(2))))
        functions.add(Function(vectorize(rotate), arg, Constant(repeat(3))))
    return functions


def used_colors(grid_tuple):
    """intersection of used colors in value tuple elements"""
    used_colors = (set(grid.used_colors()) for grid in grid_tuple)
    return set.intersection(*used_colors)


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
        (Function(get_item, arg, Constant(repeat(index))) for index in range(num_elements))
        for arg in args
    }


@vectorize
def shape(value):
    return value.shape


@vectorize
def get_item(values, index):
    return values[index]


def is_valid(node):
    return all(element is not None for element in node())


def is_scalar(node, type_):
    return all(isinstance(element, type_) for element in node())


def is_sequence(node, type_):
    return all(
        hasattr(elements, "__len__") and (isinstance(element, type_) for element in elements)
        for elements in node()
    )
