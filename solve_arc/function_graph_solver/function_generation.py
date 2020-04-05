from collections import defaultdict
from itertools import product, combinations
import logging

from ..language import *
from .nodes import Function, Constant
from .vectorize import *

logger = logging.getLogger(__name__)


# TODO: switch completely to selection based functions(?)
def generate_functions(graph):
    functions = (
        select_color_functions(graph)
        | select_all_colors_functions(graph)
        | extract_selected_area_functions(graph)
        | extract_selected_areas_functions(graph)
        | set_selected_to_color_functions(graph)
        | merge_selections_functions(graph)
        | filter_selections_functions(graph)
        | split_selection_into_connected_areas_functions(graph)
        | switch_color_functions(graph)
        | map_color_functions(graph)
        | extract_islands_functions(graph)
        | extract_color_patches_functions(graph)
        | extract_color_patch_functions(graph)
        | logic_functions(graph)
        | symmetry_functions(graph)
    )
    return functions


# TODO: refactor
# * move generate functions into graph, inline functions and give access to self (=graph)
# * rename add to expand without args (maybe option for sample size)
# * add operation counts and/or other heuristics of evaluation subtree as map (node->value) (?)
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
        self._scalars[Selection] |= {node for node in valid_nodes if is_scalar(node, Selection)}
        self._sequences[Grid] |= {node for node in valid_nodes if is_sequence(node, Grid)}
        self._sequences[Selection] |= {node for node in valid_nodes if is_sequence(node, Selection)}

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
        if a != b
    }


def switch_color_functions(graph):
    return {
        Function(vectorize(switch_color), arg, Constant(repeat(a)), Constant(repeat(b)))
        for arg in graph.scalars(Grid)
        if not (isinstance(arg, Function) and arg.callable_ == vectorize(switch_color))
        for a, b in combinations(used_colors(arg()), 2)
    }


def select_color_functions(graph):
    return {
        Function(vectorize(select_color), arg, Constant(repeat(color)))
        for arg in graph.scalars(Grid)
        for color in used_colors(arg())
    }


def select_all_colors_functions(graph):
    return {
        Function(vectorize(select_all_colors), arg, Constant(repeat(color)))
        for arg in graph.scalars(Grid)
        for color in used_colors(arg())
        # 2 colors or less is covered by select_color_functions
        if len(used_colors(arg())) > 2
    }


def split_selection_into_connected_areas_functions(graph):
    functions = set()
    for arg in graph.scalars(Selection):
        functions.add(Function(vectorize(split_selection_into_connected_areas), arg))
        functions.add(Function(vectorize(split_selection_into_connected_areas_no_diagonals), arg))
    return functions


def filter_selections_functions(graph):
    functions = set()
    for arg in graph.sequences(Selection):
        functions.add(Function(vectorize(filter_selections_touching_edge), arg))
        functions.add(Function(vectorize(filter_selections_not_touching_edge), arg))
    return functions


def merge_selections_functions(graph):
    return {
        Function(vectorize(merge_selections), selections)
        for selections in graph.sequences(Selection)
        if is_matching_shape(selections)
    }


def set_selected_to_color_functions(graph):
    return {
        Function(vectorize(set_selected_to_color), grid_arg, selection_arg, Constant(repeat(color)))
        for grid_arg, selection_arg in product(graph.scalars(Grid), graph.scalars(Selection))
        if shape(grid_arg()) == shape(selection_arg())
        for color in used_colors(graph.target)
    }


def extract_selected_area_functions(graph):
    return {
        Function(vectorize(extract_selected_area), grid_arg, selection_arg)
        for grid_arg, selection_arg in product(graph.scalars(Grid), graph.scalars(Selection))
        if shape(grid_arg()) == shape(selection_arg())
        # heuristic: if target has different shape
        and shape(grid_arg()) != shape(graph.target)
    }


def extract_selected_areas_functions(graph):
    return {
        Function(vectorize(extract_selected_areas), grid_arg, selections_arg)
        for grid_arg, selections_arg in product(graph.scalars(Grid), graph.sequences(Selection))
        # can only process sequences of length 2 further
        if is_matching_shape(selections_arg) and shape(grid_arg()) == shape(selections_arg()[0])
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


# TODO:
# * also enumerate all combinations of two scalar grids with same shape
# * refactor logical functions to also take graph sequences (?)
def logic_functions(graph):
    functions = set()
    for sequence in graph.sequences(Grid):
        if is_matching_shape_pair(sequence):
            a = Function(get_item, sequence, Constant(repeat(0)))
            b = Function(get_item, sequence, Constant(repeat(1)))
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


def is_matching_shape_pair(sequence_node):
    """assume type is already checked"""
    return all(
        len(sequence) == 2 and sequence[0].shape == sequence[1].shape
        for sequence in sequence_node()
    )


def is_matching_shape(sequence_node):
    """assume type is already checked"""
    return all(
        len(sequence) >= 2 and all(scalar.shape == sequence[0].shape for scalar in sequence[1:])
        for sequence in sequence_node()
    )


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
        hasattr(elements, "__len__") and all(isinstance(element, type_) for element in elements)
        for elements in node()
    )
