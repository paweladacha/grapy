from behave import given, when, then


@given("I have a working environment")
def step_given_working_environment(context):
    context.dummy = "dummy"


@when("I run a test")
def step_when_run_test(context):
    context.result = f"Hello {context.dummy}"


@then("I should see the result")
def step_then_see_result(context):
    assert context.result == "Hello dummy"
