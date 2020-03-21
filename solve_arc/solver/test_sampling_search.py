import logging

import pytest

from .sampling_search import *
from ..language import *

# logging.getLogger().setLevel(logging.DEBUG)


def test_solve__nop():
    source = Grid([[1, 2, 3]])
    target = source
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=4)

    # identity
    assert solution is not None
    test = Grid([[4, 5, 6]])
    assert solution(test) == test


def test_solve__no_solution_within_depth():
    source = Grid([[1, 2, 3]])
    target = Grid([[4, 5, 6]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=2)

    assert solution is None


def test_solve__single_colorswap():
    source = Grid([[1, 2, 2]])
    target = Grid([[2, 1, 1]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=1)

    assert solution is not None
    assert solution(source) == target
    assert solution(Grid([[1, 1, 2]])) == Grid([[2, 2, 1]])


@pytest.mark.skip
def test_solve__single_xor():
    source = (Grid([[1, 0, 0]]), Grid([[1, 1, 0]]))
    target = Grid([[0, 1, 0]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=1)

    assert solution is not None
    assert solution(source) == target
    assert solution((Grid([[1, 0, 1]]), Grid([[1, 1, 0]]))) == Grid([[0, 1, 1]])


def test_solve__single_colorswap__multiple_contraints():
    constraints = [
        Constraint(source=Grid([[1, 2, 2]]), target=Grid([[2, 1, 1]])),
        Constraint(source=Grid([[1, 2, 1]]), target=Grid([[2, 1, 2]])),
    ]

    solution = solve(constraints, max_depth=1)

    assert solution is not None
    assert solution(Grid([[1, 1, 2]])) == Grid([[2, 2, 1]])


@pytest.mark.skip
def test_solve__single_xor__multiple_contraints():
    constraints = [
        Constraint(source=(Grid([[1, 0, 0]]), Grid([[1, 1, 0]])), target=Grid([[0, 1, 0]])),
        Constraint(source=(Grid([[0, 1, 1]]), Grid([[1, 1, 0]])), target=Grid([[1, 0, 1]])),
    ]

    solution = solve(constraints, max_depth=1)

    assert solution is not None
    assert solution((Grid([[1, 0, 1]]), Grid([[1, 1, 0]]))) == Grid([[0, 1, 1]])


@pytest.mark.skip
def test_solve__complex():
    source = Grid([[0, 0, 1], [2, 2, 2], [1, 0, 1]])
    target = Grid([[3, 0, 3]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, max_depth=3)

    assert solution is not None
    assert solution(Grid([[1, 1, 0, 0], [2, 2, 2, 2], [1, 0, 0, 1]])) == Grid([[3, 3, 0, 3]])


@pytest.mark.skip
def test_solve__complex__multiple_constraints():
    # undefined / no color swap
    constraint_1 = Constraint(source=Grid([[1, 0], [2, 2], [1, 0]]), target=Grid([[0, 0]]))

    # undefined logical operation (or|xor)
    constraint_2 = Constraint(source=Grid([[1, 0], [2, 2], [0, 0]]), target=Grid([[3, 0]]))

    solution = solve([constraint_1, constraint_2], max_depth=3)

    test = Grid([[1, 1], [2, 2], [1, 0]])
    print(solution)
    assert solution(test) == Grid([[0, 3]])
