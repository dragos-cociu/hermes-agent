# ADR-0016: Phase 5 explicit Hermes captureBinding telemetry

## Status

Accepted for implementation in a separate local shadow-only Class C increment.

## Context

The P0.4 candidate transports an explicit `gateKey` inside terminal verification evidence, but a live pilot showed that outbound events have no explicit binding to the runtime session, task contract, and trace. Without that binding, a receiver cannot safely associate events with a Phase 5 session. Binding must not be inferred from cwd, prompt, path, command, transcript, ordering, task/session names, or capture paths.

## Decision

Add an optional additive `captureBinding` object before the existing outbound JSON is signed:

```json
{
  "captureBinding": {
    "sessionId": "...",
    "taskContractId": "...",
    "traceId": "..."
  }
}
```

Each field is accepted only when it is an explicit non-empty string of at most 256 characters without a NUL byte. Invalid fields are omitted without trimming, repair, fallback, or inference. If no field validates, `captureBinding` is absent rather than null or empty.

`sessionId` uses the already explicit runtime/session plumbing. `taskContractId` and `traceId` are added as explicit parameters through the existing agent and hook paths. A delegated subagent inherits both values verbatim from its parent; it does not generate or derive replacements.

The binding is additive and opt-in. Callers that do not provide it retain the previous payload shape. The existing HMAC automatically covers the binding because serialization occurs before signing. Signing, queueing, delivery, producer sequencing, target parsing, and existing top-level fields are unchanged.

## Scope boundaries

This increment does not add persistent configuration, a user-facing environment variable, a new model-facing tool argument, a receiver, a normalizer, an active decision path, or deployment. The candidate remains shadow-only.

## Verification

The implementation must include unit coverage for validation, omission and non-inference, child inheritance, event consistency, and HMAC coverage. It must also include a real temporary-`HERMES_HOME` HTTPServer path that registers the hook from config, invokes and flushes it, and inspects the delivered signed body.

## Rollback

A revert removes the additive field and explicit plumbing. No persistent state or migration is required.
