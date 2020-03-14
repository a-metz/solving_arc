from itertools import chain
import functools
import logging

from ..language import *
from ..language.argument import extract_scalar, ArgumentError

logger = logging.getLogger(__name__)

MAX_DEPTH = 4

parameterizers = [extract_islands.parameterize, logic.parameterize, switch_color.parameterize]


def solve(source, target, max_depth):
    def solve_recursive(argument, target, applied_functions):
        try:
            grid = extract_scalar(argument)
            if grid == target:
                return applied_functions
        except ArgumentError:
            pass

        depth = len(applied_functions)
        if depth < max_depth:
            functions = chain.from_iterable(
                parameterize(argument) for parameterize in parameterizers
            )
            for function in functions:
                result = function(argument)

                logger.debug(format_function(function, result, depth))

                # no result, end this branch
                if result is None:
                    continue

                solution = solve_recursive(result, target, applied_functions + [function])
                if solution is not None:
                    return solution

        return None

    return solve_recursive(source, target, applied_functions=[])


def format_function(function, result, depth):
    indent = "  " * (depth + 1)

    if isinstance(function, functools.partial):
        return format_partial(function, result, indent)

    return "{}{}() = {}".format(indent, function.__name__, repr(result))


def format_partial(function, result, indent):
    """format partial applied function created with functools.partial"""

    positional_args = [repr(arg) for arg in function.args]
    keyword_args = ["{}={}".format(key, repr(value)) for key, value in function.keywords.items()]
    args = ", ".join(positional_args + keyword_args)

    return "{}{}({}) = {}".format(indent, function.func.__name__, args, repr(result))
