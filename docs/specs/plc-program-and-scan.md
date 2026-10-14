# PLC program, I/O and scan study (CC-6)

Status: frozen by WP-2.2. Schemas: `contracts/automation/plc-model.schema.json`
(`automation.plc`), `plc-scan-request.schema.json` and `plc-scan-result.schema.json`
(`plc.scan`). Validation: `packages/py/qe_core/src/qe_core/plc_contracts.py`. Language:
`quantic-st-0.1`, defined in `docs/specs/structured-text-subset.md`.

IEC 61131-3 is not owned, so nothing here claims conformance with it. Sources: Bolton,
Programmable Logic Controllers, 6th ed (Newnes, 2015) for the scan (pp. 106 to 107, mass
I/O copying) and counters (Figure 10.1, p. 246); Beckhoff Tc2_Standard pages for timer
and counter behaviour (accessed 2026-10-14). Everything marked (choice) is a Quantic
subset choice.

## 1. Model (`automation.plc`)

- `controller_id`, `name`, `language: quantic-st-0.1`.
- `program`: `program_id` and `body`, the statements only (no PROGRAM or VAR blocks).
- `variables`: name, section (input, output, internal), type (BOOL, INT, REAL, TIME) and
  an optional typed `initial`. Inputs take no initial value. Defaults: FALSE, 0, 0.0,
  0 ms. TIME values are integer milliseconds.
- `instances`: function-block instances (TON, TOF, TP, CTU, CTD, CTUD).
- `task`: one cyclic task with `period_ms` from 1 to 60000.
- `devices`: optional field devices, each owning some I/O variables, so an asset in the
  project registry can name a pushbutton or contactor (element type `devices`).
- `process`: `null` or the authored motor starter of section 5.

Rules checked without parsing the body: names follow `[A-Za-z_][A-Za-z0-9_]*`, are not
reserved words and are unique ignoring case (ST is not case sensitive, Bolton p. 169);
instance names count. First-slice I/O is BOOL only (choice: digital I/O). Initial values
are typed with no coercion and in range (INT -32768 to 32767; REAL finite binary32; TIME
-2147483648 to 2147483647 ms). Each I/O variable belongs to at most one device. Errors
inside the body (unknown names, types, syntax) are the engine's diagnostics with the
body line and column.

Asset element types: `controller`, `devices`, `variables`, `function_blocks`, `process`.

A stored `automation.plc` or `plc.scan` payload whose `schema_version` is not a CC-6
version (for example the CC-3 placeholder in `examples/multi_domain`) stays stored,
unvalidated and not executable, with an info diagnostic, and its bytes are preserved.

## 2. Scan request (`plc.scan`)

`execution` is a CC-4 time-stepped request with the `fixed_ms` clock, elapsed time from
0 (`start: cold`: every variable takes its initial value and every block its reset
state), `step_size_s` equal to the task period, and at most 100000 scans.

`bindings` give every CC-4 signal exactly one target. All signals are boolean with unit
`1`.

| Signal | Binds to |
|---|---|
| input | an input variable not wired to the process, or the process scenario ports `overload_event`, `overload_reset` |
| output | an output variable, or the process state ports `contactor_closed`, `overload_tripped`, `motor_running` |

Every unwired input variable and every output variable is bound exactly once; with a
process, both scenario ports are bound. `events.sha256` pins the event file.

## 3. Input events

The CC-4 `input_series_file` is a time series of instant samples on the same elapsed
axis whose signals equal the request's input signals, in order. The row at 0 ms sets
every input; later rows list every input again, and a value that differs from the row
before is a change. Rows are whole milliseconds and before the stop time, and every cell
is valid: a PLC input is never missing. Values hold until the next row.

A change at t_e is first seen by the first scan that starts at or after t_e (Bolton
pp. 106 to 107: inputs are copied once, at the start of the scan). The result lists every
change with that `first_scan`, or `null` when no scan in the run starts after it.

## 4. Scan ordering and timing

With period h, scan k starts at t_k = k h and commits at t_(k+1):

1. Capture the input image at t_k: external inputs from the events, process-wired inputs
   from the process state left by scan k - 1 (the initial state for scan 0).
2. Execute the statements top to bottom. Timers use t_k. A block's outputs read before
   its call in the same scan are those of its previous call.
3. Commit the output image at t_(k+1).
4. Advance the process with the committed coil and the scenario inputs captured at t_k.

So process feedback reaches the program one scan after the coil changes (one-scan
feedback), and the execution time of a scan is modelled as the whole period (choice).

The CC-4 series holds instant samples at t_0 ... t_N: input cells are what scan k read;
output cells at t_0 are the initial values and at t_(k+1) what scan k committed. The CC-4
steps are one `initialise` and one `step_to` per scan. A runtime fault in scan k keeps
scans 0 to k - 1, ends at t_k with status `partial` and an error diagnostic.

## 5. Motor-starter process (authored, not a model of real equipment)

State: contactor closed C, overload tripped O. Scenario inputs: overload event E (the
overload relay's trip condition is present), reset R. Coil command K from the PLC output
wired as `coil`.

| Step | Rule |
|---|---|
| 1 | O' = E OR (O AND NOT R): the event wins over a reset in the same scan |
| 2 | C' = K AND NOT O': the relay's contact is in series with the coil |
| 3 | running' = C': no acceleration or motor dynamics |
| 4 | Next scan reads `contactor_feedback` = C' and `overload_ok` = NOT O' |

The initial state must satisfy C = K_initial AND NOT O. The relay contact in series with
the coil is a hardwired interlock: it opens the contactor at the commit in which the trip
occurs, one scan before the program can see `overload_ok` fall. There are no electrical
dynamics, no timing of real contactors and no safety rating.

## 6. Result

`execution` is the CC-4 time-stepped result; `program` gives the program ID and the
SHA-256 of the body; `events` is the change list of section 3; `scans` is the per-scan
working (decision D11): input image, each statement (assignment target and value, IF
condition and value, block call with inputs and outputs), output image, every instance's
outputs and the process before, scenario, coil and after. `limitations` lists the
declared subset limits shown in reports.

Checks on a result: one scan per completed step, at k h and committed at (k + 1) h; the
images name exactly the declared inputs and outputs with typed values; every call names
a declared instance and reports exactly its block's outputs; timers have PT >= 0 and
0 <= ET <= PT; counters have Q, QU and QD consistent with CV and PV and CV >= 0 for down
counters; process-wired inputs repeat the previous scan's process state; the process
follows section 5; the series repeats the images; every scan input is the latest event
at or before its start.

## 7. Declared limits

No full IEC 61131-3 language, no edition conformance, no vendor binary compatibility, no
multitasking, fieldbus, retain memory, analog I/O, ladder logic or hardware access, and
no safety certification.
