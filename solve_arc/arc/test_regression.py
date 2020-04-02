from warnings import warn

import pytest

from .evaluation import _evaluate, _get_tasks
from .loader import training_tasks, evaluation_tasks
from .solved_tasks import SOLVED_TASK_IDS


@pytest.fixture
def expect_solve():
    return SOLVED_TASK_IDS


@pytest.mark.slow
def test_regression(expect_solve):
    solved = set(_evaluate(_get_tasks(expect_solve), max_time_per_task=10))

    assert expect_solve == solved, "failed to solve: {}".format(
        ", ".join(sorted(expect_solve - solved))
    )


@pytest.mark.skip
def test_check_for_additional_solve(expect_solve):
    expect_no_solve = (set(training_tasks().keys()) | set(evaluation_tasks().keys())) - expect_solve

    additionally_solved = set(_evaluate(_get_tasks(expect_no_solve), max_time_per_task=10))

    if len(additionally_solved) > 0:
        warn("additionally solved: {}".format(", ".join(sorted(additionally_solved))))
