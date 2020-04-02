from itertools import repeat


class _Node:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)


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
    def __init__(self, value):
        super().__init__(value)
        self.value_sequence = repeat(value)

    def __call__(self, use_cache=True):
        """return color wrapped in iterator for use as arguments for vectorized operations"""
        return self.value_sequence
