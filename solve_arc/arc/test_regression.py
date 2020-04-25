from warnings import warn

import pytest

from .evaluation import _evaluate, _get_tasks
from .loader import training_tasks, evaluation_tasks
from .solved_tasks import SOLVED_TASK_IDS


@pytest.fixture
def expect_solve():
    return set(SOLVED_TASK_IDS)


@pytest.fixture
def default_kwargs():
    return {
        "max_seconds_per_task": 20,
        "max_search_depth": 10,
        "max_expansions_per_node": 20,
    }


@pytest.mark.slow
def test_regression(expect_solve, default_kwargs):
    solved = set(_evaluate(_get_tasks(expect_solve), **default_kwargs))

    assert expect_solve == solved, "failed to solve: {}".format(
        ", ".join(sorted(expect_solve - solved))
    )


@pytest.mark.skip
def test_check_for_additional_solve(expect_solve):
    expect_no_solve = (set(training_tasks().keys()) | set(evaluation_tasks().keys())) - expect_solve

    additionally_solved = set(_evaluate(_get_tasks(expect_no_solve), **default_kwargs))

    if len(additionally_solved) > 0:
        warn("additionally solved: {}".format(", ".join(sorted(additionally_solved))))
