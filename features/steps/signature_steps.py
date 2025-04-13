from behave import given, when, then

from grapy.classes import (
    Signature,
    # Context,
    # Task,
    # KeyGetter,
    # Protocols,
    # Workflow,
    # WorkflowWithAssumptions,
)
from typing import Union, Any, Callable as TypingCallable


@given("I have sample Signature")
def step_given_working_environment(context):
    context.sample_signature = Signature("positional_arg", kwarg="some_kwarg")


@when("I insert argument at zero index")
def step_when_run_test(context):
    context.new_argument = "inserted_argument"
    context.sample_signature.args.insert(0, context.new_argument)


@then("Signature has that argument at zero index")
def step_then_see_result(context):
    assert context.sample_signature.args[0] == context.new_argument
