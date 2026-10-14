# Structured Text subset (qe_plc engine, WP-2.8)

Status: frozen for WP-2.2 (CC-6), which builds the PLC program and scan-study contract on it.

This is a deliberately bounded subset of IEC 61131-3 Structured Text. IEC 61131-3
itself is not owned (PLAN.md section 9, paid-source table), so nothing here claims
conformance with it. Sources are cited per rule; where the owned books are silent the
rule is a declared Quantic subset choice, listed in section 6.

Sources:

- Bolton, W., Programmable Logic Controllers, 6th ed (Newnes/Elsevier, 2015), in
  `Pietrols/QE-References` as `bolton-2015-plc`: mass I/O copying pp. 106 to 107; scan
  cycle p. 117; Structured Text section 6.3, Table 6.3 p. 168 and pp. 168 to 169; timers
  section 9.1 p. 225, Figures 9.2 and 9.3 p. 226; counters section 10.1 p. 245.
- Petruzella, F. D., Programmable Logic Controllers, 3rd ed (McGraw-Hill, 2005),
  `petruzella-2005-plc`, for background on timer and counter instructions.

## 1. Program structure

```
PROGRAM <name>
  VAR_INPUT  <declarations> END_VAR     (read from the input image; the program cannot write them)
  VAR_OUTPUT <declarations> END_VAR     (copied to the output image at the end of each scan)
  VAR        <declarations> END_VAR     (internal, retained between scans; function-block instances)
  <statements>
END_PROGRAM
```

A declaration is `name {, name} : TYPE [:= constant] ;`. Inputs take no initial value.
Function-block instances are declared only in VAR and take no initial value. Each name is
declared once.

## 2. Lexical rules

- Not case sensitive, for keywords and names (Bolton p. 169). Spaces and line breaks are
  free. Comments: `(* ... *)` and `// ...` to end of line.
- Literals: `TRUE`, `FALSE`; integers `42`; reals with a decimal point `0.5`, `1.0e3`;
  durations `T#` or `TIME#` followed by parts in `d`, `h`, `m`, `s`, `ms`, for example
  `T#1m30s`, `TIME#250ms`. Durations resolve to whole milliseconds.
- Words outside the subset (FOR, WHILE, REPEAT, CASE, FUNCTION, FUNCTION_BLOCK, POINTER,
  ARRAY, STRUCT, AT, RETAIN, DINT, LREAL, STRING and others) are rejected with
  UNSUPPORTED_SYNTAX, never ignored.

## 3. Statements

- Assignment `target := expression ;` to an output or internal variable.
- `IF c THEN ... {ELSIF c THEN ...} [ELSE ...] END_IF ;` with BOOL conditions.
- Function-block call `instance(INPUT := expression, ...) ;` with named inputs only;
  omitted inputs take FALSE, 0 or T#0ms. Outputs are read as `instance.Q`, `instance.ET`,
  `instance.CV`, `instance.QU`, `instance.QD`.
- Statements run once per scan, top to bottom. There are no loops, so every scan does a
  bounded amount of work.

## 4. Types and operators

Types: BOOL; INT (16-bit, -32768 to 32767); REAL (IEEE 754 binary32: values are rounded
to single precision on assignment); TIME (whole milliseconds).

Precedence, lowest first (Bolton Table 6.3, p. 168): OR; XOR; AND and &; = and <>;
<, >, <= and >=; + and -; *, / and MOD; unary - and NOT; **; parentheses. Binary
operators of equal precedence associate to the left, including ** (choice).

| Operator | Operands | Result |
|---|---|---|
| AND, &, OR, XOR | BOOL | BOOL |
| NOT | BOOL | BOOL |
| unary - | INT, REAL, TIME | same |
| + and - | INT and INT; TIME and TIME; INT or REAL mixed | INT; TIME; REAL |
| * and / | INT and INT; INT or REAL mixed | INT; REAL |
| MOD | INT and INT | INT |
| ** | INT or REAL | REAL |
| =, <> | equal types, or INT with REAL | BOOL |
| <, >, <=, >= | equal non-BOOL types, or INT with REAL | BOOL |

INT and REAL may be mixed; the INT is widened to REAL (choice). Assigning REAL to INT is
a type error. Integer `/` truncates toward zero and MOD takes the sign of the dividend:
-7 / 2 = -3, -7 MOD 3 = -1.

## 5. Scan cycle

Each scan, at simulated time t (Bolton pp. 106 to 107, "mass I/O copying"):

1. Copy every input into the input image. An input event at time t_e is first seen by
   the first scan that starts at or after t_e.
2. Execute the statements in order, reading inputs from the image and writing outputs to
   the output image. Function blocks are evaluated with the scan start time t.
3. Transfer the output image.
4. Advance t by the scan period.

Time is simulated, so results never depend on the speed of the computer. A run is
limited to 100000 scans.

Each scan returns its working (decision D11): the input image, every executed statement
with its source line, expression text and value, every IF condition with its value, every
function-block call with its inputs and outputs, the output image and the state of every
instance.

## 6. Function blocks

Timer shapes follow Bolton Figure 9.3 (p. 226); counters follow section 10.1 (p. 245).
Rules marked (choice) are Quantic subset choices where the books do not decide.

**TON (on-delay).** While IN is TRUE, ET = t - t_start, capped at PT, where t_start is the
scan in which IN was first seen TRUE; Q = (ET >= PT). When IN is FALSE, Q = FALSE and
ET = 0 (choice: immediate reset).

**TOF (off-delay).** While IN is TRUE, Q = TRUE and ET = 0. When IN falls, timing starts:
ET = t - t_fall capped at PT, and Q stays TRUE until ET >= PT. After expiry ET holds PT
until IN is TRUE again (choice). Before IN has ever been TRUE, Q = FALSE.

**TP (pulse).** A rising edge of IN starts a pulse: Q = TRUE while ET = t - t_start < PT,
whatever IN does. A rising edge during a pulse is ignored (choice: not retriggerable).
After the pulse, ET holds PT while IN stays TRUE and returns to 0 when IN is FALSE
(choice).

**CTU (up counter).** Each rising edge of CU adds 1. R sets CV = 0 and takes priority
(choice). Q = (CV >= PV).

**CTD (down counter).** LD loads CV = PV and takes priority (choice). Each rising edge of
CD subtracts 1. Q = (CV <= 0).

**CTUD (up-down counter).** Priority (choice): R (CV = 0), then LD (CV = PV), then edges.
A rising CU adds 1, a rising CD subtracts 1, and both rising in the same scan leave CV
unchanged (choice). QU = (CV >= PV), QD = (CV <= 0).

All counters saturate at the INT limits instead of wrapping (choice). Edges are detected
between successive calls of the same instance; the first call compares with FALSE. A zero
PT gives: TON on in the same scan, TOF off in the falling scan, TP no pulse.

## 7. Errors

Static errors are found before any scan runs; runtime errors stop the run at that scan,
as a PLC faults, keeping the scans already completed. Each is a diagnostic whose
`element_ref.field` is `source:<line>:<column>`.

| Code | Meaning |
|---|---|
| SYNTAX | The text does not follow the grammar |
| UNSUPPORTED_SYNTAX | A construct outside the subset |
| UNKNOWN_NAME, UNKNOWN_TYPE | Undeclared name, unknown type or block input |
| DUPLICATE_NAME | Name or block input given twice |
| TYPE_MISMATCH | Operand, assignment, condition or block input of the wrong type |
| READ_ONLY | Assignment to an input |
| INT_OVERFLOW | INT result or constant outside -32768 to 32767 |
| DIVIDE_BY_ZERO | / or MOD by zero |
| REAL_RANGE | REAL result not finite or not real |
| TIME_PRECISION | Duration that is not a whole number of milliseconds |
| INPUT_EVENT, SCAN_PERIOD, RUN_LIMIT | Invalid run settings |

Program text is only tokenised and interpreted by our own code. It is never passed to
Python's eval or exec, a shell, or any external runtime.
