import random
import logging
from collections import Counter
from itertools import count

import numpy as np

from ..language import *
from .vectorize import *
from .nodes import *
from .node_collection import *


logger = logging.getLogger(__name__)


class Graph:
    def __init__(self, initial_nodes, target, max_depth=5, max_steps=10000, **kwargs):
        self.target = target
        self.max_depth = max_depth if max_depth is not None else float("inf")
        self.steps = range(max_steps) if max_steps else count()

        self.nodes = NodeCollection(initial_nodes)
        self.function_sampler = FunctionSampler(self)
        self.expansion_count = 0

    def solve(self):
        for step in self.steps:
            try:
                node = self.function_sampler()

                if node.depth < self.max_depth:
                    self.nodes.add(node)

                if node() == self.target:
                    return node

            except NoSample:
                pass

        logger.debug("max steps reached")
        return None


DISABLED = 0


class FunctionSampler:
    def __init__(self, graph):
        self.nodes = graph.nodes
        self.target = graph.target

        self.color_weights = {
            Color.BLACK: 1.0,
            Color.BLUE: 1.0,
            Color.RED: 1.0,
            Color.GREEN: 1.0,
            Color.YELLOW: 1.0,
            Color.GRAY: 1.0,
            Color.PINK: 1.0,
            Color.ORANGE: 1.0,
            Color.AZURE: 1.0,
            Color.CRIMSON: 1.0,
        }

        self.operation_weights = {
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
            split_left_right: 1.0,
            split_left_middle_right: 1.0,
            split_top_bottom: 1.0,
            split_top_middle_bottom: 1.0,
            concatenate_top_bottom: 1.0,
            concatenate_left_right: 1.0,
            concatenate_top_to_bottom: 1.0,
            concatenate_left_to_right: 1.0,
            merge_grids_with_mask: 1.0,
            take_first: 1.0,
            take_last: 1.0,
            sort_by_area: 1.0,
            take_grid_with_unique_colors: 1.0,
            # selection
            select_color: 1.0,
            select_all_colors: 1.0,
            split_selection_into_connected_areas: 1.0,
            split_selection_into_connected_areas_no_diagonals: 1.0,
            split_selection_into_connected_areas_skip_gaps: 1.0,
            extend_selections_to_bounds: 1.0,
            extend_selection_to_bounds: 1.0,
            filter_selections_touching_edge: 1.0,
            filter_selections_not_touching_edge: 1.0,
            merge_selections: 1.0,
            # symmetry
            flip_up_down: 1.0,
            flip_left_right: 1.0,
            rotate_90: 1.0,
            rotate_180: 1.0,
            rotate_270: 1.0,
            flip_up_down_within_bounds: 1.0,
            flip_left_right_within_bounds: 1.0,
            rotate_90_within_bounds: 1.0,
            rotate_180_within_bounds: 1.0,
            rotate_270_within_bounds: 1.0,
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
            elementwise_equal_and: self.sample_logic_args,
            elementwise_equal_or: self.sample_logic_args,
            elementwise_xor: self.sample_logic_args,
            selection_elementwise_and: None,
            selection_elementwise_or: None,
            selection_elementwise_xor: None,
            selection_elementwise_eq: None,
            selection_elementwise_not: None,
            # segmentation
            # TODO: sample with highter prob for shape != shape(target)
            extract_selected_areas: lambda: self.sample_matching_shape_args(
                Grid, Selections
            ),
            # TODO: sample with highter prob for shape != shape(target)
            extract_selected_area: lambda: self.sample_matching_shape_args(
                Grid, Selection
            ),
            split_left_right: lambda: self.sample_split_args(width_segments=2),
            split_left_middle_right: lambda: self.sample_split_args(width_segments=3),
            split_top_bottom: lambda: self.sample_split_args(height_segments=2),
            split_top_middle_bottom: lambda: self.sample_split_args(height_segments=3),
            concatenate_top_bottom: self.sample_concatenate_top_bottom_args,
            concatenate_left_right: self.sample_concatenate_left_right_args,
            concatenate_top_to_bottom: self.sample_concatenate_top_to_bottom_args,
            concatenate_left_to_right: self.sample_concatenate_left_to_right_args,
            merge_grids_with_mask: lambda: self.sample_matching_shape_args(
                Grid, Grid, Selection
            ),
            take_first: lambda: self.sample_type_args(Grids, Selections),
            take_last: lambda: self.sample_type_args(Grids, Selections),
            sort_by_area: lambda: self.sample_type_args(Grids, Selections),
            take_grid_with_unique_colors: lambda: self.sample_type_args(Grids),
            # selection
            select_color: self.sample_select_color_args,
            select_all_colors: self.sample_select_color_args,
            split_selection_into_connected_areas: lambda: self.sample_type_args(
                Selection
            ),
            split_selection_into_connected_areas_no_diagonals: lambda: self.sample_type_args(
                Selection
            ),
            split_selection_into_connected_areas_skip_gaps: lambda: self.sample_type_args(
                Selection
            ),
            extend_selections_to_bounds: lambda: self.sample_type_args(Selections),
            extend_selection_to_bounds: lambda: self.sample_type_args(Selection),
            filter_selections_touching_edge: lambda: self.sample_type_args(Selections),
            filter_selections_not_touching_edge: lambda: self.sample_type_args(
                Selections
            ),
            merge_selections: self.sample_merge_selection_args,
            # symmetry
            flip_up_down: lambda: self.sample_type_args(Grid),
            flip_left_right: lambda: self.sample_type_args(Grid),
            rotate_90: lambda: self.sample_type_args(Grid),
            rotate_180: lambda: self.sample_type_args(Grid),
            rotate_270: lambda: self.sample_type_args(Grid),
            flip_up_down_within_bounds: lambda: self.sample_matching_shape_args(
                Grid, Selection
            ),
            flip_left_right_within_bounds: lambda: self.sample_matching_shape_args(
                Grid, Selection
            ),
            rotate_90_within_bounds: lambda: self.sample_matching_shape_args(
                Grid, Selection
            ),
            rotate_180_within_bounds: lambda: self.sample_matching_shape_args(
                Grid, Selection
            ),
            rotate_270_within_bounds: lambda: self.sample_matching_shape_args(
                Grid, Selection
            ),
        }

    def __call__(self):
        operation = self.sample_operation()
        args = self.sample_args[operation]()
        # vectorize operation to as nodes contain all values for all constraints
        return Function(vectorize(operation), *args)

    def sample_operation(self):
        operations = list(self.operation_weights.keys())
        weights = list(self.operation_weights.values())
        return _py_random.choices(operations, weights=weights)[0]

    def sample_swap_color_args(self):
        node = self.sample_node(self.nodes.with_type(Grid))
        # TODO: sample colors based on updated probabilities
        color_candidates = used_colors(node())
        from_color = self.sample_color(color_candidates)
        to_color = self.sample_color(color_candidates - {from_color})
        return node, Constant(repeat(from_color)), Constant(repeat(to_color))

    def sample_map_color_args(self):
        node = self.sample_node(self.nodes.with_type(Grid))
        # TODO: sample colors based on updated probabilities
        target_colors = used_colors(self.target)
        to_color = self.sample_color(target_colors)
        from_color = self.sample_color(used_colors(node()) - {to_color})
        return node, Constant(repeat(from_color)), Constant(repeat(to_color))

    def sample_map_color_in_selection_args(self):
        grid_node, selection_node = self.sample_matching_shape_args(Grid, Selection)
        target_colors = used_colors(self.target)
        from_color = self.sample_color(used_colors(grid_node()) - target_colors)
        to_color = self.sample_color(target_colors - {from_color})
        return (
            grid_node,
            selection_node,
            Constant(repeat(from_color)),
            Constant(repeat(to_color)),
        )

    def sample_set_selected_to_color_args(self):
        grid_node, selection_node = self.sample_matching_shape_args(Grid, Selection)
        # TODO: sample to_color higher prob for used_colors(target)
        color = self.sample_color(used_colors(self.target))
        return grid_node, selection_node, Constant(repeat(color))

    def sample_extract_args(self):
        # TODO: sample all, but same shape as target with less prob
        node = self.sample_node(
            self.nodes.with_type(Grid) - self.nodes.with_shape(shape(self.target))
        )
        # TODO: sample from_color only from used_colors(node)
        color = self.sample_color(used_colors(node()))
        return node, Constant(repeat(color))

    def sample_logic_args(self):
        # TODO: rely on take functions and use scalar grids instead of sequence
        sample_matching_shape_grids = self.sample_node(
            self.nodes.with_type(Grids)
            & self.nodes.with_length(2)
            & self.nodes.with_shape.matching_sequences
        )
        return (
            Function(vectorize(take_first), sample_matching_shape_grids),
            Function(vectorize(take_last), sample_matching_shape_grids),
        )

    def sample_select_color_args(self):
        node = self.sample_node(self.nodes.with_type(Grid))
        color = self.sample_color(used_colors(node()))
        return node, Constant(repeat(color))

    def sample_merge_selection_args(self):
        node = self.sample_node(
            self.nodes.with_type(Selections) & self.nodes.with_shape.matching_sequences
        )
        return (node,)

    def sample_split_args(self, height_segments=1, width_segments=1):
        # TODO: sample with higher prob when not target shape
        candidates = set(self.nodes.with_type(Grid))

        def nodes_with_splittable_dimension(nodes_with_dimension, num_segments):
            splittable_dimensions = {
                dimension
                for dimension in nodes_with_dimension.values
                if all(
                    element is not None and element % num_segments == 0
                    for element in dimension
                )
            }
            if len(splittable_dimensions) == 0:
                raise NoSample()
            return union(nodes_with_dimension(dim) for dim in splittable_dimensions)

        if height_segments > 1:
            candidates &= nodes_with_splittable_dimension(
                self.nodes.with_height, height_segments
            )
        if width_segments > 1:
            candidates &= nodes_with_splittable_dimension(
                self.nodes.with_width, width_segments
            )

        return (self.sample_node(candidates),)

    def sample_concatenate_top_bottom_args(self):
        # TODO: sample with higher prob when not target shape
        # TODO: sample with lower prob when concatentate same node
        candidates = self.nodes.with_type(Grid)
        top_node = self.sample_node(candidates)
        bottom_node = self.sample_node(
            candidates & self.nodes.with_width(width(top_node()))
        )
        return top_node, bottom_node

    def sample_concatenate_left_right_args(self):
        # TODO: sample with higher prob when not target shape
        # TODO: sample with lower prob when concatentate same node
        candidates = self.nodes.with_type(Grid)
        left_node = self.sample_node(candidates)
        right_node = self.sample_node(
            candidates & self.nodes.with_height(height(left_node()))
        )
        return left_node, right_node

    def sample_concatenate_top_to_bottom_args(self):
        # TODO: sample with higher prob when not target shape
        candidates = (
            self.nodes.with_type(Grids) & self.nodes.with_width.matching_sequences
        )
        return (self.sample_node(candidates),)

    def sample_concatenate_left_to_right_args(self):
        # TODO: sample with higher prob when not target shape
        candidates = (
            self.nodes.with_type(Grids) & self.nodes.with_height.matching_sequences
        )
        return (self.sample_node(candidates),)

    def sample_type_args(self, *types):
        if len(types) > 1:
            candidates = union(self.nodes.with_type(type_) for type_ in types)
        else:
            candidates = self.nodes.with_type(types[0])
        return (self.sample_node(candidates),)

    def sample_matching_selection_node(self, grid_node):
        return self.sample_node(
            self.nodes.with_type(Selection) & self.nodes.with_shape(shape(grid_node()))
        )

    def sample_matching_shape_args(self, *types, replace=True):
        if replace:
            num_required = {type_: 1 for type_ in types}
        else:
            num_required = Counter(types)

        candidates_by_type = [set() for _ in types]

        for shape_ in self.nodes.with_shape.values:
            nodes_for_shape = self.nodes.with_shape(shape_)
            nodes_by_type = [
                self.nodes.with_type(type_) & nodes_for_shape for type_ in types
            ]

            if all(
                len(nodes) >= num_required[type_]
                for type_, nodes in zip(types, nodes_by_type)
            ):
                for candidates, nodes in zip(candidates_by_type, nodes_by_type):
                    candidates |= nodes

        if any(len(candidates) == 0 for candidates in candidates_by_type):
            raise NoSample()

        sampled_nodes = []
        sampled_nodes.append(self.sample_node(candidates_by_type[0]))
        nodes_with_matching_shape = self.nodes.with_shape(shape(sampled_nodes[0]()))
        for candidates in candidates_by_type[1:]:
            candidates &= nodes_with_matching_shape
            if not replace:
                candidates -= set(sampled_nodes)
            sampled_nodes.append(self.sample_node(candidates))

        return tuple(sampled_nodes)

    def sample_node(self, nodes):
        nodes = list(nodes)
        if len(nodes) == 0:
            raise NoSample()

        def weight(node):
            return 1 / ((0.1 * node.usages) + (0.1 * node.depth) + 1)

        weights = [weight(node) for node in nodes]
        return _py_random.choices(nodes, weights=weights)[0]

    def sample_color(self, colors):
        colors = list(colors)
        if len(colors) == 0:
            raise NoSample()

        weights = [self.color_weights[color] for color in colors]
        return _py_random.choices(colors, weights=weights)[0]


def union(iterable):
    elements = list(iterable)
    if len(elements) == 0:
        return set()

    return set.union(*elements)


class NoSample(Exception):
    pass


_py_random = random.Random(0)
_np_random = np.random.RandomState(0)
