from types import SimpleNamespace

from agent.conversation_loop import _restore_or_build_system_prompt


def test_new_session_lifecycle_receives_explicit_agent_binding(monkeypatch):
    events = []
    agent = SimpleNamespace(
        _session_db=None,
        session_id="session-1",
        task_contract_id="contract-1",
        trace_id="trace-1",
        model="test-model",
        platform="cli",
        _build_system_prompt=lambda _message: "prompt",
    )
    monkeypatch.setattr(
        "hermes_cli.lifecycle.invoke_hook",
        lambda name, **kwargs: events.append((name, kwargs)) or [],
    )
    monkeypatch.setattr(
        "agent.credits_tracker.seed_credits_at_session_start", lambda _agent: None,
    )

    _restore_or_build_system_prompt(agent, None, [])

    assert events == [("on_session_start", {
        "session_id": "session-1",
        "task_contract_id": "contract-1",
        "trace_id": "trace-1",
        "model": "test-model",
        "platform": "cli",
    })]
