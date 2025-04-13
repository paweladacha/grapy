from behave import given, when, then

from grapy.classes import (
    Signature,
    Context,
    Task,
    KeyGetter,
    Protocols,
    Workflow,
    WorkflowGraph,
)


@given("a WorkflowGraph with the diamond graph")
def step_workflowgraph_diamond(context):
    def add(a, b):
        return a + b

    node1 = Task(add, Signature(2, 3), "add1")  # 5
    edge1to2_1 = Task(add, Signature(KeyGetter("add1"), 4), "edge1to2_1")  # 9
    edge1to2_2 = Task(add, Signature(KeyGetter("add1"), 1), "edge1to2_2")  # 6
    node2_1 = Task(add, Signature(KeyGetter("add1"), 3), "add2_1")  # 8
    node2_2 = Task(add, Signature(KeyGetter("add1"), 2), "add2_2")  # 7
    edge2_1to3 = Task(add, Signature(KeyGetter("add2_1"), 3), "edge2_1to3")  # 11
    edge2_2to3 = Task(add, Signature(KeyGetter("add2_2"), 3), "edge2_2to3")  # 10
    node3 = Workflow(
        protocol=Protocols.WorkflowProtocols.BasicContext(),
        items=[
            Task(
                add, Signature(KeyGetter("add2_1"), KeyGetter("add2_2")), "add3"
            ),  # 15
            Task(
                add,
                Signature(KeyGetter("edge2_1to3"), KeyGetter("edge2_2to3")),
                "add3_1",
            ),  # 21
        ],
    )
    wfg = WorkflowGraph(
        nodes={"node1": node1, "node2_1": node2_1, "node2_2": node2_2, "node3": node3},
        edges={
            ("node1", "node2_1"): edge1to2_1,
            ("node1", "node2_2"): edge1to2_2,
            ("node2_1", "node3"): edge2_1to3,
            ("node2_2", "node3"): edge2_2to3,
        },
        root_node="node1",
        protocol=Protocols.WorkflowGraphProtocols.Balanced(),
    )
    context.wfg_diamond = wfg


@given("a sample context")
def step_sample_context(context):
    context.sample_context = Context()


@when("the WorkflowGraph is executed")
def step_workflowgraph_called(context):
    context.result = context.wfg_diamond(context.sample_context)


@then("the WorkflowGraph should return the expected result")
def step_impl(context):
    assert context.sample_context["add1"] == 5
    assert context.sample_context["add2_1"] == 8
    assert context.sample_context["add2_2"] == 7
    assert context.sample_context["add3"] == 15
    assert context.sample_context["edge1to2_1"] == 9
    assert context.sample_context["edge1to2_2"] == 6
    assert context.sample_context["edge2_1to3"] == 11
    assert context.sample_context["edge2_2to3"] == 10
    assert context.sample_context["add3"] == 15
    assert context.sample_context["add3_1"] == 21
