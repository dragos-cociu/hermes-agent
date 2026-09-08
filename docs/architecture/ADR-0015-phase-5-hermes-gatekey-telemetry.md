# ADR-0015: Phase 5 explicit Hermes gateKey telemetry

## Status

Accepted for the local shadow-only Phase 5 candidate.

## Decision

Hermes accepts an optional structured `gate_key` value at the `terminal_tool`
call boundary and passes it explicitly to `record_terminal_result`. The value is
copied verbatim into `verification_evidence.gateKey` only when it is a valid,
non-empty bounded string without a NUL byte. Missing or invalid values produce
no gate key; they are never repaired or inferred.

The key is not derived from the command, canonical command, classifier kind,
cwd, repository root, task/session identifiers, transcript, or execution order.
The existing classifier remains responsible only for its existing local
classification. The existing webhook serialization already carries the
`result_dict` under `extra.result`, so its signing, queue, delivery, producer
sequence, and top-level payload code remain unchanged.

## Consequences

This is additive telemetry only. It does not add a pre-verification hook, an
in-loop action, an automatic stop, a receiver, persistence, systemd unit, or
active decision path. Callers that do not provide `gate_key` retain their prior
behavior. The candidate remains local and shadow-only; persistent activation and
integration require a separate human gate.
