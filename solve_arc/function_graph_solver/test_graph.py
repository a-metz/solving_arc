from .graph import *


def test_function__lazy_evaluation_and_caching():
    class CountCalls:
        def __init__(self):
            self.call_count = 0

        def __call__(self):
            self.call_count += 1
            return 42

    callable_ = CountCalls()
    function = Function(callable_)

    # expect lazy evaluation
    assert callable_.call_count == 0
    assert function() == 42
    assert callable_.call_count == 1

    # expect returning of cached result
    assert function() == 42
    assert callable_.call_count == 1

    # expect reevaluting result
    assert function(use_cache=False) == 42
    assert callable_.call_count == 2


def test_function__lazy_evaluation_with_multiple_arguments():
    def add_second_times_three(a, b):
        return a + (3 * b)

    arg_1 = Constant(0)
    arg_2 = Constant(0)
    function = Function(add_second_times_three, arg_1, arg_2)

    # modify constant value after creating function to check lazy evaluation
    arg_1.value = 2
    arg_2.value = 5
    assert function() == 2 + (3 * 5)
