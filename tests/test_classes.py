# import sys
# import os

# sys.path.append("..")
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pytest
from grapy.classes import (
    Signature,
    Context,
    Task,
    KeyGetter,
    Protocols,
    Workflow,
    WorkflowWithAssumptions,
    WorkflowGraph,
)
from typing import Union, Any, Callable as TypingCallable


@pytest.fixture
def sample_function_add() -> TypingCallable[[int], int]:
    """
    Fixture that provides a sample function for testing.
    """

    def func(x: int, y: int) -> int:
        return x + y

    return func


@pytest.fixture
def sample_task_elements(sample_function_add) -> Union[TypingCallable, Signature, str]:
    f = sample_function_add
    s = Signature("hello world")
    put_to_key = "result"
    return f, s, put_to_key


@pytest.fixture
def sample_context() -> Context:
    return Context({"a": 2, "b": 2})


class TestTask:
    def test_returns_when_no_put_to(self, sample_function_add, sample_context):
        t = Task(
            func=sample_function_add,
            signature=Signature(KeyGetter("a"), 3),
            put_to=None,
        )
        ctx = sample_context
        assert t(ctx) == 5

    def test_updates_context_with_put_to(self, sample_function_add, sample_context):
        t = Task(sample_function_add, Signature(KeyGetter("a"), 3), "result")
        ctx = sample_context
        t(ctx)
        assert ctx["result"] == 5

    def test_has_given_parameters(self, sample_task_elements):
        f, s, put_to_key = sample_task_elements
        t = Task(f, s, put_to_key)
        assert t.func is f
        assert t.put_to == put_to_key
        assert t.signature is s

    def test_with_explicit_protocol(self, sample_function_add, sample_context):
        t = Task(
            sample_function_add,
            Signature(x=2, y=KeyGetter("b")),
            "result",
            protocol=Protocols.TaskProtocols.BasicContext(),
        )
        ctx = sample_context
        t(ctx)
        assert ctx["result"] == 4

    def test_default_protocol(self, sample_function_add, sample_context):
        t = Task(sample_function_add, Signature(KeyGetter("a"), 3), "result")
        ctx = sample_context
        t(ctx)
        assert ctx["result"] == 5

    def test_task_put_to_zero(self, sample_function_add, sample_context):
        t = Task(sample_function_add, Signature(2, 3), 0)
        ctx = sample_context
        out = t(ctx)
        assert out == 5
        assert ctx[0] == 5


class TestSignature:
    def test_update(self):
        s = Signature(2, b=2)
        a = "first arg"
        s.args.insert(0, a)
        assert s.args[0] == a
        z = "last arg"
        s.args.append(z)
        assert s.args[-1] == z
        new_kw = {"kw": "new kw"}
        s.kwargs.update(new_kw)
        assert "kw" in s.kwargs
        assert s.kwargs["kw"] == "new kw"


class TestContext:
    def test_resolve_missing_key(self, sample_context):
        s = Signature(1, KeyGetter("missing_key"))
        with pytest.raises(KeyError):
            args, kwargs = sample_context.resolve_keys(s)


@pytest.fixture
def sample_functions() -> Union[TypingCallable, TypingCallable, TypingCallable]:
    """
    Fixture that provides a sample functions for testing.
    """

    def add(x: int, y: int) -> int:
        return x + y

    def mul(x: int, y: int) -> int:
        return x * y

    def sub(x: int, y: int) -> int:
        return x - y

    return add, mul, sub


@pytest.fixture
def sample_task_list(sample_functions) -> Union[Task, Task, Task]:
    add, mul, sub = sample_functions
    task_list = [
        Task(add, Signature(KeyGetter("a"), y=10), "add_result"),
        Task(mul, Signature(x=2, y=KeyGetter("a")), "mul_result"),
        Task(
            sub,
            Signature(KeyGetter("add_result"), KeyGetter("mul_result")),
            "sub_result",
        ),
    ]
    return task_list


class TestWorkflow:
    def test_with_kwargs(self, sample_task_list, sample_context):
        wf = Workflow(
            items=[*sample_task_list],
            protocol=Protocols.WorkflowProtocols.BasicContext(),
        )
        ctx = sample_context
        wf(ctx)
        assert ctx["add_result"] == 12
        assert ctx["mul_result"] == 4
        assert ctx["sub_result"] == 8

    def test_with_protocol(self, sample_task_list, sample_context):
        wf = Workflow(
            protocol=Protocols.WorkflowProtocols.BasicContext(),
            items=[*sample_task_list],
        )
        ctx = sample_context
        wf(ctx)
        assert ctx["add_result"] == 12
        assert ctx["mul_result"] == 4
        assert ctx["sub_result"] == 8

    def test_manually_sequential(self, sample_functions, sample_context):
        add, mul, sub = sample_functions
        ctx = sample_context

        def task_factory_with_assumptions(func, signature):
            prev_key = KeyGetter("_prev")
            signature.args.insert(0, prev_key)
            return Task(func, signature, "_prev")

        # ctx['_prev'] = 10
        tf = task_factory_with_assumptions
        wf = Workflow(
            protocol=Protocols.WorkflowProtocols.BasicContext(),
            items=[
                Task(ctx.update, Signature({"_prev": 10}), None),
                tf(add, Signature(2)),
                tf(mul, Signature(3)),
                tf(sub, Signature(35)),
            ],
        )
        wf(ctx)
        assert ctx["_prev"] == 1

    def test_WithAssumptions_SequentialProtocol(self, sample_functions, sample_context):
        ctx = sample_context
        add, mul, sub = sample_functions
        kg_prev = KeyGetter("_prev")
        # sig_factory = lambda *args, **kwargs: Signature(kg_prev, *args, **kwargs)  # also with functools.partial
        import functools

        sig_factory = functools.partial(Signature, kg_prev)
        wfa = WorkflowWithAssumptions(
            put_to="_prev",
            map_ctx={"a": "start"},
            return_key="_prev",
            items=[
                Task(add, Signature(KeyGetter("start"), 2)),  # 4
                Task(mul, Signature(KeyGetter("_prev"), 2)),  # 8
                Task(sub, Signature(kg_prev, 7)),  # 1
                Task(add, sig_factory(4)),  # 5
            ],
            protocol=Protocols.WorkflowProtocols.Sequential(),
        )

        out = wfa(ctx)
        assert out == 5

    def test_call_empty(self, sample_context):
        ctx = sample_context
        wf = Workflow(items=[], protocol=Protocols.WorkflowProtocols.BasicContext())
        wf(ctx)

    def test_workflow_in_workflow(self, sample_functions, sample_context):
        ctx = sample_context
        add, mul, sub = sample_functions
        wf1 = Workflow(
            protocol=Protocols.WorkflowProtocols.BasicContext(),
            items=[
                Task(add, Signature(2, 2), "add"),  # 4
                Task(mul, Signature(3, 3), "mul"),  # 9
            ],
        )
        wf2 = Workflow(
            protocol=Protocols.WorkflowProtocols.BasicContext(),
            items=[
                wf1,
                Task(sub, Signature(KeyGetter("mul"), KeyGetter("add")), "sub"),
            ],  # 5
        )
        wf2(ctx)
        assert ctx["sub"] == 5


class TestWorkflowGraph:
    def test_init_empty(self):
        wfg = WorkflowGraph()
        assert isinstance(wfg, WorkflowGraph)

    def test_call_with_one_task_node(self, sample_function_add, sample_context):
        node = {"node1": Task(sample_function_add, Signature(1, 2), "result")}
        wfg = WorkflowGraph(
            nodes=node,
            root_node="node1",
            protocol=Protocols.WorkflowGraphProtocols.Balanced(),
        )
        wfg(sample_context)
        assert sample_context["result"] == 3

    def test_traverse_balanced_protocol(self):
        wfg = WorkflowGraph(
            nodes=dict(node1=None, node2=None),
            edges={("node1", "node2"): None},
            root_node="node1",
            protocol=Protocols.WorkflowGraphProtocols.Balanced(),
        )
        traverse_generator = wfg.traverse()
        assert next(traverse_generator) == "node1"
        assert next(traverse_generator) == ("node1", "node2")
        assert next(traverse_generator) == "node2"

    def test_traverse_balanced_protocol_diamond_graph(self):
        wfg = WorkflowGraph(
            nodes={"node{}".format(x): None for x in range(1, 5)},
            edges={
                ("node1", "node2"): None,
                ("node1", "node3"): None,
                ("node2", "node4"): None,
                ("node3", "node4"): None,
            },
            root_node="node1",
            protocol=Protocols.WorkflowGraphProtocols.Balanced(),
        )

        traverse_generator = wfg.traverse()
        assert next(traverse_generator) == "node1"
        assert next(traverse_generator) in (("node1", "node2"), ("node1", "node3"))
        assert next(traverse_generator) in (("node1", "node2"), ("node1", "node3"))
        assert next(traverse_generator) in ("node2", "node3")
        assert next(traverse_generator) in ("node2", "node3")
        assert next(traverse_generator) in (("node2", "node4"), ("node3", "node4"))
        assert next(traverse_generator) in (("node2", "node4"), ("node3", "node4"))
        assert next(traverse_generator) == "node4"

    def test_call_balanced_diamond_graph(self, sample_functions, sample_context):
        ctx = sample_context
        add, mul, sub = sample_functions
        wfg = WorkflowGraph(
            root_node="node1", protocol=Protocols.WorkflowGraphProtocols.Balanced()
        )
        wfg.nodes["node1"] = Task(
            add, Signature(KeyGetter("a"), KeyGetter("b")), "r_node1"
        )  # 4
        wfg.edges[("node1", "node2")] = Task(
            add, Signature(KeyGetter("r_node1"), 3), "r_edge1_2"
        )  # 7
        wfg.edges[("node1", "node3")] = Task(
            add, Signature(KeyGetter("r_node1"), 1), "r_edge1_3"
        )  # 5
        wfg.nodes["node2"] = Task(
            mul, Signature(KeyGetter("r_edge1_2"), 3), "r_node2"
        )  # 21
        wfg.nodes["node3"] = Task(
            mul, Signature(KeyGetter("r_edge1_3"), 7), "r_node3"
        )  # 35
        wfg.edges[("node2", "node4")] = Task(
            add, Signature(KeyGetter("r_node2"), 2), "r_edge2_4"
        )  # 23
        wfg.edges[("node3", "node4")] = Task(
            add, Signature(KeyGetter("r_node3"), 2), "r_edge3_4"
        )  # 37
        wfg.nodes["node4"] = Workflow(
            protocol=Protocols.WorkflowProtocols.BasicContext(),
            items=[
                Task(sub, Signature(30, KeyGetter("r_edge2_4")), "sub1"),  # 7
                Task(sub, Signature(40, KeyGetter("r_edge3_4")), "sub2"),  # 3
                Task(
                    mul, Signature(KeyGetter("sub1"), KeyGetter("sub2")), "final"
                ),  # 21
            ],
        )

        wfg(ctx)
        assert ctx["r_node1"] == 4
        assert ctx["r_edge1_2"] == 7
        assert ctx["r_edge1_3"] == 5
        assert ctx["r_node2"] == 21
        assert ctx["r_node3"] == 35
        assert ctx["r_edge2_4"] == 23
        assert ctx["r_edge3_4"] == 37
        assert ctx["sub1"] == 7
        assert ctx["sub2"] == 3
        assert ctx["final"] == 21


# below needs to be rethinked - think how each element can be customized, extended
# and make that as obvious and as simple as possible
def test_wrapping_protocol(sample_function_add):
    count = []

    class WrappedProtocol(Protocols.TaskProtocols.BasicContext):
        def __call__(self, task, context):
            print("wrapper")
            count.append(1)
            return super().__call__(task, context)

    import functools

    task_factory = functools.partial(Task, protocol=WrappedProtocol())
    t = task_factory(sample_function_add, Signature(2, 3), "result")
    t(Context())
    assert count[0] == 1
    # raise NotImplementedError
