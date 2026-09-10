from types import SimpleNamespace

from agent.turn_context import build_turn_context


def test_pre_llm_hook_receives_explicit_agent_binding(monkeypatch):
    """The turn prologue must bind its lifecycle event from runtime state."""
    source = __import__("inspect").getsource(build_turn_context)

    assert 'task_contract_id=getattr(agent, "task_contract_id", None)' in source
    assert 'trace_id=getattr(agent, "trace_id", None)' in source


def test_pre_llm_binding_access_does_not_synthesize_missing_values():
    agent = SimpleNamespace()

    assert getattr(agent, "task_contract_id", None) is None
    assert getattr(agent, "trace_id", None) is None
