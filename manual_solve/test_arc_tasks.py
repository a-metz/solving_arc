import pytest

from ..utilities.arc_loader import train_and_test_subtasks
from ..language import *


def test_0520fde7(input_, expected):
    islands = extract_islands(input_, water=5)
    merged = elementwise_eand(*islands)
    result = switch_color(merged, 1, 2)
    assert result == expected
