import pytest

from .arguments import *
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


@pytest.fixture
def selection_a():
    return Selection([[False, False], [True, True]])


@pytest.fixture
def selection_b():
    return Selection([[False, True], [False, True]])


def test_selection_elementwise_and(selection_a, selection_b):
    expected = Selection([[False, False], [False, True]])

    assert selection_elementwise_and(selection_a, selection_b) == expected


def test_selection_elementwise_or(selection_a, selection_b):
    expected = Selection([[False, True], [True, True]])

    assert selection_elementwise_or(selection_a, selection_b) == expected


def test_selection_elementwise_xor(selection_a, selection_b):
    expected = Selection([[False, True], [True, False]])

    assert selection_elementwise_xor(selection_a, selection_b) == expected


def test_selection_elementwise_eq(selection_a, selection_b):
    expected = Selection([[True, False], [False, True]])

    assert selection_elementwise_eq(selection_a, selection_b) == expected


def test_selection_elementwise_not():
    selection = Selection([[True, False]])

    assert selection_elementwise_not(selection) == Selection([[False, True]])
