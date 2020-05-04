from collections import defaultdict


from ..language import *
from .vectorize import *
from .nodes import *


class NodeCollection(set):
    def __init__(self, nodes):
        super().__init__(nodes)
        self._by_type = defaultdict(set)
        self._by_length = defaultdict(set)
        self.with_shape = _ByProperty(shape)
        self.with_height = _ByProperty(height)
        self.with_width = _ByProperty(width)
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

            self.with_shape.process(node, type_)
            self.with_height.process(node, type_)
            self.with_width.process(node, type_)

            if type_ in {Grids, Selections}:
                # sort by sequence length
                lengths = {len(element) for element in node()}
                if len(lengths) == 1:
                    self._by_length[lengths.pop()].add(node)

    def with_type(self, type_):
        return self._by_type[type_]

    def with_length(self, length):
        return self._by_length[length]


class _ByProperty:
    applicable_types = {Grid, Selection, Grids, Selections}
    sequence_types = {Grids, Selections}

    def __init__(self, get_property):
        self._get_property = get_property
        self._by_property = defaultdict(set)
        self.matching_sequences = set()

    def process(self, node, type_):
        if type_ in self.applicable_types:
            property_vector = self._get_property(node())
            self._by_property[property_vector].add(node)

            # when sequence does not match, property will be None
            # check for all sequences in property vector
            if type_ in self.sequence_types and all(
                [element is not None for element in property_vector]
            ):
                self.matching_sequences.add(node)

    def __call__(self, value):
        return self._by_property[value]

    @property
    def values(self):
        return self._by_property.keys()


def used_colors(grid_vector):
    """intersection of used colors in value tuple elements"""
    used_colors = (set(grid.used_colors()) for grid in grid_vector)
    return set.intersection(*used_colors)


def common_type(argument_vector):
    types = {type(element) for element in argument_vector}
    if len(types) == 1:
        return types.pop()

    return None


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
