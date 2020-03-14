from ..language import *
from .kaggle import *


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
    assert results_string[0] == "0520fde7_0,|101|011| |000|000| |000|000|"
    assert results_string[1] == "0520fde7_1,|12|34| |56|78| |00|00|"
