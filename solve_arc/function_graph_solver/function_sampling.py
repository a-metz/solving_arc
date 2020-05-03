import random

import numpy as np

from ..language import *
from .vectorize import *
from .nodes import *
from .node_collection import *


# TODO: extend to replace function_generation.Graph
class Graph:
    def __init__(self, initial_nodes, target=None, max_expansions=10):
        self.target = target

        self.nodes = NodeCollection(initial_nodes)
        self.function_sampler = FunctionSampler(self)
        self.remaining_expansions = max_expansions

    def expand(self):
        if self.remaining_expansions == 0:
            raise NoRemainingExpansions()
        self.remaining_expansions -= 1

        try:
            node = self.function_sampler()
            self.nodes.add(node)

            if node() == self.target:
                return node

        except NoSample:
            pass

        return None


class NoRemainingExpansions(Exception):
    pass


DISABLED = 0
NOT_IMPLEMENTED = 0


class FunctionSampler:
    def __init__(self, graph):
        self.graph = graph

        # prior probabilities all colors
        self.color_probs = {
            Color.BLACK: 0.55,
            Color.BLUE: 0.05,
            Color.RED: 0.05,
            Color.GREEN: 0.05,
            Color.YELLOW: 0.05,
            Color.GRAY: 0.05,
            Color.PINK: 0.05,
            Color.ORANGE: 0.05,
            Color.AZURE: 0.05,
            Color.CRIMSON: 0.05,
        }

        # prior probabilities all operations
        self.operation_probs = {
            # color
            switch_color: 1.0,
            map_color: 1.0,
            map_color_in_selection: 1.0,
            set_selected_to_color: 1.0,
            fill_grid: DISABLED,
            # compositions
            extract_color_patches: 1.0,
            extract_color_patch: 1.0,
            extract_islands: 1.0,
            # logic
            elementwise_equal_and: 1.0,
            elementwise_equal_or: 1.0,
            elementwise_xor: 1.0,
            selection_elementwise_and: DISABLED,
            selection_elementwise_or: DISABLED,
            selection_elementwise_xor: DISABLED,
            selection_elementwise_eq: DISABLED,
            selection_elementwise_not: DISABLED,
            # segmentation
            extract_selected_areas: 1.0,
            extract_selected_area: 1.0,
            split_left_right: NOT_IMPLEMENTED,
            split_left_middle_right: NOT_IMPLEMENTED,
            split_top_bottom: NOT_IMPLEMENTED,
            split_top_middle_bottom: NOT_IMPLEMENTED,
            concatenate_top_bottom: NOT_IMPLEMENTED,
            concatenate_left_right: NOT_IMPLEMENTED,
            concatenate_top_to_bottom: NOT_IMPLEMENTED,
            concatenate_left_to_right: NOT_IMPLEMENTED,
            merge_grids_with_mask: DISABLED,
            take_first: NOT_IMPLEMENTED,
            take_last: NOT_IMPLEMENTED,
            sort_by_area: NOT_IMPLEMENTED,
            take_grid_with_unique_colors: NOT_IMPLEMENTED,
            # selection
            select_color: NOT_IMPLEMENTED,
            select_all_colors: NOT_IMPLEMENTED,
            split_selection_into_connected_areas: NOT_IMPLEMENTED,
            split_selection_into_connected_areas_no_diagonals: NOT_IMPLEMENTED,
            split_selection_into_connected_areas_skip_gaps: NOT_IMPLEMENTED,
            extend_selections_to_bounds: NOT_IMPLEMENTED,
            extend_selection_to_bounds: NOT_IMPLEMENTED,
            filter_selections_touching_edge: NOT_IMPLEMENTED,
            filter_selections_not_touching_edge: NOT_IMPLEMENTED,
            merge_selections: NOT_IMPLEMENTED,
            # symmetry
            flip_up_down: NOT_IMPLEMENTED,
            flip_left_right: NOT_IMPLEMENTED,
            rotate_90: NOT_IMPLEMENTED,
            rotate_180: NOT_IMPLEMENTED,
            rotate_270: NOT_IMPLEMENTED,
            flip_up_down_within_bounds: NOT_IMPLEMENTED,
            flip_left_right_within_bounds: NOT_IMPLEMENTED,
            rotate_90_within_bounds: NOT_IMPLEMENTED,
            rotate_180_within_bounds: NOT_IMPLEMENTED,
            rotate_270_within_bounds: NOT_IMPLEMENTED,
        }

        # map for operation -> function to generate args for operation
        self.sample_args = {
            # color
            switch_color: self.sample_swap_color_args,
            map_color: self.sample_map_color_args,
            map_color_in_selection: self.sample_map_color_in_selection_args,
            set_selected_to_color: self.sample_set_selected_to_color_args,
            fill_grid: None,
            # compositions
            extract_color_patches: self.sample_extract_args,
            extract_color_patch: self.sample_extract_args,
            extract_islands: self.sample_extract_args,
            # logic
            elementwise_equal_and: self.sample_matching_shape_grids_from_sequence,
            elementwise_equal_or: self.sample_matching_shape_grids_from_sequence,
            elementwise_xor: self.sample_matching_shape_grids_from_sequence,
            selection_elementwise_and: None,
            selection_elementwise_or: None,
            selection_elementwise_xor: None,
            selection_elementwise_eq: None,
            selection_elementwise_not: None,
            # segmentation
            # TODO: sample with highter prob for shape != shape(target)
            extract_selected_areas: lambda: self.sample_matching_shape_nodes(Grid, Selections),
            # TODO: sample with highter prob for shape != shape(target)
            extract_selected_area: lambda: self.sample_matching_shape_nodes(Grid, Selection),
            split_left_right: None,
            split_left_middle_right: None,
            split_top_bottom: None,
            split_top_middle_bottom: None,
            concatenate_top_bottom: None,
            concatenate_left_right: None,
            concatenate_top_to_bottom: None,
            concatenate_left_to_right: None,
            merge_grids_with_mask: None,
            take_first: None,
            take_last: None,
            sort_by_area: None,
            take_grid_with_unique_colors: None,
            # selection
            select_color: None,
            select_all_colors: None,
            split_selection_into_connected_areas: None,
            split_selection_into_connected_areas_no_diagonals: None,
            split_selection_into_connected_areas_skip_gaps: None,
            extend_selections_to_bounds: None,
            extend_selection_to_bounds: None,
            filter_selections_touching_edge: None,
            filter_selections_not_touching_edge: None,
            merge_selections: None,
            # symmetry
            flip_up_down: None,
            flip_left_right: None,
            rotate_90: None,
            rotate_180: None,
            rotate_270: None,
            flip_up_down_within_bounds: None,
            flip_left_right_within_bounds: None,
            rotate_90_within_bounds: None,
            rotate_180_within_bounds: None,
            rotate_270_within_bounds: None,
        }

    def __call__(self):
        operation = sample(self.operation_probs)
        args = self.sample_args[operation]()
        # vectorize operation to as nodes contain all values for all constraints
        return Function(vectorize(operation), *args)

    def sample_swap_color_args(self):
        node = sample_uniform(self.graph.nodes.with_type(Grid))
        # TODO: sample colors based on updated probabilities
        color_candidates = used_colors(node())
        from_color = sample_uniform(color_candidates)
        to_color = sample_uniform(color_candidates - {from_color})
        return node, Constant(repeat(from_color)), Constant(repeat(to_color))

    def sample_map_color_args(self):
        node = sample_uniform(self.graph.nodes.with_type(Grid))
        # TODO: sample colors based on updated probabilities
        from_color = sample_uniform(used_colors(node()))
        to_color = sample_uniform(used_colors(self.graph.target) - {from_color})
        return node, Constant(repeat(from_color)), Constant(repeat(to_color))

    def sample_map_color_in_selection_args(self):
        grid_node, selection_node = self.sample_matching_shape_nodes(Grid, Selection)
        from_color = sample_uniform(used_colors(grid_node()))
        to_color = sample_uniform(used_colors(self.graph.target) - {from_color})
        from_color, to_color = sample_permutation(self.color_probs, 2)
        return grid_node, selection_node, Constant(repeat(from_color)), Constant(repeat(to_color))

    def sample_set_selected_to_color_args(self):
        grid_node, selection_node = self.sample_matching_shape_nodes(Grid, Selection)
        # TODO: sample to_color higher prob for used_colors(target)
        color = sample(self.color_probs)
        return grid_node, selection_node, Constant(repeat(color))

    def sample_extract_args(self):
        grid_node = sample_uniform(
            self.graph.nodes.with_type(Grid) - self.graph.nodes.with_shape(shape(self.graph.target))
        )
        # TODO: sample from_color only from used_colors(grid_node)
        color = sample(self.color_probs)
        return grid_node, Constant(repeat(color))

    def sample_matching_shape_grids_from_sequence(self):
        # TODO: rely on take functions and use scalar grids instead of sequence
        sample_matching_shape_grids = sample_uniform(
            self.graph.nodes.with_type(Grids)
            & self.graph.nodes.with_length(2)
            & self.graph.nodes.matching_shape_sequences()
        )
        return (
            Function(vectorize(take_first), sample_matching_shape_grids),
            Function(vectorize(take_last), sample_matching_shape_grids),
        )

    def sample_matching_selection_node(self, grid_node):
        return sample_uniform(
            self.graph.nodes.with_type(Selection) & self.graph.nodes.with_shape(shape(grid_node()))
        )

    def sample_matching_shape_nodes(self, a_type, b_type):
        a_candidates = set()
        b_candidates = set()
        for shape_ in self.graph.nodes.shapes():
            shape_candidates = self.graph.nodes.with_shape(shape_)
            a_candidates_for_shape = self.graph.nodes.with_type(a_type) & shape_candidates
            b_candidates_for_shape = self.graph.nodes.with_type(b_type) & shape_candidates
            if len(a_candidates_for_shape) > 0 and len(b_candidates_for_shape) > 0:
                a_candidates |= a_candidates_for_shape
                b_candidates |= b_candidates_for_shape

        a_node = sample_uniform(a_candidates)
        b_node = sample_uniform(b_candidates & self.graph.nodes.with_shape(shape(a_node())))
        return a_node, b_node


def sample_uniform(iterable):
    if len(iterable) == 0:
        raise NoSample()

    return _py_random.choice(list(iterable))


def sample(probs):
    return _py_random.choices(list(probs.keys()), weights=list(probs.values()))[0]


def sample_permutation(probs, size):
    return _np_random.choice(list(probs.keys()), size=size, replace=False, p=list(probs.values()))


class NoSample(Exception):
    pass


_py_random = random.Random(0)
_np_random = np.random.RandomState(0)
