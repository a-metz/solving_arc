from itertools import chain
from functools import partial
from collections import namedtuple
import logging

from ..language import *
from ..language.argument import extract_scalar, ArgumentError

logger = logging.getLogger(__name__)

MAX_DEPTH = 4

parameterizers = [extract_islands.parameterize, logic.parameterize, switch_color.parameterize]


Constraint = namedtuple("Constraint", ["source", "target"])


def solve(constraints, max_depth):
    sources, targets = zip(*constraints)

    def solve_recursive(arguments, depth):
        # no solution along this branch for at least one argument
        if not all(arguments):
            return None

        if is_solved(arguments):
            return Solution()

        if depth == max_depth:
            return None

        common_valid_functions = set.intersection(*[valid_functions(arg) for arg in arguments])
        for function in common_valid_functions:
            results = [function(arg) for arg in arguments]
            # logger.debug(format_function(function, results, depth))

            sub_solution = solve_recursive(results, depth + 1)
            # check if found solution
            if sub_solution is not None:
                return Solution.chain(function, sub_solution)

        return None

    def is_solved(arguments):
        try:
            # check if all arguments equal their target
            return all(extract_scalar(arg) == target for arg, target in zip(arguments, targets))
        except ArgumentError:
            return False

    return solve_recursive(sources, depth=0)


def valid_functions(argument):
    return set(chain.from_iterable(parameterize(argument) for parameterize in parameterizers))


class Solution(list):
    def __call__(self, arg):
        for function in self:
            arg = function(arg)
        return arg

    @classmethod
    def chain(cls, func, solution):
        return Solution([func] + solution)


def format_function(function, result, depth):
    if isinstance(function, partial):
        function_string = format_partial(function)
    else:
        function_string = function.__name__ + "()"

    indent = "    " * depth
    return "{}{} = {}".format(indent, function_string, repr(result))


def format_partial(function):
    """format partial applied function created with functools.partial"""

    positional_args = [repr(arg) for arg in function.args]
    keyword_args = ["{}={}".format(key, repr(value)) for key, value in function.keywords.items()]
    args = ", ".join(positional_args + keyword_args)

    return "{}({})".format(function.func.__name__, args)
