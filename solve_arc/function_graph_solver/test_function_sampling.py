import sys
import warnings
from itertools import product

import pytest

from . import function_sampling
from .function_sampling import *
from .node_collection import *

epsilon = sys.float_info.epsilon


def test_graph_step__once():
    source = Vector([Grid.from_string("1 2 3 4 5")])
    target = Vector([Grid.from_string("6 7 8 9 0")])
    initial_nodes = {Constant(source)}
    graph = Graph(initial_nodes, target, max_steps=1)
    graph.function_sampler.operation_probs = {map_color: 1.0}
    graph.solve()

    # expect one new node
    created_nodes = graph.nodes - initial_nodes
    assert len(created_nodes) == 1
    created_node = next(iter(created_nodes))

    # expect node node to be a function with inital nodes as argument
    assert isinstance(created_node, Function)
    assert set(created_node.args) > set(initial_nodes)


def test_graph_step__max_steps():
    source = Vector([Grid.from_string("1 2 3 4 5")])
    target = Vector([Grid.from_string("6 7 8 9 0")])
    initial_nodes = {Constant(source)}
    graph = Graph({Constant(source)}, target, max_steps=3)

    graph.function_sampler.operation_probs = {map_color: 1.0}
    graph.solve()

    created_nodes = graph.nodes - initial_nodes
    assert len(created_nodes) == 3


def test_graph_solve__find_target():
    source = Vector([Grid.from_string("0 1"), Grid.from_string("3 1 4")])
    target = Vector([Grid.from_string("0 2"), Grid.from_string("3 2 4")])
    initial_nodes = {Constant(source)}
    graph = Graph(initial_nodes, target, max_depth=1, max_steps=10)

    graph.function_sampler.operation_probs = {rotate_90: 1.0}
    solution = graph.solve()

    assert solution is None

    graph.function_sampler.operation_probs = {map_color: 1.0}
    solution = graph.solve()

    assert solution == Function(
        vectorize(map_color),
        Constant(source),
        Constant(repeat(Color(1))),
        Constant(repeat(Color(2))),
    )


@pytest.fixture
def all_args():
    return {
        # scalar grid
        Constant(Vector([Grid.from_string("0 1"), Grid.from_string("0 1 2")])),
        Constant(Vector([Grid.from_string("0 2"), Grid.from_string("0 2 4")])),
        Constant(Vector([Grid.from_string("1 0"), Grid.from_string("1 0 0")])),
        Constant(Vector([Grid.from_string("1 0 1"), Grid.from_string("1 0 0")])),
        Constant(Vector([Grid.from_string("0 1"), Grid.from_string("0 1")])),
        Constant(Vector([Grid.from_string("0 1"), Grid.from_string("0 1 2 3")])),
        Constant(Vector([Grid.from_string("0\n1"), Grid.from_string("0\n1\n2\n3")])),
        Constant(Vector([Grid.from_string("0\n1\n2"), Grid.from_string("1\n2\n3")])),
        # scalar selection
        Constant(Vector([Selection.from_string(". #"), Selection.from_string(". # #")])),
        Constant(Vector([Selection.from_string(". # #"), Selection.from_string(". # #")])),
        # matching shape grids
        Constant(
            Vector(
                [
                    Grids([Grid.from_string("0 1"), Grid.from_string("1 1")]),
                    Grids([Grid.from_string("0 1 2"), Grid.from_string("1 1 1")]),
                ]
            )
        ),
        # partially matching shape grids
        Constant(
            Vector(
                [
                    Grids([Grid.from_string("0 1"), Grid.from_string("1 1")]),
                    Grids([Grid.from_string("0 2"), Grid.from_string("1 1 1")]),
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
        # non-matching shape selections
        Constant(
            Vector(
                [
                    Selections([Selection.from_string(". #"), Selection.from_string("# # .")]),
                    Selections([Selection.from_string("# #"), Selection.from_string(". # #")]),
                ]
            )
        ),
    }


@pytest.fixture
def dummy_target():
    return Vector([Grid.from_string("0 2"), Grid.from_string("0 2 0"), Grid.from_string("2 4")])


@pytest.mark.parametrize(
    "types",
    [
        (Grid, Grid),
        (Grid, Selection),
        (Grid, Selections),
        (Grid, Grid, Grid),
        (Grid, Grid, Selection),
        (Grid, Grids, Selection),
    ],
)
@pytest.mark.parametrize("replace", [True, False])
def test_function_sampler__sample_matching_shape_args(all_args, dummy_target, types, replace):
    repetitions = 100
    graph = Graph(all_args, dummy_target)
    function_sampler = FunctionSampler(graph)
    assert len(function_sampler.nodes.with_type(Grid)) == 8

    for _ in range(repetitions):
        nodes = function_sampler.sample_matching_shape_args(*types, replace=replace)

        # assert correct type
        for node, type_ in zip(nodes, types):
            assert common_type(node()) == type_

        # assert equal shape
        assert len({shape(node()) for node in nodes}) == 1

        # assert no equal nodes
        if not replace:
            assert len(set(nodes)) == len(nodes)


def test_function_sampler__all_functions_smoketest(all_args, dummy_target):
    repetitions = 100
    graph = Graph(all_args, dummy_target)
    function_sampler = FunctionSampler(graph)

    for operation in function_sampler.operation_probs.keys():
        sample_args = function_sampler.sample_args[operation]

        if sample_args is not None:
            for _ in range(repetitions):
                try:
                    args = sample_args()
                    function = Function(vectorize(operation), *args)
                    value = function()
                except Exception as exception:
                    print("failed for operation: {}".format(operation.__name__))
                    raise

                assert value is not None
