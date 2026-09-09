"""Structural regression coverage for gateway capture-binding ingress."""

import ast
from pathlib import Path


RUN_PATH = Path(__file__).parents[2] / "gateway" / "run.py"


def _functions(tree: ast.AST, name: str):
    return [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    ]


def _calls(function: ast.AST, name: str):
    return [
        node for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and ((isinstance(node.func, ast.Name) and node.func.id == name)
             or (isinstance(node.func, ast.Attribute) and node.func.attr == name))
    ]


def _keyword_name(call: ast.Call, keyword: str) -> str | None:
    value = next(item.value for item in call.keywords if item.arg == keyword)
    return value.id if isinstance(value, ast.Name) else None


def test_gateway_foreground_binding_is_fixed_and_forwarded_verbatim():
    tree = ast.parse(RUN_PATH.read_text(encoding="utf-8"))
    wrapper = _functions(tree, "_run_agent")[0]
    inner = _functions(tree, "_run_agent_inner")[0]

    for name in ("task_contract_id", "trace_id"):
        parameter = next(arg for arg in wrapper.args.args if arg.arg == name)
        assert parameter is not None
        forwarded = _calls(wrapper, "_run_agent_inner")
        assert len(forwarded) == 2
        assert all(_keyword_name(call, name) == name for call in forwarded)

    context_call = _calls(inner, "TurnContext")[0]
    assert _keyword_name(context_call, "task_contract_id") == "task_contract_id"
    assert _keyword_name(context_call, "trace_id") == "trace_id"

    run_sync = next(
        function for function in _functions(tree, "run_sync")
        if _calls(function, "AIAgent")
        and any(
            ast.unparse(item.value) == "ctx.session_id"
            for call in _calls(function, "AIAgent")
            for item in call.keywords
            if item.arg == "session_id"
        )
    )
    constructor = _calls(run_sync, "AIAgent")[0]
    values = {item.arg: item.value for item in constructor.keywords}
    assert ast.unparse(values["task_contract_id"]) == "ctx.task_contract_id"
    assert ast.unparse(values["trace_id"]) == "ctx.trace_id"

    recursive = _calls(inner, "_run_agent")[-1]
    assert _keyword_name(recursive, "task_contract_id") == "task_contract_id"
    assert _keyword_name(recursive, "trace_id") == "trace_id"


def test_gateway_background_binding_is_explicit_and_hygiene_agent_is_unchanged():
    tree = ast.parse(RUN_PATH.read_text(encoding="utf-8"))
    background = _functions(tree, "_run_background_task_inner")[0]
    constructor = _calls(background, "AIAgent")[0]
    assert _keyword_name(constructor, "task_contract_id") == "task_contract_id"
    assert _keyword_name(constructor, "trace_id") == "trace_id"

    all_agent_calls = [
        call for call in ast.walk(tree)
        if isinstance(call, ast.Call)
        and ((isinstance(call.func, ast.Name) and call.func.id == "AIAgent")
             or (isinstance(call.func, ast.Attribute) and call.func.attr == "AIAgent"))
    ]
    hygiene = next(call for call in all_agent_calls if call.lineno > 19000 and call.lineno < 21000)
    assert "task_contract_id" not in {item.arg for item in hygiene.keywords}
    assert "trace_id" not in {item.arg for item in hygiene.keywords}
