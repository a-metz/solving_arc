import sys
import warnings
from itertools import product

import pytest

from . import function_sampling
from .function_sampling import *
from .node_collection import *

epsilon = sys.float_info.epsilon


@pytest.fixture
def example_source():
    return Vector([Grid.from_string("0 1"), Grid.from_string("0 1 0"), Grid.from_string("1 4")])


@pytest.fixture
def example_selection():
    return Vector(
        [Selection.from_string(". #"), Selection.from_string(". # ."), Selection.from_string("# .")]
    )


@pytest.fixture
def example_target():
    return Vector([Grid.from_string("0 2"), Grid.from_string("0 2 0"), Grid.from_string("2 4")])


@pytest.fixture
def initial_nodes(example_source):
    return {Constant(example_source)}


@pytest.fixture
def graph(example_source, example_target):
    return Graph(initial_nodes={Constant(example_source)}, target=example_target, max_expansions=10)


def test_graph_create(graph, initial_nodes):
    assert graph.nodes == initial_nodes


def test_graph_expand__once(graph, initial_nodes):
    graph.function_sampler.operation_probs = {map_color: 1.0}
    graph.expand()

    # expect one new node
    expanded_nodes = graph.nodes - initial_nodes
    assert len(expanded_nodes) == 1
    expanded_node = next(iter(expanded_nodes))

    # expect node node to be a function with inital nodes as argument
    assert isinstance(expanded_node, Function)
    assert set(expanded_node.args) > set(initial_nodes)


def test_graph_expand__max_expansions(initial_nodes, example_target):
    max_expansions = 10
    graph = Graph(initial_nodes, target=example_target, max_expansions=max_expansions)

    for _ in range(max_expansions):
        graph.expand()

    with pytest.raises(NoRemainingExpansions):
        graph.expand()


def test_graph_expand__find_target(example_source, example_target):
    source_node = Constant(example_source)
    graph = Graph({source_node}, target=example_target)

    graph.function_sampler.operation_probs = {map_color: 1.0}
    graph.function_sampler.color_probs = {Color(1): epsilon, Color(2): 1.0 - epsilon}
    solution = graph.expand()

    assert solution is None

    graph.function_sampler.color_probs = {Color(1): 1.0 - epsilon, Color(2): epsilon}
    solution = graph.expand()

    assert solution == Function(
        vectorize(map_color), source_node, Constant(repeat(Color(1))), Constant(repeat(Color(2)))
    )


@pytest.fixture
def all_args(example_source, example_selection):
    return {
        # scalar grid
        Constant(Vector([Grid.from_string("0 1"), Grid.from_string("0 1 2")])),
        # scalar selection
        Constant(Vector([Selection.from_string(". #"), Selection.from_string(". # #")])),
        # matching shape grids
        Constant(
            Vector(
                [
                    Grids([Grid.from_string("0 1"), Grid.from_string("1 1")]),
                    Grids([Grid.from_string("0 1 2"), Grid.from_string("1 1 1")]),
                ]
            )
        ),
        # matching shape selections
        Constant(
            Vector(
                [
                    Selections([Selection.from_string(". #"), Selection.from_string("# #")]),
                    Selections([Selection.from_string(". # #"), Selection.from_string("# # #")]),
                ]
            )
        ),
    }


def test_function_sampler__sample_matching_shape_nodes(all_args):
    graph = Graph(all_args)
    function_sampler = FunctionSampler(graph)

    for a_type, b_type in product([Grid, Grids, Selection, Selections], repeat=2):
        for _ in range(1000):
            a_node, b_node = function_sampler.sample_matching_shape_nodes(a_type, b_type)
            assert common_type(a_node()) == a_type
            assert common_type(b_node()) == b_type
            assert shape(a_node()) == shape(b_node())


def test_function_sampler__all_functions_smoketest(all_args, example_target):
    graph = Graph(all_args, target=example_target)
    function_sampler = FunctionSampler(graph)

    for operation in function_sampler.operation_probs.keys():
        sample_args = function_sampler.sample_args[operation]

        if sample_args is not None:
            try:
                args = sample_args()
                function = Function(vectorize(operation), *args)
                value = function()
            except Exception as exception:
                print("failed for operation: {}".format(operation.__name__))
                raise

            assert value is not None
