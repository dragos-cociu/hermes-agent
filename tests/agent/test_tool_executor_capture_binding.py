from types import SimpleNamespace
from unittest.mock import patch

from agent.tool_executor import _emit_terminal_post_tool_call


def test_terminal_tool_emitter_passes_agent_binding():
    agent = SimpleNamespace(
        session_id="session-1", task_contract_id="contract-1", trace_id="trace-1",
        _current_turn_id="turn-1", _current_api_request_id="request-1",
    )
    with patch("model_tools._emit_post_tool_call_hook") as emit:
        _emit_terminal_post_tool_call(
            agent, function_name="terminal", function_args={}, result="ok",
            effective_task_id="task-1", tool_call_id="tool-1",
        )
    assert emit.call_args.kwargs["task_contract_id"] == "contract-1"
    assert emit.call_args.kwargs["trace_id"] == "trace-1"
