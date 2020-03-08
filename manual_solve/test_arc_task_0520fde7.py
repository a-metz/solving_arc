from ..utilities.arc_loader import train_and_test_subtasks

from ..language import *


def transform(grid):
    islands = extract_islands(grid, water=5)
    merged = elementwise_eand(*islands)
    return map_color(merged, 1, 2)


def test_manual_solve():
    for subtask in train_and_test_subtasks("0520fde7"):
        assert subtask.output == transform(subtask.input)
