from collections import defaultdict

from ..language import Grid, Mask


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

        # no solution found
        return None

    def scalars(self, type_):
        return self._scalars[type_]

    def sequences(self, type_):
        return self._sequences[type_]


def is_valid(node):
    return all(element is not None for element in node())


def is_scalar(node, type_):
    return all(isinstance(element, type_) for element in node())


def is_sequence(node, type_):
    return all(
        hasattr(elements, "__len__") and (isinstance(element, type_) for element in elements)
        for elements in node()
    )
