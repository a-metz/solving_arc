import logging

from .tree_search import *
from ..language import *

# logging.getLogger().setLevel(logging.DEBUG)


def test_solution():
    a = lambda x: x + "l"
    b = lambda x: x + "e"
    c = lambda x: x + "x"

    solution = Solution([a, b, c])
    assert solution("a") == "alex"


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

    assert solution is not None
    assert solution[0](source) == target


def test_solve_complex():
    source = Grid([[0, 0, 1], [2, 2, 2], [1, 0, 1]])
    target = Grid([[3, 0, 3]])

    solution = solve(source, target, max_depth=3)

    assert solution is not None
    assert solution(source) == target


def test_solve_and_transfer():
    source = Grid([[0, 0, 1], [2, 2, 2], [1, 0, 1]])
    target = Grid([[3, 0, 3]])

    solution = solve(source, target, max_depth=3)

    test = Grid([[1, 1, 0, 0], [2, 2, 2, 2], [1, 0, 0, 1]])
    assert solution(test) == Grid([[3, 3, 0, 3]])
