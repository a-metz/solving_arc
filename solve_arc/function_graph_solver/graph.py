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


class _Node:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def operation_count():
        """ dict of operation: count in """
        return {}


class Function(_Node):
    """cached partial application"""

    def __init__(self, operation, *args):
        self.operation = operation
        self.args = args

    def __call__(self, use_cache=True):
        """evaluate function with evaluated args, use cached values if possible and use_cache is True"""
        if not (use_cache and hasattr(self, "value")):
            args = [arg(use_cache) for arg in self.args]
            self.value = self.operation(*args)

        return self.value

    def __str__(self):
        return "{}({})".format(self.operation.__name__, ", ".join(str(arg) for arg in self.args))

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join([self.operation.__name__] + [repr(arg) for arg in self.args]),
        )

    def __hash__(self):
        return hash(self.operation) ^ hash(tuple(arg() for arg in self.args))


class _Value(_Node):
    def __init__(self, value):
        self.value = value

    def __call__(self, use_cache=True):
        return self.value

    def __str__(self):
        return "{}".format(str(self.value))

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(self.value))

    def __hash__(self):
        return hash(self.value)


class Source(_Value):
    @classmethod
    def from_scalar(cls, scalar):  # TODO: scalar has a different meaning
        return cls((scalar,))

    def load(self, value):
        """replace value for transfer of program to different inputs"""
        self.value = value

    def __str__(self):
        # do not output of grid as that would clutter the output
        return "{}".format(self.__class__.__name__.lower())


class Constant(_Value):
    """endlessly iterate over value so instance can be used as argument for vectorized functions"""

    def __iter__(self):
        return self

    def __next__(self):
        return self.value

    def __call__(self, use_cache=True):
        return self
