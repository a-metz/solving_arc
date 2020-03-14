from .hashable_partial import partial


def test_partial__inner_function_equality():
    function_a = lambda x: x
    function_b = lambda y: y

    assert partial(function_a) == partial(function_a)
    assert partial(function_a) != partial(function_b)


def test_partial__arguments_equality():
    function = lambda x, y: x + y

    # positional arguments
    assert partial(function, 1) == partial(function, 1)
    assert partial(function, 1) != partial(function, 2)

    # keyword arguments
    assert partial(function, y=1) == partial(function, y=1)
    assert partial(function, y=1) != partial(function, y=2)

    # inequality due to different argument type
    assert partial(function, 1, 2) != partial(function, x=1, y=2)
