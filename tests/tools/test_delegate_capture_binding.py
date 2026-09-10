import threading
from unittest.mock import MagicMock, patch

from tools.delegate_tool import _build_child_agent


def test_delegated_child_inherits_parent_binding_exactly():
    parent = MagicMock()
    parent.base_url = "https://example.invalid/v1"
    parent.api_key = "key"
    parent.provider = "openrouter"
    parent.api_mode = "chat_completions"
    parent.model = "test-model"
    parent.platform = "cli"
    parent.providers_allowed = None
    parent.providers_ignored = None
    parent.providers_order = None
    parent.provider_sort = None
    parent.provider_require_parameters = False
    parent.provider_data_collection = None
    parent.openrouter_min_coding_score = None
    parent.enabled_toolsets = ["terminal"]
    parent.disabled_toolsets = None
    parent._session_db = None
    parent._delegate_depth = 0
    parent._active_children = []
    parent._active_children_lock = threading.Lock()
    parent._print_fn = None
    parent.tool_progress_callback = None
    parent.thinking_callback = None
    parent.session_id = "parent-session"
    parent.task_contract_id = " contract-verbatim "
    parent.trace_id = "trace-verbatim"

    with (
        patch("tools.delegate_tool._load_config", return_value={}),
        patch("run_agent.AIAgent") as agent_class,
        patch("hermes_cli.lifecycle.invoke_hook", return_value=[]),
    ):
        agent_class.return_value = MagicMock(session_id="child-session")
        _build_child_agent(
            task_index=0, goal="test", context=None, toolsets=None, model=None,
            max_iterations=5, task_count=1, parent_agent=parent,
        )

    kwargs = agent_class.call_args.kwargs
    assert kwargs["task_contract_id"] == " contract-verbatim "
    assert kwargs["trace_id"] == "trace-verbatim"
