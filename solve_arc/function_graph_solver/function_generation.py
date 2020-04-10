from collections import defaultdict
from itertools import product, combinations
import logging

from ..language import *
from .nodes import Function, Constant
from .vectorize import *

logger = logging.getLogger(__name__)


# TODO: move generate functions into graph, inline functions and give access to self (=graph)
# TODO: rename add to expand without args (maybe option for sample size)
# TODO: add operation counts and/or other heuristics of evaluation subtree as map (node->value) (?)
class Graph:
    def __init__(self, initial_nodes, target, max_depth):
        self.target = target
        self.max_depth = max_depth

        # all nodes that have been generated, for more efficient checking
        self.checked_nodes = set(initial_nodes)
        self.expandable_nodes = set(initial_nodes)

        # nodes by type for faster access
        self.nodes_type = NodesByType()
        self.nodes_type.filter(self.expandable_nodes)

    def expand(self):
        new_nodes = self.generate_functions()

        # manage nodes to be checked
        unchecked_nodes = new_nodes - self.checked_nodes
        check_solution_nodes = {
            node for node in unchecked_nodes if is_valid(node) and node.depth() <= self.max_depth
        }
        # actually check only happens at the end
        self.checked_nodes |= check_solution_nodes

        # manage nodes to be expanded
        self.expandable_nodes |= {
            node for node in new_nodes if is_valid(node) and node.depth() < self.max_depth
        }
        self.nodes_type.filter(self.expandable_nodes)

        logger.debug(
            "new: %d, total expandable: %d, check solution for: %d, total checked: %d",
            len(new_nodes),
            len(self.expandable_nodes),
            len(check_solution_nodes),
            len(self.checked_nodes),
        )

        return check_solution_nodes

    # TODO: switch completely to selection based functions(?)
    # TODO: write unpack function which unpacks first, second, last(?), largest, smallest, tallest, widest, ... as new nodes
    def generate_functions(self):
        functions = (
            select_color_functions(self)
            | select_all_colors_functions(self)
            | extract_selected_area_functions(self)
            | extract_selected_areas_functions(self)
            | set_selected_to_color_functions(self)
            | merge_selections_functions(self)
            | filter_selections_functions(self)
            | split_selection_into_connected_areas_functions(self)
            | switch_color_functions(self)
            | map_color_functions(self)
            | extract_islands_functions(self)
            | extract_color_patches_functions(self)
            | extract_color_patch_functions(self)
            | logic_functions(self)
            | symmetry_functions(self)
        )
        return functions


class NodesByType:
    def __init__(self):
        self.by_type = defaultdict(set)

    def filter(self, nodes):
        for node in nodes:
            vector_iter = iter(node())
            type_ = type(next(vector_iter))
            # only valid if all are equal
            if all(type_ == type(element) for element in vector_iter):
                self.by_type[type_].add(node)

        for type_, nodes in self.by_type.items():
            logger.debug("type %s nodes: %d", type_.__name__, len(nodes))

    def __call__(self, type_):
        return self.by_type[type_]


def map_color_functions(graph):
    return {
        Function(vectorize(map_color), node, Constant(repeat(a)), Constant(repeat(b)))
        for node in graph.nodes_type(Grid)
        for a, b in product(
            used_colors(node()),
            # heuristic: only map to colors used in target
            used_colors(graph.target),
        )
        if a != b
    }


def switch_color_functions(graph):
    return {
        Function(vectorize(switch_color), node, Constant(repeat(a)), Constant(repeat(b)))
        for node in graph.nodes_type(Grid)
        if not (isinstance(node, Function) and node.callable_ == vectorize(switch_color))
        for a, b in combinations(used_colors(node()), 2)
    }


def select_color_functions(graph):
    return {
        Function(vectorize(select_color), node, Constant(repeat(color)))
        for node in graph.nodes_type(Grid)
        for color in used_colors(node())
    }


def select_all_colors_functions(graph):
    return {
        Function(vectorize(select_all_colors), node, Constant(repeat(color)))
        for node in graph.nodes_type(Grid)
        for color in used_colors(node())
        # 2 colors or less is covered by select_color_functions
        if len(used_colors(node())) > 2
    }


def split_selection_into_connected_areas_functions(graph):
    functions = set()
    for node in graph.nodes_type(Selection):
        functions.add(Function(vectorize(split_selection_into_connected_areas), node))
        functions.add(Function(vectorize(split_selection_into_connected_areas_no_diagonals), node))
    return functions


def filter_selections_functions(graph):
    functions = set()
    for node in graph.nodes_type(Selections):
        functions.add(Function(vectorize(filter_selections_touching_edge), node))
        functions.add(Function(vectorize(filter_selections_not_touching_edge), node))
    return functions


def merge_selections_functions(graph):
    return {
        Function(vectorize(merge_selections), selections)
        for selections in graph.nodes_type(Selections)
        if is_matching_shape(selections)
    }


def set_selected_to_color_functions(graph):
    return {
        Function(
            vectorize(set_selected_to_color), grid_node, selection_node, Constant(repeat(color))
        )
        for grid_node, selection_node in product(
            graph.nodes_type(Grid), graph.nodes_type(Selection)
        )
        if shape(grid_node()) == shape(selection_node())
        for color in used_colors(graph.target)
    }


def extract_selected_area_functions(graph):
    return {
        Function(vectorize(extract_selected_area), grid_node, selection_node)
        for grid_node, selection_node in product(
            graph.nodes_type(Grid), graph.nodes_type(Selection)
        )
        if shape(grid_node()) == shape(selection_node())
        # heuristic: if target has different shape
        and shape(grid_node()) != shape(graph.target)
    }


def extract_selected_areas_functions(graph):
    return {
        Function(vectorize(extract_selected_areas), grid_node, selections_node)
        for grid_node, selections_node in product(
            graph.nodes_type(Grid), graph.nodes_type(Selections)
        )
        # can only process nodes ofs length 2 further
        if is_matching_shape(selections_node) and shape(grid_node()) == shape(selections_node()[0])
        # heuristic: if target has different shape
        and shape(grid_node()) != shape(graph.target)
    }


def extract_islands_functions(graph):
    return {
        Function(vectorize(extract_islands), node, Constant(repeat(color)))
        for node in graph.nodes_type(Grid)
        # heuristic: if target has different shape
        if shape(node()) != shape(graph.target)
        for color in used_colors(node())
    }


def extract_color_patches_functions(graph):
    return {
        Function(vectorize(extract_color_patches), node, Constant(repeat(color)))
        for node in graph.nodes_type(Grid)
        # heuristic: if target has different shape
        if shape(node()) != shape(graph.target)
        for color in used_colors(node())
    }


def extract_color_patch_functions(graph):
    return {
        Function(vectorize(extract_color_patch), node, Constant(repeat(color)))
        for node in graph.nodes_type(Grid)
        # heuristic: if target has different shape
        if shape(node()) != shape(graph.target)
        for color in used_colors(node())
    }


# TODO: also enumerate all combinations of two scalar grids with same shape
# TODO: refactor logical functions to also take grid sequences (?)
def logic_functions(graph):
    functions = set()
    for sequence in graph.nodes_type(Grids):
        if is_matching_shape_pair(sequence):
            a = Function(get_item, sequence, Constant(repeat(0)))
            b = Function(get_item, sequence, Constant(repeat(1)))
            functions.add(Function(vectorize(elementwise_equal_and), a, b))
            functions.add(Function(vectorize(elementwise_equal_or), a, b))
            functions.add(Function(vectorize(elementwise_xor), a, b))
    return functions


def symmetry_functions(graph):
    functions = set()
    for node in graph.nodes_type(Grid):
        functions.add(Function(vectorize(flip_up_down), node))
        functions.add(Function(vectorize(flip_left_right), node))
        functions.add(Function(vectorize(rotate_90), node))
        functions.add(Function(vectorize(rotate_180), node))
        functions.add(Function(vectorize(rotate_270), node))
    return functions


def used_colors(grid_vector):
    """intersection of used colors in value tuple elements"""
    used_colors = (set(grid.used_colors()) for grid in grid_vector)
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
def shape(element):
    return element.shape


@vectorize
def get_item(elements, index):
    return elements[index]


def is_valid(node):
    return all(element is not None for element in node())
