from .nodes import *


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

    arg_a = Constant(None)
    arg_b = Constant(None)
    function = Function(add_second_times_three, arg_a, arg_b)
    # modify values after creating function to check lazy evaluation
    arg_a.value = 2
    arg_b.value = 5

    assert function() == 2 + (3 * 5)


def test_function__evaluation_of_chained_function():
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    arg_a = Constant(2)
    arg_b = Constant(3)
    arg_c = Constant(5)
    function = Function(add, arg_a, Function(multiply, arg_b, arg_c))

    assert function() == 2 + (3 * 5)


def test_constant__hash():
    assert hash(Constant(0)) != hash(Constant(1))

    # stress it a bit as function wrappers can also coincidentally have the same hash
    for i in range(10):
        assert hash(Constant(i)) == hash(Constant(i))


def test_function__hash_equality():
    def func(*args):
        pass

    arg = Constant(0)

    # single function
    assert hash(Function(func)) == hash(Function(func))
    assert hash(Function(func, arg)) == hash(Function(func, arg))
    assert hash(Function(func, arg)) == hash(Function(func, arg))


def test_function__hash_inequality():
    def func_a(*args):
        pass

    def func_b(*args):
        pass

    arg_a = Constant(0)
    arg_b = Constant(1)

    assert hash(Function(func_a)) != hash(Function(func_b))
    assert hash(Function(func_a, arg_a)) != hash(Function(func_b, arg_b))
    assert hash(Function(func_a, arg_a, arg_b)) != hash(Function(func_b, arg_b, arg_a))


def test_function__hash_of_chained_functions():
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    arg_a = Constant(2)
    arg_b = Constant(3)
    arg_c = Constant(5)
    reference = Function(add, arg_a, Function(multiply, arg_b, arg_c))

    # same function instantiated twice
    assert hash(Function(add, arg_a, Function(multiply, arg_b, arg_c))) == hash(reference)

    # different inner function
    assert hash(Function(add, arg_a, Function(add, arg_b, arg_c))) != hash(reference)

    # different inner value
    assert hash(Function(add, arg_a, Function(multiply, arg_a, arg_c))) != hash(reference)

    # different inner function but same resulting value
    arg_d = Constant(1)
    arg_e = Constant(15)
    assert hash(Function(add, arg_a, Function(multiply, arg_d, arg_e))) == hash(reference)
