import pytest
import sys

from . import function_sampling
from .function_sampling import *

epsilon = sys.float_info.epsilon


@pytest.fixture
def example_source():
    return Vector([Grid.from_string("0 1"), Grid.from_string("0 1 0"), Grid.from_string("1 4")])


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
    graph.expand()

    # expect one new node
    expanded_nodes = graph.nodes - initial_nodes
    assert len(expanded_nodes) == 1
    expanded_node = next(iter(expanded_nodes))

    # expect node node to be a function with inital nodes as argument
    assert isinstance(expanded_node, Function)
    assert set(expanded_node.args) > set(initial_nodes)


def test_graph_expand__max_expansions(initial_nodes):
    max_expansions = 10
    graph = Graph(initial_nodes, max_expansions)

    for _ in range(max_expansions):
        graph.expand()

    with pytest.raises(NoRemainingExpansions):
        graph.expand()


def test_graph_expand__find_target(example_source, example_target):
    source_node = Constant(example_source)
    graph = Graph({source_node}, target=example_target)

    function_sampling.operation_probs = {map_color: 1.0}
    function_sampling.color_probs = {Color(1): epsilon, Color(2): 1.0 - epsilon}
    solution = graph.expand()

    assert solution is None

    function_sampling.color_probs = {Color(1): 1.0 - epsilon, Color(2): epsilon}
    solution = graph.expand()

    assert solution == Function(
        vectorize(map_color), source_node, Constant(repeat(Color(1))), Constant(repeat(Color(2)))
    )


def test_generate_functions_smoketest(example_source):
    graph = Graph({Constant(example_source)})

    for operation in operation_probs.keys():
        Function(vectorize(operation), *generate_args[operation](graph))
