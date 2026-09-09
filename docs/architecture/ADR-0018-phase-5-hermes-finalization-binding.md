# ADR-0018: Phase 5 Hermes finalization binding

Status: Accepted

## Context

P0.4c populated `task_contract_id` and `trace_id` at agent construction, but a
real one-shot run showed that the normal CLI teardown did not include the same
binding in `on_session_finalize`. The gateway expiry/shutdown and TUI session
boundary paths had the same lifecycle boundary risk.

## Decision

Keep `task_contract_id` and `trace_id` explicit and fixed for the lifetime of
the agent/session. The normal CLI, gateway, and TUI finalization paths forward
the values verbatim to the existing generic lifecycle dispatcher. CLI callers
may provide explicit values through `--task-contract-id` and `--trace-id`.
Omitted values remain `None`.

No value is inferred from cwd, prompt, command, transcript, filename,
environment, unrelated session/task identifiers, or turn order. No value is
generated or changed per turn. Queued follow-ups and session expiry preserve the
same pair. The internal gateway hygiene agent remains unbound.

## Consequences

- Normal CLI one-shot/session teardown can produce a complete binding on
  `on_session_finalize`.
- Gateway shutdown/expiry and TUI teardown preserve the same session identity.
- Existing callers remain compatible when flags/values are omitted.
- Existing lifecycle dispatch, signing, queue, delivery, and captureBinding
  serialization remain unchanged.

## Non-goals

This increment does not change HMAC/signing, producer sequencing, outbound
queueing, receiver behavior, persistent hooks, systemd, active mode, or
ProgressTrace Core. It does not merge or publish the candidate.
