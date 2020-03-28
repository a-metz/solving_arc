from time import sleep

import pytest

from .timeout import *


@pytest.mark.slow
def test_timeout__short_running_completes():
    def short_running(value):
        sleep(0.1)
        return value

    result = timeout(1)(short_running)(42)

    assert result == 42


@pytest.mark.slow
def test_timeout__long_running_times_out():
    def long_running(value):
        sleep(10)
        return value

    result = timeout(1)(long_running)(42)

    assert result is None
