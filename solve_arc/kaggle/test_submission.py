import pytest

from ..language.grid import Grid
from .submission import *


def test_format_grid():
    grid = Grid([[1, 2], [3, 4]])

    assert format_grid(grid) == "|12|34|"


def test_format_results():
    task_id = "0520fde7"
    # single attempt
    test_0_result = Grid([[1, 0, 1], [0, 1, 1]])
    # multiple attempts
    test_1_result = [Grid([[1, 2], [3, 4]]), Grid([[5, 6], [7, 8]])]
    results = [test_0_result, test_1_result]

    results_string = format_results(task_id, results)
    assert results_string[0] == "0520fde7_0,|101|011|"
    assert results_string[1] == "0520fde7_1,|12|34| |56|78|"


@pytest.mark.slow
def test_generate_submission_smoketest():
    generate_submission("solve_arc/kaggle/test_data", max_depth=3, max_time=10)

    submission = open("submission.csv", "r").readlines()
    assert submission[0] == "output_id,output\n"
    assert submission[1] == "0520fde7_0,|202|000|000|\n"
    assert submission[2] == "7c008303_0,|00|00|\n"  # default result because no solution found
