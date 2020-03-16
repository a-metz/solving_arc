import functools


class partial(functools.partial):
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        # assume sorted dict implementation
        return hash(self.func) ^ hash(tuple(self.args)) ^ hash(tuple(self.keywords.items()))
