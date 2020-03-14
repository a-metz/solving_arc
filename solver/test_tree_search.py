import logging

from .tree_search import *
from ..language import *

# logging.getLogger().setLevel(logging.DEBUG)


def test_solve_nop():
    source = Grid([[1, 2, 3]])
    target = source

    solution = solve(source, target, max_depth=4)

    # one solution with no applied functions
    assert solution == []


def test_solve_no_solution_within_depth():
    source = Grid([[1, 2, 3]])
    target = Grid([[4, 5, 6]])

    solution = solve(source, target, max_depth=2)

    assert solution == None


def test_solve_simple_colorswap():
    source = Grid([[1, 2]])
    target = Grid([[2, 1]])

    solution = solve(source, target, max_depth=1)

    assert len(solution) > 0
    assert solution[0](source) == target


def test_solve_complex():
    source = Grid([[0, 0, 1], [2, 2, 2], [1, 0, 1]])
    target = Grid([[3, 0, 3]])

    solution = solve(source, target, max_depth=3)

    assert len(solution) == 3
