from collections import defaultdict


from ..language import *
from .vectorize import *
from .nodes import *


class NodeCollection(set):
    def __init__(self, nodes):
        super().__init__(nodes)
        self._by_type = defaultdict(set)
        self._by_shape = defaultdict(set)
        self._by_length = defaultdict(set)
        self._matching_shape_sequences = set()
        for node in nodes:
            self._process(node)

    def add(self, node):
        super().add(node)
        self._process(node)

    def _process(self, node):
        # sort by type
        type_ = common_type(node())
        if type_ is not None:
            self._by_type[type_].add(node)

            if type_ in {Grid, Selection}:
                # sort scalars by shape
                self._by_shape[shape(node())].add(node)

            if type_ in {Grids, Selections}:
                # sort sequences by shape
                shape_ = shape(node())
                if all([element is not None for element in shape_]):
                    self._by_shape[shape_].add(node)
                    self._matching_shape_sequences.add(node)

                # sort by sequence length
                lengths = {len(element) for element in node()}
                if len(lengths) == 1:
                    self._by_length[lengths.pop()].add(node)

    def with_type(self, type_):
        return self._by_type[type_]

    def with_shape(self, shape_):
        return self._by_shape[shape_]

    def shapes(self):
        return set(self._by_shape.keys())

    def with_length(self, length):
        return self._by_length[length]

    def matching_shape_sequences(self):
        return self._matching_shape_sequences


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


def common_type(argument_vector):
    types = {type(element) for element in argument_vector}
    if len(types) == 1:
        return types.pop()

    return None


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
