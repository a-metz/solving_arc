import numpy as np


class _Base:
    def __init__(self, state):
        self.state = np.array(state, copy=True)

        assert len(self.state.shape) == 2, "state needs to be 2d array"

    @classmethod
    def from_string(cls, string):
        lines = [line.strip() for line in string.splitlines() if len(line.strip()) > 0]
        elements = [[int(element) for element in line.split()] for line in lines]
        return cls(elements)

    def copy(self):
        return self.__class__(self.state)

    def enumerate(self):
        return np.ndenumerate(self.state)

    @property
    def shape(self):
        return self.state.shape

    def __getitem__(self, *args, **kwargs):
        substate = self.state.__getitem__(*args, **kwargs)

        if np.isscalar(substate):
            return substate

        # return new grid for nonscalar values
        return self.__class__(substate)

    def __hash__(self):
        # only consider state for hash
        return hash(self.state.tobytes())

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __str__(self):
        return "{}(<{}, {}>)".format(self.__class__.__name__, shape[0], shape[1])

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.state.tolist())


class Grid(_Base):
    def __init__(self, state):
        super().__init__(state)

        assert self.state.dtype.kind in ["i", "u"], "state datatype must be integral"

    @classmethod
    def empty(cls, shape):
        return cls(np.zeros(shape=shape, dtype=np.int))

    @classmethod
    def from_string(cls, string):
        elements = [[int(char) for char in line] for line in filtered_elements(string)]
        return cls(elements)

    def used_colors(self):
        """returns list of colors used in grid"""
        return np.unique(self.state)

    def __str__(self):
        return "\n".join([" ".join([str(char) for char in row]) for row in self.state])


class Selection(_Base):
    def __init__(self, state):
        super().__init__(state)

        assert self.state.dtype.kind == "b", "state datatype must be boolean"

    @classmethod
    def empty(cls, shape):
        return cls(np.zeros(shape=shape, dtype=np.bool))

    @classmethod
    def from_indices(cls, shape, indices):
        num_rows = shape[0]
        num_colums = shape[1]
        # assignment by indices can only be done on flat array (numpy limitation)
        flat_indices = np.dot(np.array(indices), np.array([num_colums, 1]))
        flat_state = np.zeros(shape=num_rows * num_colums, dtype=np.bool)
        flat_state[flat_indices] = True
        return Selection(flat_state.reshape(shape))

    @classmethod
    def from_string(cls, string):
        elements = [[char == "#" for char in line] for line in filtered_elements(string)]
        return cls(elements)

    def any(self):
        """returns whether any element is true in selection"""
        return np.any(self.state)

    def __str__(self):
        return "\n".join([" ".join(["#" if value else "." for value in row]) for row in self.state])


def filtered_elements(string):
    return (line.strip().split() for line in string.splitlines() if len(line.strip()) > 0)
