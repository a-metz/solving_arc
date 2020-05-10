from collections import defaultdict, Counter
from itertools import product, combinations, combinations_with_replacement, permutations, count
from statistics import mean
import logging
import random

from ..language import *
from .nodes import Function, Constant
from .vectorize import *
from .loss import loss

logger = logging.getLogger(__name__)


class Graph:
    def __init__(
        self, initial_nodes, target, max_depth=10, max_usages=10, expand_batch_size=1000, **kwargs
    ):
        self.target = target
        self.max_depth = max_depth
        self.max_usages = max_usages
        self.expand_batch_size = expand_batch_size

        self.random = random.Random(0)  # seed for determinism

        # all nodes that have been generated, for checking for new nodes
        self.nodes = set()

        # count nodes that have already been expanded
        self.expandable_nodes = set()

        self._process(initial_nodes)

    def solve(self):
        try:
            for _ in count():
                solution = self._expand()

                if solution is not None:
                    return solution

        except NoExpandableNodes:
            logger.debug("no futher graph expansion possible")

        return None

    def _expand(self):
        candidates, likelihoods = self._get_sample_candidates_with_likelihoods()
        sample_size = min(len(candidates), self.expand_batch_size)
        expand_next = NodeCollection(
            self.random.choices(candidates, weights=likelihoods, k=sample_size)
        )
        logger.debug(
            "expand %d nodes (Grid: %d, Grids: %d, Selection: %d, Selections: %d)",
            len(expand_next),
            len(expand_next.of_type(Grid)),
            len(expand_next.of_type(Grids)),
            len(expand_next.of_type(Selection)),
            len(expand_next.of_type(Selections)),
        )

        new_nodes = generate_functions(expand_next, self) - self.nodes

        logger.debug(
            "new nodes: %d", len(new_nodes),
        )

        return self._process(new_nodes)

    def _get_sample_candidates_with_likelihoods(self):
        candidates = [node for node in self.expandable_nodes if node.usages <= self.max_usages]

        if len(candidates) == 0:
            raise NoExpandableNodes()

        def likelihood(node):
            min_likelihood = 0.1
            return min_likelihood + (1 / loss(node, self.target))

        likelihoods = [likelihood(node) for node in candidates]
        assert not np.isinf(likelihoods).any()

        return candidates, likelihoods

    def _process(self, new_nodes):
        self.nodes |= new_nodes
        self.expandable_nodes |= {
            node for node in new_nodes if is_valid(node()) and node.depth < self.max_depth
        }
        logger.debug(
            "total expandable: %d, total nodes: %d", len(self.expandable_nodes), len(self.nodes),
        )

        # check for solution
        for node in new_nodes:
            if node() == self.target:
                return node

        return None


class NoExpandableNodes(Exception):
    pass


@reduce_all
def is_valid(value):
    return value is not None


class NodeCollection(set):
    def __init__(self, iterable):
        super().__init__(iterable)
        self._filter_by_type(iterable)

    def _filter_by_type(self, nodes):
        by_type = defaultdict(set)
        for node in nodes:
            vector_iter = iter(node())
            type_ = type(next(vector_iter))
            # only valid if all are equal
            if all(type_ == type(element) for element in vector_iter):
                by_type[type_].add(node)

        self._by_type = by_type

    def of_type(self, type_):
        return self._by_type[type_]


def generate_functions(nodes, graph):
    functions = (
        set()
        | map_color_functions(nodes, graph)
        | map_color_in_selection_functions(nodes, graph)
        | switch_color_functions(nodes, graph)
        | set_selected_to_color_functions(nodes, graph)
        | select_color_functions(nodes, graph)
        | select_all_colors_functions(nodes, graph)
        | split_selection_into_connected_areas_functions(nodes, graph)
        | filter_selections_functions(nodes, graph)
        | merge_selections_functions(nodes, graph)
        | extend_selection_to_bounds_functions(nodes, graph)
        | extend_selections_to_bounds_functions(nodes, graph)
        | extract_selected_area_functions(nodes, graph)
        | extract_selected_areas_functions(nodes, graph)
        | extract_islands_functions(nodes, graph)
        | extract_color_patches_functions(nodes, graph)
        | extract_color_patch_functions(nodes, graph)
        | concatenate_functions(nodes, graph)
        | concatenate_sequence_functions(nodes, graph)
        | split_functions(nodes, graph)
        | logic_functions(nodes, graph)
        | symmetry_functions(nodes, graph)
        | take_functions(nodes, graph)
        | sort_by_area_functions(nodes, graph)
        | select_color_functions(nodes, graph)
    )
    return functions


def map_color_functions(nodes, graph):
    return {
        Function(vectorize(map_color), node, Constant(repeat(a)), Constant(repeat(b)))
        for node in nodes.of_type(Grid)
        for a, b in product(
            used_colors(node()),
            # heuristic: only map to colors used in target
            used_colors(graph.target),
        )
        if a != b
    }


def map_color_in_selection_functions(nodes, graph):
    return {
        Function(
            vectorize(map_color_in_selection),
            grid_node,
            selection_node,
            # heuristic: only map background
            Constant(repeat(0)),
            Constant(repeat(color)),
        )
        for grid_node, selection_node in product(nodes.of_type(Grid), nodes.of_type(Selection))
        if shape(grid_node()) == shape(selection_node())
        # heuristic: only map to colors used in target
        for color in used_colors(graph.target)
    }


def switch_color_functions(nodes, graph):
    return {
        Function(vectorize(switch_color), node, Constant(repeat(a)), Constant(repeat(b)))
        for node in nodes.of_type(Grid)
        if not (isinstance(node, Function) and node.operation == vectorize(switch_color))
        for a, b in combinations(used_colors(node()), 2)
    }


def set_selected_to_color_functions(nodes, graph):
    return {
        Function(
            vectorize(set_selected_to_color), grid_node, selection_node, Constant(repeat(color))
        )
        for grid_node, selection_node in product(nodes.of_type(Grid), nodes.of_type(Selection))
        if shape(grid_node()) == shape(selection_node())
        for color in used_colors(graph.target)
    }


def select_color_functions(nodes, graph):
    return {
        Function(vectorize(select_color), node, Constant(repeat(color)))
        for node in nodes.of_type(Grid)
        for color in used_colors(node())
    }


def select_all_colors_functions(nodes, graph):
    return {
        Function(vectorize(select_all_colors), node, Constant(repeat(color)))
        for node in nodes.of_type(Grid)
        for color in used_colors(node())
        # 2 colors or less is covered by select_color_functions
        if len(used_colors(node())) > 2
    }


def split_selection_into_connected_areas_functions(nodes, graph):
    functions = set()
    for node in nodes.of_type(Selection):
        functions.add(Function(vectorize(split_selection_into_connected_areas), node))
        functions.add(Function(vectorize(split_selection_into_connected_areas_no_diagonals), node))
        functions.add(Function(vectorize(split_selection_into_connected_areas_skip_gaps), node))
    return functions


def filter_selections_functions(nodes, graph):
    functions = set()
    for node in nodes.of_type(Selections):
        functions.add(Function(vectorize(filter_selections_touching_edge), node))
        functions.add(Function(vectorize(filter_selections_not_touching_edge), node))
    return functions


def merge_selections_functions(nodes, graph):
    return {
        Function(vectorize(merge_selections), selections_node)
        for selections_node in nodes.of_type(Selections)
        if is_matching_shape(selections_node())
    }


def extend_selection_to_bounds_functions(nodes, graph):
    return {
        Function(vectorize(extend_selection_to_bounds), selection_node)
        for selection_node in nodes.of_type(Selection)
    }


def extend_selections_to_bounds_functions(nodes, graph):
    return {
        Function(vectorize(extend_selections_to_bounds), selection_node)
        for selection_node in nodes.of_type(Selections)
    }


def extract_selected_area_functions(nodes, graph):
    return {
        Function(vectorize(extract_selected_area), grid_node, selection_node)
        for grid_node, selection_node in product(nodes.of_type(Grid), nodes.of_type(Selection))
        if shape(grid_node()) == shape(selection_node())
        # heuristic: if target has different shape
        and shape(grid_node()) != shape(graph.target)
    }


def extract_selected_areas_functions(nodes, graph):
    return {
        Function(vectorize(extract_selected_areas), grid_node, selections_node)
        for grid_node, selections_node in product(nodes.of_type(Grid), nodes.of_type(Selections))
        # can only process nodes ofs length 2 further
        if is_matching_shape(append(selections_node(), grid_node()))
        # heuristic: if target has different shape
        and shape(grid_node()) != shape(graph.target)
    }


def extract_islands_functions(nodes, graph):
    return {
        Function(vectorize(extract_islands), node, Constant(repeat(color)))
        for node in nodes.of_type(Grid)
        # heuristic: if target has different shape
        if shape(node()) != shape(graph.target)
        for color in used_colors(node())
    }


def extract_color_patches_functions(nodes, graph):
    return {
        Function(vectorize(extract_color_patches), node, Constant(repeat(color)))
        for node in nodes.of_type(Grid)
        # heuristic: if target has different shape
        if shape(node()) != shape(graph.target)
        for color in used_colors(node())
    }


def extract_color_patch_functions(nodes, graph):
    return {
        Function(vectorize(extract_color_patch), node, Constant(repeat(color)))
        for node in nodes.of_type(Grid)
        # heuristic: if target has different shape
        if shape(node()) != shape(graph.target)
        for color in used_colors(node())
    }


def concatenate_functions(nodes, graph):
    functions = set()

    # heuristic: only do concatenations for half target height
    half_height = (
        grid_node
        for grid_node in nodes.of_type(Grid)
        if multiply(height(grid_node()), 2) == height(graph.target)
    )
    for top_node, bottom_node in combinations_with_replacement(half_height, 2):
        if width(top_node()) == width(bottom_node()):
            functions.add(Function(vectorize(concatenate_top_bottom), top_node, bottom_node))

    # heuristic: only do concatenations for half target width
    half_width = (
        grid_node
        for grid_node in nodes.of_type(Grid)
        if multiply(width(grid_node()), 2) == width(graph.target)
    )
    for left_node, right_node in combinations_with_replacement(half_width, 2):
        if height(left_node()) == height(right_node()):
            functions.add(Function(vectorize(concatenate_left_right), left_node, right_node))

    return functions


def concatenate_sequence_functions(nodes, graph):
    functions = set()
    for sequence_node in nodes.of_type(Grids):
        # heuristic: only do concatenations if matching target dimensions
        if is_matching_width(append(sequence_node(), graph.target)) and height_sum(
            sequence_node()
        ) == height(graph.target):
            functions.add(Function(vectorize(concatenate_top_to_bottom), sequence_node))

        if is_matching_height(append(sequence_node(), graph.target)) and width_sum(
            sequence_node()
        ) == width(graph.target):
            functions.add(Function(vectorize(concatenate_left_to_right), sequence_node))
    return functions


def split_functions(nodes, graph):
    functions = set()
    # heuristic: only do concatenations for shape target.shape * num_splits
    for grid_node in nodes.of_type(Grid):
        if height(grid_node()) == multiply(height(graph.target), 2):
            functions.add(Function(vectorize(split_top_bottom), grid_node))
        if height(grid_node()) == multiply(height(graph.target), 3):
            functions.add(Function(vectorize(split_top_middle_bottom), grid_node))
        if width(grid_node()) == multiply(width(graph.target), 2):
            functions.add(Function(vectorize(split_left_right), grid_node))
        if width(grid_node()) == multiply(width(graph.target), 3):
            functions.add(Function(vectorize(split_left_middle_right), grid_node))
    return functions


def logic_functions(nodes, graph):
    functions = set()
    for sequence in nodes.of_type(Grids):
        if is_matching_shape_pair(sequence()):
            a = Function(vectorize(take_first), sequence)
            b = Function(vectorize(take_last), sequence)
            functions.add(Function(vectorize(elementwise_equal_and), a, b))
            functions.add(Function(vectorize(elementwise_equal_or), a, b))
            functions.add(Function(vectorize(elementwise_xor), a, b))

    scalars = nodes.of_type(Grid)
    for a, b in combinations(scalars, 2):
        if shape(a()) == shape(b()):
            functions.add(Function(vectorize(elementwise_equal_or), a, b))
            # makes stuff too slow:
            # functions.add(Function(vectorize(elementwise_equal_and), a, b))
            # functions.add(Function(vectorize(elementwise_xor), a, b))

    return functions


def symmetry_functions(nodes, graph):
    functions = set()
    for node in nodes.of_type(Grid):
        functions.add(Function(vectorize(flip_up_down), node))
        functions.add(Function(vectorize(flip_left_right), node))
        functions.add(Function(vectorize(rotate_90), node))
        functions.add(Function(vectorize(rotate_180), node))
        functions.add(Function(vectorize(rotate_270), node))

    for grid_node, selection_node in product(nodes.of_type(Grid), nodes.of_type(Selection)):
        if shape(grid_node()) != shape(selection_node()):
            continue
        functions.add(Function(vectorize(flip_up_down_within_bounds), grid_node, selection_node))
        functions.add(Function(vectorize(flip_left_right_within_bounds), grid_node, selection_node))
        functions.add(Function(vectorize(rotate_90_within_bounds), grid_node, selection_node))
        functions.add(Function(vectorize(rotate_180_within_bounds), grid_node, selection_node))
        functions.add(Function(vectorize(rotate_270_within_bounds), grid_node, selection_node))

    return functions


def take_functions(nodes, graph):
    functions = set()
    for sequence in nodes.of_type(Grids) | nodes.of_type(Selections):
        functions.add(Function(vectorize(take_first), sequence))
        functions.add(Function(vectorize(take_last), sequence))

    for sequence in nodes.of_type(Grids):
        functions.add(Function(vectorize(take_grid_with_unique_colors), sequence))

    return functions


def sort_by_area_functions(nodes, graph):
    return {
        Function(vectorize(sort_by_area), sequence)
        for sequence in nodes.of_type(Grids) | nodes.of_type(Selections)
    }


def used_colors(grid_vector):
    """intersection of used colors in value tuple elements"""
    used_colors = (set(grid.used_colors()) for grid in grid_vector)
    return set.intersection(*used_colors)


@reduce_all
def is_matching_shape_pair(sequence):
    """assume type is already checked"""
    return len(sequence) == 2 and sequence[0].shape == sequence[1].shape


@reduce_all
def is_matching_shape(sequence):
    """assume type is already checked"""
    if len(sequence) < 2:
        return False

    shape = sequence[0].shape
    return all(scalar.shape == shape for scalar in sequence[1:])


@reduce_all
def is_matching_height(sequence):
    """assume type is already checked"""
    if len(sequence) < 2:
        return False

    height = sequence[0].shape[0]
    return all(scalar.shape[0] == height for scalar in sequence[1:])


@reduce_all
def is_matching_width(sequence):
    """assume type is already checked"""
    if len(sequence) < 2:
        return False

    width = sequence[0].shape[1]
    return all(scalar.shape[1] == width for scalar in sequence[1:])


@vectorize
def shape(element):
    return element.shape


@vectorize
def height(element):
    return element.height


@vectorize
def width(element):
    return element.width


@vectorize
def height_sum(sequence):
    return sum(scalar.height for scalar in sequence)


@vectorize
def width_sum(sequence):
    return sum(scalar.width for scalar in sequence)


def multiply(vector, factor):
    return tuple(scalar * factor for scalar in vector)


@vectorize
def append(sequence, scalar):
    return sequence.append(scalar)
