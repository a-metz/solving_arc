class _Node:
    def __init__(self):
        self.usages = 0

    def __call__(self, use_cache=True):
        raise NotImplementedError()

    @property
    def depth(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        # allow equality between subclasses for uniqueness in sets
        return isinstance(other, _Node) and hash(self) == hash(other)

    def __hash__(self):
        raise NotImplementedError()


# TODO: nicer interface for caching switch i.e. a recursive clear_cache() function (?) -> but may not invalidate hash!
class Function(_Node):
    """cached partial application"""

    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation
        self.args = args

        for arg in self.args:
            arg.usages += 1

    def __call__(self, use_cache=True):
        """evaluate function with evaluated args, use cached values if possible and use_cache is True"""
        if not (use_cache and hasattr(self, "value")):
            args = [arg(use_cache) for arg in self.args]
            self.value = self.operation(*args)

        return self.value

    @property
    def depth(self):
        if not hasattr(self, "_depth"):
            self._depth = 1 + max(arg.depth for arg in self.args)

        return self._depth

    def __str__(self):
        return "{}({})".format(self.operation.__name__, ", ".join(str(arg) for arg in self.args))

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join([self.operation.__name__] + [repr(arg) for arg in self.args]),
        )

    def __hash__(self):
        # alternative: hash(self.operation) ^ hash(tuple(arg() for arg in self.args))
        # creates more functions with equal value, but avoids evaluating same callable and args mutiple times
        return hash(self())


class Constant(_Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __call__(self, use_cache=True):
        return self.value

    @property
    def depth(self):
        return 0

    def __str__(self):
        return "{}".format(str(self.value))

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(self.value))

    def __hash__(self):
        return hash(self.value)
