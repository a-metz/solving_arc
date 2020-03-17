import logging

import pytest

from .sampling_search import *
from ..language import *

# logging.getLogger().setLevel(logging.DEBUG)


def test_solve_nop():
    source = Grid([[1, 2, 3]])
    target = source
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=4)

    # identity
    test = Grid([[4, 5, 6]])
    assert solution(test) == test


def test_solve_no_solution_within_depth():
    source = Grid([[1, 2, 3]])
    target = Grid([[4, 5, 6]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=2)

    assert solution == None


def test_solve_simple_colorswap():
    source = Grid([[1, 2]])
    target = Grid([[2, 1]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=1)

    assert solution is not None
    assert solution(source) == target


def test_solve_complex():
    source = Grid([[0, 0, 1], [2, 2, 2], [1, 0, 1]])
    target = Grid([[3, 0, 3]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=3)

    assert solution is not None
    assert solution(source) == target


def test_solve_and_transfer():
    source = Grid([[0, 0, 1], [2, 2, 2], [1, 0, 1]])
    target = Grid([[3, 0, 3]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=3)

    test = Grid([[1, 1, 0, 0], [2, 2, 2, 2], [1, 0, 0, 1]])
    assert solution(test) == Grid([[3, 3, 0, 3]])


@pytest.mark.skip
def test_solve_multiple_constraints_and_transfer():
    # undefined / no color swap
    constraint_1 = Constraint(source=Grid([[1, 0], [2, 2], [1, 0]]), target=Grid([[0, 0]]))

    # undefined logical operation (or|xor)
    constraint_2 = Constraint(source=Grid([[1, 0], [2, 2], [0, 0]]), target=Grid([[3, 0]]))

    solution = solve([constraint_1, constraint_2], max_depth=3)

    test = Grid([[1, 1], [2, 2], [1, 0]])
    print(solution)
    assert solution(test) == Grid([[0, 3]])
