from itertools import repeat


class Function:
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
        return "Function({})".format(
            ", ".join([self.operation.__name__] + [repr(arg) for arg in self.args])
        )

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.operation) ^ hash(tuple(arg() for arg in self.args))


class Source:
    """cached value source"""

    def __init__(self, value):
        self.value = value

    def load(self, value):
        """replace value for transfer of program to different source"""
        self.value = value

    def __call__(self, use_cache=True):
        return self.value

    def __str__(self):
        return "source()"

    def __repr__(self):
        return "Source({})".format(repr(self.value))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.value)


class Constant:
    """cached value constant"""

    def __init__(self, scalar):
        self.scalar = scalar
        self.value = repeat(scalar)

    def __call__(self, use_cache=True):
        """return scalar wrapped in iterator for use as arguments for vectorized operations"""
        return self.value

    def __str__(self):
        return str(self.scalar)

    def __repr__(self):
        return "Constant({})".format(repr(self.value))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.scalar)
