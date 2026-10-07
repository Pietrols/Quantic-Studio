# Textbook load-flow solver

This package implements a balanced polar Newton-Raphson load-flow solver using NumPy only for numerical arrays and the linear solve. It builds Y-bus from the engine-neutral power network contract and returns the load-flow result contract. It has no dependency on or import from an engine adapter.

The implementation equations are derived in `docs/learning/newton-raphson-load-flow.md`. The solver's test reference is the original closed-form two-bus fixture; the three-bus fixture checks per-iteration mismatch history. Five-bus and fourteen-bus fixtures are cross-check cases without stored answers.
