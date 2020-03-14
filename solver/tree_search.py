from itertools import chain
import logging

from ..language import *
from ..language.argument import extract_scalar, ArgumentError

logger = logging.getLogger(__name__)

MAX_DEPTH = 4

parameterizers = [extract_islands.parameterize, logic.parameterize, switch_color.parameterize]


def solve(source, target, max_depth):
    def solve_recursive(args, target, applied_functions):
        try:
            grid = extract_scalar(args)
            if grid == target:
                return applied_functions
        except ArgumentError:
            pass

        depth = len(applied_functions)
        if depth < max_depth:
            functions = chain.from_iterable(parameterize(args) for parameterize in parameterizers)
            for function in functions:
                result = function()

                logger.debug(format_partial(function, result, depth))
                if result is None:
                    continue

                solution = solve_recursive(result, target, applied_functions + [function])
                if solution is not None:
                    return solution

        return None

    return solve_recursive(source, target, applied_functions=[])


def format_partial(function, result, depth):
    """format partial applied function created with functools.partial"""

    indent = "  " * (depth + 1)
    args = ", ".join(repr(arg) for arg in function.args)
    keywords = ", ".join(
        ["{}={}".format(key, repr(value)) for key, value in function.keywords.items()]
    )
    return "{}{}({}, {}) = {}".format(indent, function.func.__name__, args, keywords, repr(result))
