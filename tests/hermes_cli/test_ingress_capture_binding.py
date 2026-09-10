"""Regression coverage for explicit CLI/one-shot capture bindings."""

import ast
import inspect

from hermes_cli import oneshot
from hermes_cli.cli_agent_setup_mixin import CLIAgentSetupMixin


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    return next(
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    )


def _call(function: ast.AST, name: str) -> ast.Call:
    return next(
        node for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and ((isinstance(node.func, ast.Name) and node.func.id == name)
             or (isinstance(node.func, ast.Attribute) and node.func.attr == name))
    )


def _assert_forwarded(call: ast.Call) -> None:
    keywords = {keyword.arg: keyword.value for keyword in call.keywords}
    for name in ("task_contract_id", "trace_id"):
        assert isinstance(keywords[name], ast.Name)
        assert keywords[name].id == name


def test_oneshot_binding_is_explicit_verbatim_and_defaults_to_none(monkeypatch):
    seen = {}

    def fake_run_agent(*args, **kwargs):
        seen.update(kwargs)
        return "ok", {"final_response": "ok"}

    monkeypatch.setattr(oneshot, "_run_agent", fake_run_agent)
    monkeypatch.setattr(oneshot, "_validate_explicit_toolsets", lambda value: (None, None))

    assert oneshot.run_oneshot("hello", task_contract_id=" contract ", trace_id="trace") == 0
    assert seen["task_contract_id"] == " contract "
    assert seen["trace_id"] == "trace"

    seen.clear()
    assert oneshot.run_oneshot("hello") == 0
    assert seen["task_contract_id"] is None
    assert seen["trace_id"] is None


def test_oneshot_agent_constructor_forwards_binding_names():
    tree = ast.parse(inspect.getsource(oneshot))
    _assert_forwarded(_call(_function(tree, "_run_agent"), "AIAgent"))


def test_interactive_cli_agent_constructor_forwards_explicit_or_absent_binding():
    signature = inspect.signature(CLIAgentSetupMixin._init_agent)
    assert signature.parameters["task_contract_id"].default is None
    assert signature.parameters["trace_id"].default is None

    tree = ast.parse(inspect.getsource(CLIAgentSetupMixin))
    _assert_forwarded(_call(_function(tree, "_init_agent"), "AIAgent"))
