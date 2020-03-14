from itertools import chain
from functools import partial
import logging

from ..language import *
from ..language.argument import extract_scalar, ArgumentError

logger = logging.getLogger(__name__)

MAX_DEPTH = 4

parameterizers = [extract_islands.parameterize, logic.parameterize, switch_color.parameterize]


class Solution(list):
    def __call__(self, arg):
        for function in self:
            arg = function(arg)
        return arg

    @classmethod
    def chain(cls, func, solution):
        return Solution([func] + solution)


def solve(source, target, max_depth):
    def solve_recursive(argument, depth):
        # no solution
        if argument is None:
            return None

        # check if solved
        try:
            grid = extract_scalar(argument)
            if grid == target:
                return Solution()
        except ArgumentError:
            pass

        if depth < max_depth:
            functions = [parameterize(argument) for parameterize in parameterizers]
            for function in chain.from_iterable(functions):
                result = function(argument)
                logger.debug(format_function(function, result, depth))

                sub_solution = solve_recursive(result, depth + 1)
                # check if found solution
                if sub_solution is not None:
                    return Solution.chain(function, sub_solution)

        return None

    return solve_recursive(source, depth=0)


def format_function(function, result, depth):
    indent = "  " * (depth + 1)

    if isinstance(function, partial):
        return format_partial(function, result, indent)

    return "{}{}() = {}".format(indent, function.__name__, repr(result))


def format_partial(function, result, indent):
    """format partial applied function created with functools.partial"""

    positional_args = [repr(arg) for arg in function.args]
    keyword_args = ["{}={}".format(key, repr(value)) for key, value in function.keywords.items()]
    args = ", ".join(positional_args + keyword_args)

    return "{}{}({}) = {}".format(indent, function.func.__name__, args, repr(result))
