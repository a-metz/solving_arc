from warnings import warn

import pytest

from .evaluation import _evaluate, _get_tasks
from .loader import training_tasks, evaluation_tasks


@pytest.fixture
def expect_solve():
    return {
        "0520fde7",
        "0b148d64",
        # soon? "11852cab",
        "195ba7dc",
        # soon? "1b2d62fb",
        "1cf80156",
        "3428a4f5",
        "3c9b0459",
        "5d2a5c43",
        "6150a2bd",
        "67a3c6ac",
        "68b16354",
        "7468f01a",
        "74dd1130",
        # soon? "8d5021e8",
        "9dfd6313",
        "b1948b0a",
        "bf699163",
        "c8f0f002",
        "e98196ab",
        "ed36ccf7",
    }


@pytest.mark.slow
def test_regression(expect_solve):
    solved = set(_evaluate(_get_tasks(expect_solve), max_time=10))

    assert expect_solve == solved, "failed to solve: {}".format(
        ", ".join(sorted(expect_solve - solved))
    )


@pytest.mark.skip
def test_check_for_additional_solve(expect_solve):
    expect_no_solve = (set(training_tasks().keys()) | set(evaluation_tasks().keys())) - expect_solve

    additionally_solved = set(_evaluate(_get_tasks(expect_no_solve), max_time=10))

    if len(additionally_solved) > 0:
        warn("additionally solved: {}".format(", ".join(sorted(additionally_solved))))
