from warnings import warn

import pytest

from .evaluation import _evaluate, _get_tasks
from .loader import training_tasks, evaluation_tasks
from .task_ids import SOLVED_TASK_IDS, REGRESSION_TASK_IDS


@pytest.fixture
def default_kwargs():
    return {
        "max_seconds_per_task": 20,
        "max_depth": 5,
        "max_usages": 20,
        "expand_batch_size": 10000,
    }


@pytest.mark.slow
def test_regression(default_kwargs):
    expect_solve = set(REGRESSION_TASK_IDS)

    unsolved = set(expect_solve)
    retries = 3
    while len(unsolved) > 0 and retries > 0:
        unsolved -= set(_evaluate(_get_tasks(unsolved), **default_kwargs))
        retries -= 1

    assert len(unsolved) == 0, "failed to solve: {}".format(", ".join(sorted(unsolved)))
