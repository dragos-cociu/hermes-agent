# ADR-0017: Phase 5 Hermes ingress binding

Status: Accepted

## Context

Hermes agents can emit verification evidence whose `captureBinding` includes a
task contract and trace. The agent runtime already preserves explicitly supplied
`task_contract_id` and `trace_id` values and delegated agents already inherit
them. The remaining boundary is construction of agents by CLI, one-shot, and
gateway ingress paths.

Inferring either identifier from a prompt, working directory, filename,
transcript, command, process environment, or an unrelated session/task ID would
make the evidence ambiguous. Changing a binding between turns would likewise
make one cached agent represent multiple identities.

## Decision

CLI, one-shot, foreground gateway, and background gateway ingress methods accept
optional `task_contract_id` and `trace_id` values and pass them explicitly and
verbatim to `AIAgent` construction. Both values are fixed for that agent/session
lifetime. Gateway queued follow-ups forward the original pair unchanged.

If an ingress caller has no explicit value, it supplies the default `None`.
Hermes does not infer, normalize, generate, or read either value from the
environment. The gateway hygiene agent is internal maintenance rather than a
real ingress session and remains unchanged.

## Consequences

- Callers with authoritative task context can establish a complete capture
  binding at ingress.
- Existing callers remain unbound and preserve `None` without behavior change.
- Agent caching remains compatible because a binding cannot change per turn.
- Delegated children continue using the existing parent-to-child inheritance.

## Non-goals

This decision does not change serialization, signing, HMAC, queueing, delivery,
producer sequencing, receiver behavior, model tools, environment variables, or
the existing delegation plumbing. It does not activate persistent hooks,
services, or any outbound integration.
