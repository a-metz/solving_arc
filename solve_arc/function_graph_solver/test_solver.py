import logging

import pytest

from ..language import *
from .solver import *


@pytest.fixture(params=["full", "sampling"])
def search_strategy(request):
    return request.param


# basic cases:


def test_solve__nop(search_strategy):
    source = Grid([[1, 2, 3]])
    target = source
    constraints = [Constraint(source, target)]

    solution = solve(constraints, search_strategy, max_depth=4)

    # identity
    assert solution is not None
    test = Grid([[4, 5, 6]])
    assert solution(test) == test


def test_solve__no_solution_within_depth(search_strategy):
    source = Grid([[1, 2, 3]])
    target = Grid([[4, 5, 6]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, search_strategy, max_depth=2)

    assert solution is None


# some depth 1 solution cases:


def test_solve__single_colorswap(search_strategy):
    source = Grid([[1, 2, 2]])
    target = Grid([[2, 1, 1]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, search_strategy, max_depth=1)

    assert solution is not None
    assert solution(source) == target
    assert solution(Grid([[1, 1, 2]])) == Grid([[2, 2, 1]])


def test_solve__single_xor(search_strategy):
    source = Grids([Grid([[1, 0, 0]]), Grid([[1, 1, 0]])])
    target = Grid([[0, 1, 0]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, search_strategy, max_depth=2)

    assert solution is not None
    assert solution(source) == target
    assert solution((Grid([[1, 0, 1]]), Grid([[1, 1, 0]]))) == Grid([[0, 1, 1]])


def test_solve__single_flip(search_strategy):
    source = Grid([[1, 2], [3, 4]])
    target = Grid([[2, 1], [4, 3]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, search_strategy, max_depth=1)

    assert solution is not None
    assert solution(source) == target
    assert solution(target) == source


def test_solve__single_concatenation(search_strategy):
    source = Grid([[1, 2]])
    target = Grid([[1, 2], [1, 2]])
    constraints = [Constraint(source, target)]

    solution = solve(constraints, search_strategy, max_depth=1)

    assert solution is not None
    assert solution(source) == target


def test_solve__single_colorswap__multiple_contraints(search_strategy):
    constraints = [
        Constraint(source=Grid([[1, 2, 2]]), target=Grid([[2, 1, 1]])),
        Constraint(source=Grid([[1, 2, 1]]), target=Grid([[2, 1, 2]])),
    ]

    solution = solve(constraints, search_strategy, max_depth=1)

    assert solution is not None
    for source, target in constraints:
        assert solution(source) == target
    assert solution(Grid([[1, 1, 2]])) == Grid([[2, 2, 1]])


def test_solve__single_xor__multiple_contraints(search_strategy):
    constraints = [
        Constraint(
            source=Grids([Grid([[1, 0, 0]]), Grid([[1, 1, 0]])]),
            target=Grid([[0, 1, 0]]),
        ),
        Constraint(
            source=Grids([Grid([[0, 1, 1]]), Grid([[1, 1, 0]])]),
            target=Grid([[1, 0, 1]]),
        ),
    ]

    solution = solve(constraints, search_strategy, max_depth=2)

    assert solution is not None
    for source, target in constraints:
        assert solution(source) == target
    assert solution((Grid([[1, 0, 1]]), Grid([[1, 1, 0]]))) == Grid([[0, 1, 1]])


# some solution cases:


def test_solve__select_color_and_extract_selected_area__multiple_contraints(
    search_strategy,
):
    constraints = [
        Constraint(source=Grid([[1, 2, 1]]), target=Grid([[2]])),
        Constraint(source=Grid([[2, 2, 1]]), target=Grid([[2, 2]])),
    ]

    solution = solve(constraints, search_strategy, max_depth=2)

    assert solution is not None
    for source, target in constraints:
        assert solution(source) == target
    assert solution(Grid([[1, 2, 2]])) == Grid([[2, 2]])


@pytest.mark.skip
def test_solve__complex__multiple_constraints(search_strategy):
    constraints = [
        # undefined / no color swap
        Constraint(source=Grid([[1, 0], [2, 2], [1, 1]]), target=Grid([[0, 3]])),
        # undefined logical operation (or|xor)
        Constraint(source=Grid([[1, 0], [2, 2], [0, 0]]), target=Grid([[3, 0]])),
    ]

    solution = solve(constraints, search_strategy, max_depth=3)

    assert solution is not None
    for source, target in constraints:
        assert solution(source) == target
    assert solution(Grid([[1, 1], [2, 2], [1, 0]])) == Grid([[0, 3]])


def test_solve__split_and_get_first__multiple_constraints(search_strategy):
    constraints = [
        Constraint(source=Grid([[1, 2], [3, 4]]), target=Grid([[1, 2]])),
        Constraint(source=Grid([[3, 4, 5], [6, 7, 8]]), target=Grid([[3, 4, 5]])),
    ]

    solution = solve(constraints, search_strategy, max_depth=2)

    assert solution is not None
    for source, target in constraints:
        assert solution(source) == target
