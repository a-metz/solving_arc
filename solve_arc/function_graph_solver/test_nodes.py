import pytest

from .nodes import *


def test_function__lazy_evaluation_and_caching():
    class CountCalls:
        def __init__(self):
            self.call_count = 0

        def __call__(self):
            self.call_count += 1
            return 42

    operation = CountCalls()
    function = Function(operation)

    # expect lazy evaluation
    assert operation.call_count == 0
    assert function() == 42
    assert operation.call_count == 1

    # expect returning of cached result
    assert function() == 42
    assert operation.call_count == 1

    # expect reevaluting result
    assert function(use_cache=False) == 42
    assert operation.call_count == 2


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


def test_function__hash():
    def func_a():
        return 42

    def func_b():
        return 0

    arg = Constant(42)

    # check hash equality when result is equal
    reference = Function(func_a)
    assert hash(Function(func_a)) == hash(reference)
    assert hash(Function(func_b)) != hash(reference)

    # also between constant and function
    assert hash(arg) == hash(reference)


def test_constant__equality():
    assert Constant(0) != Constant(1)

    # stress it a bit as function wrappers can also coincidentally have the same hash
    for i in range(10):
        assert Constant(i) == Constant(i)


def test_function__equality():
    def func_a():
        return 42

    def func_b():
        return 0

    arg = Constant(42)

    # check equality when result is equal
    reference = Function(func_a)
    assert Function(func_a) == reference
    assert Function(func_b) != reference
    assert Function(arg) == reference

    # also between constant and function
    assert arg == reference


@pytest.mark.skip("only valid when using hash calculation based on callable and argument values")
def test_function__hash_equality():
    def func(*args):
        pass

    arg = Constant(0)

    # single function
    assert hash(Function(func)) == hash(Function(func))
    assert hash(Function(func, arg)) == hash(Function(func, arg))
    assert hash(Function(func, arg)) == hash(Function(func, arg))


@pytest.mark.skip("only valid when using hash calculation based on callable and argument values")
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


@pytest.mark.skip("only valid when using hash calculation based on callable and argument values")
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
