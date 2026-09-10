import ast
from pathlib import Path


def test_all_turn_finalizer_lifecycle_emitters_pass_explicit_binding():
    source = Path("agent/turn_finalizer.py").read_text()
    tree = ast.parse(source)
    lifecycle_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "_invoke_hook":
            lifecycle_calls.append(node)

    assert len(lifecycle_calls) == 3
    for call in lifecycle_calls:
        keyword_names = {keyword.arg for keyword in call.keywords}
        assert "task_contract_id" in keyword_names
        assert "trace_id" in keyword_names
