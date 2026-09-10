from hermes_cli import lifecycle


def test_lifecycle_forwards_explicit_capture_binding(monkeypatch):
    seen = {}
    monkeypatch.setattr("hermes_cli.observability.observe_lifecycle", lambda *a, **k: None)
    monkeypatch.setattr(
        "hermes_cli.plugins.invoke_hook",
        lambda name, **kwargs: seen.update(name=name, **kwargs) or [],
    )

    lifecycle.invoke_hook(
        "on_session_start",
        session_id="session-1",
        task_contract_id="contract-1",
        trace_id="trace-1",
    )

    assert seen["task_contract_id"] == "contract-1"
    assert seen["trace_id"] == "trace-1"


def test_lifecycle_does_not_infer_binding(monkeypatch):
    seen = {}
    monkeypatch.setattr("hermes_cli.observability.observe_lifecycle", lambda *a, **k: None)
    monkeypatch.setattr(
        "hermes_cli.plugins.invoke_hook",
        lambda name, **kwargs: seen.update(kwargs) or [],
    )
    lifecycle.invoke_hook("on_session_start", session_id="contract-looking-session")
    assert "task_contract_id" not in seen
    assert "trace_id" not in seen
