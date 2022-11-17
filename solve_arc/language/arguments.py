import numpy as np
from enum import IntEnum


class Color(IntEnum):
    BLACK = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    GRAY = 5
    PINK = 6
    ORANGE = 7
    AZURE = 8
    CRIMSON = 9


# TODO: inherit from numpy array (?)
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

    @property
    def width(self):
        return self.state.shape[1]

    @property
    def height(self):
        return self.state.shape[0]

    def __getitem__(self, *args, **kwargs):
        substate = self.state.__getitem__(*args, **kwargs)

        if np.isscalar(substate):
            return substate

        # return new grid for nonscalar values
        return self.__class__(substate)

    def __hash__(self):
        # only consider state for hash
        return hash(self.state.shape) ^ hash(self.state.tobytes())

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __str__(self, str_element=str):
        return "\n".join(
            [" ".join([str_element(element) for element in row]) for row in self.state]
        )

    def __repr__(self):
        return "{}(<{}, {}>)".format(self.__class__.__name__, self.shape[0], self.shape[1])


class Grid(_Base):
    """ main representation of pixel grids for arc dataset inputs and outputs """

    def __init__(self, state):
        super().__init__(state)

        assert self.state.dtype.kind in ["i", "u"], "state datatype must be integral"

    @classmethod
    def empty(cls, shape):
        return cls(np.zeros(shape=shape, dtype=int))

    @classmethod
    def filled(cls, shape, color):
        return cls(np.full(shape=shape, fill_value=color, dtype=int))

    @classmethod
    def from_string(cls, string):
        elements = [[int(char) for char in line] for line in filtered_elements(string)]
        return cls(elements)

    def used_colors(self):
        """returns tuple of colors used in grid"""
        return tuple(np.unique(self.state))


class Selection(_Base):
    """ representation of boolean masks for intermediate selections """

    def __init__(self, state):
        super().__init__(state)

        assert self.state.dtype.kind == "b", "state datatype must be boolean"

    @classmethod
    def empty(cls, shape):
        return cls(np.zeros(shape=shape, dtype=bool))

    @classmethod
    def from_indices(cls, shape, indices):
        num_rows = shape[0]
        num_colums = shape[1]
        # assignment by indices can only be done on flat array (numpy limitation)
        flat_indices = np.dot(np.array(indices), np.array([num_colums, 1]))
        flat_state = np.zeros(shape=num_rows * num_colums, dtype=bool)
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
        return super().__str__(str_element=lambda element: "#" if element else ".")


def filtered_elements(string):
    return (line.strip().split() for line in string.splitlines() if len(line.strip()) > 0)


class _Sequence(tuple):
    """ base class for sequences of grids / selections for operations resulting in mutiple values """

    def append(self, element):
        return self.__class__(self + (element,))

    def apply(self, func, *args):
        return self.__class__(func(element, *args) for element in self)

    @property
    def shape(self):
        """ shape of elements in sequence if identical, else None"""
        shapes = {element.shape for element in self}
        if len(shapes) != 1:
            return None

        return shapes.pop()

    @property
    def height(self):
        """ height of elements in sequence if identical, else None"""
        heights = {element.height for element in self}
        if len(heights) != 1:
            return None

        return heights.pop()

    @property
    def width(self):
        """ width of elements in sequence if identical, else None"""
        widths = {element.width for element in self}
        if len(widths) != 1:
            return None

        return widths.pop()

    def __str__(self):
        return "\n---\n".join(str(element) for element in self)

    def __repr__(self):
        return "{}([{}])".format(
            self.__class__.__name__, ", ".join(repr(element) for element in self)
        )


class Grids(_Sequence):
    pass


class Selections(_Sequence):
    pass
