import pytest

from ..utilities.arc_loader import train_and_test_subtasks
from ..language import *


def test_0520fde7(input_, expected):
    islands = extract_islands(input_, water=5)
    merged = elementwise_eand(*islands)
    result = switch_color(merged, 1, 2)
    assert result == expected


def test_0d3d703e(input_, expected):
    result = switch_color(input_, 3, 4)
    result = switch_color(result, 1, 5)
    result = switch_color(result, 2, 6)
    result = switch_color(result, 8, 9)
    assert result == expected


def test_1b2d62fb(input_, expected):
    islands = extract_islands(input_, water=1)
    merged = elementwise_eor(*islands)
    result = switch_color(merged, 0, 9)
    result = switch_color(result, 8, 9)
    assert result == expected


def test_3428a4f5(input_, expected):
    islands = extract_islands(input_, water=4)
    merged = elementwise_xor(*islands)
    result = switch_color(merged, 2, 3)


def test_1cf80156(input_, expected):
    islands = extract_islands(input_, water=0)
    (result,) = islands
    assert result == expected
