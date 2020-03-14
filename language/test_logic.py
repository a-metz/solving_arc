import pytest

from .grid import Grid
from .logic import *


@pytest.fixture
def example_grid():
    return Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def test_elementwise_operation__different_shapes():
    a = Grid([[1, 2]])
    b = Grid([[1, 2], [3, 4]])

    assert elementwise_equal_and(a, b) == None


def test_elementwise_equal_and():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 4]])

    assert elementwise_equal_and(a, b) == Grid([[0, 0], [0, 4]])


def test_elementwise_equal_and__inequal_nonzero_elements():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 5]])

    assert elementwise_equal_and(a, b) == None


def test_elementwise_equal_or():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 4]])

    assert elementwise_equal_or(a, b) == Grid([[0, 2], [3, 4]])


def test_elementwise_equal_or__inequal_nonzero_elements():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 5]])

    assert elementwise_equal_or(a, b) == None


def test_elementwise_xor():
    a = Grid([[0, 0], [3, 4]])
    b = Grid([[0, 2], [0, 4]])

    assert elementwise_xor(a, b) == Grid([[0, 2], [3, 0]])


def test_parameterize():
    args = [Grid([[0, 0, 1, 1]]), Grid([[0, 1, 0, 1]])]

    logic_functions = parameterize(args)

    assert len(logic_functions) == 3
    results = {func() for func in logic_functions}
    assert results == {Grid([[0, 0, 0, 1]]), Grid([[0, 1, 1, 1]]), Grid([[0, 1, 1, 0]])}


def test_parameterize__different_shapes():
    args = [Grid([[0, 1]]), Grid([[1, 0, 1]])]

    logic_functions = parameterize(args)

    assert len(logic_functions) == 0


def test_parameterize__wrong_number_of_arguments():
    args = [Grid([[0, 1]])]

    logic_functions = parameterize(args)

    assert len(logic_functions) == 0
