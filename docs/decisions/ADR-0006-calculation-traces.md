# ADR-0006: Results carry their working (Contract Change CC-7)

Status: Accepted (Peter, 2026-10-14, decision D11). Implemented by WP-1.11.

## Context

The Phase 1 audit found every number correct but no equations in the reports
(dispute 2026-10-14-claude-WP-1.7-dispute.md). Peter's requirement: a reviewer
must be able to see each equation, the values substituted into it and the
result, and redo the calculation by hand from the report alone.

## Decision

1. Results carry a trace of their working. Short-circuit result 0.3.0 adds a
   per-bus `trace`; motor-start result 0.4.0 adds `motor_trace`. Both are
   additive and optional; 0.2.0 and 0.3.0 results stay valid against archived
   schemas in `contracts/v0.2/` and `contracts/v0.3/`.
2. The trace is computed by our own arithmetic, not copied from the engine.
   For single-source radial short-circuit components the adapter builds each
   element impedance from the inputs and sums them along the path, referring
   across transformers by the squared rated ratio. A current is reported only
   if that sum agrees with pandapower's network reduction, and
   c Un / (sqrt(3) |Z_k|) reproduces pandapower's Ik'', to a relative 1e-9.
   The trace is therefore a second, independent calculation, not decoration.
3. Reports present the trace: a Method section listing every governing
   equation with its book, edition and page, then a worked calculation per
   bus and case. The load-flow report gains its method and a per-bus power
   balance closed from the reported flows.
4. Notation is ASCII (sqrt, kappa, ^, *) because the PDF fonts must render it.

## Consequences

- Meshed or multi-source components show the engine's Thevenin impedance
  with basis `engine-thevenin`; the Ik'' identity is still checked.
- A future engine change that alters an impedance by more than 1e-9 makes the
  value unavailable instead of silently different.
- Report length grows; the worked sections follow each case table so the
  summary stays first.
