from typing import Any, Callable as TypingCallable, Union, Tuple
from abc import ABC, abstractmethod


class KeyGetter:
    def __init__(self, key):
        self.key = key


class Signature:
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = kwargs


class Context(dict):
    def _resolve_key(self, parameter):
        if isinstance(parameter, KeyGetter):
            return self[parameter.key]
        else:
            return parameter

    def resolve_keys(self, signature: Signature):
        args = [self._resolve_key(arg) for arg in signature.args]
        kwargs = {k: self._resolve_key(v) for k, v in signature.kwargs.items()}
        return args, kwargs


class Protocols:
    class TaskProtocols:
        class BasicContext:
            def __call__(self, task, context):
                args, kwargs = context.resolve_keys(task.signature)
                result = task.func(*args, **kwargs)
                if task.put_to is not None:
                    context[task.put_to] = result
                return result

    class WorkflowProtocols:
        class BasicContext:
            def __call__(self, workflow, context):
                last_out = None
                for item in workflow.items:
                    last_out = item(context)
                return last_out

        class Sequential:
            def __call__(self, workflow, context):
                if workflow.map_ctx:
                    for k_from, k_to in workflow.map_ctx.items():
                        context[k_to] = context[k_from]

                for item in workflow.items:
                    context[workflow.put_to] = item(context)

                if workflow.return_key:
                    return context[workflow.return_key]

    class WorkflowGraphProtocols:
        class Balanced:
            def __call__(self, graph, context):
                last_out = None
                for key in self._traverse(graph):
                    print(f"this key {key}")
                    if isinstance(key, tuple):  # then it is an edge
                        obj = graph.edges[key]
                    else:
                        obj = graph.nodes[key]
                    last_out = obj(context)
                return last_out

            def _get_edge_dict(self, graph):
                edge_dict = {}
                for src, tar in graph.edges.keys():
                    if src in edge_dict:
                        edge_dict[src].add(tar)
                    else:
                        edge_dict[src] = {
                            tar,
                        }
                return edge_dict

            def _traverse(self, graph):
                edge_dict = self._get_edge_dict(graph)

                node_keys = set((graph.root_node,))
                edge_keys_set = set()

                while node_keys:

                    edge_keys_set.clear()
                    for src_node_key in node_keys:
                        yield src_node_key
                        if src_node_key in edge_dict:
                            edge_keys_set.update(
                                {
                                    (src_node_key, target_node_key)
                                    for target_node_key in edge_dict[src_node_key]
                                }
                            )

                    node_keys.clear()
                    for edge_key in edge_keys_set:
                        yield edge_key
                        node_keys.add(edge_key[-1])


class Task:
    def __init__(
        self,
        func: TypingCallable,
        signature: Signature,
        put_to: str = None,
        protocol=Protocols.TaskProtocols.BasicContext(),
    ):
        self.func = func
        self.signature = signature
        self.put_to = put_to
        self.protocol = protocol

    def __call__(self, context: Context) -> Any:
        return self.protocol(self, context)


class Workflow:
    def __init__(self, items, protocol=None):
        self.items = items
        self.protocol = protocol

    def __call__(self, context: Context):
        return self.protocol(self, context)


class WorkflowWithAssumptions(Workflow):
    def __init__(self, *args, put_to=None, map_ctx=None, return_key=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.put_to = put_to
        self.map_ctx = map_ctx
        self.return_key = return_key


class WorkflowGraph:
    def __init__(
        self, nodes: dict = None, edges: dict = None, root_node=None, protocol=None
    ):
        self.nodes = nodes if nodes else dict()
        self.edges = edges if edges else dict()
        self.root_node = root_node
        self.protocol = protocol

    def __call__(self, context: Context):
        return self.protocol(self, context)

    def traverse(self):
        yield from self.protocol._traverse(self)


class SystemManager:
    """Abstract class providing factory object for all classes"""

    def __init__(self):
        pass

    def get_keygetter(self, *args, **kwargs):
        return KeyGetter(*args, **kwargs)

    def get_signature(self, *args, **kwargs):
        return Signature(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        return Context(*args, **kwargs)

    def get_task(self, *args, **kwargs):
        return Task(*args, **kwargs)

    def get_workflow(self, *args, **kwargs):
        return Workflow(*args, **kwargs)

    def get_workflowgraph(self, *args, **kwargs):
        return WorkflowGraph(*args, **kwargs)
