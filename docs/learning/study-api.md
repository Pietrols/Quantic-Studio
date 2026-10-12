# From project files to an API study

The API is an orchestration boundary, not another electrical solver. It receives
a project path and study ID, loads the versioned manifest through core, and finds
the study's model binding. This matters when a plant and a feeder coexist in one
project: a mathematically valid result from the wrong network is still wrong.

Core owns schemas and references. The domain adapter owns equations and numerical
conversion. The report package owns presentation. The API composes these layers
without importing pandapower directly or moving equations into HTTP handlers.

Every execution uses a validated network/request snapshot in a separate worker
process. Timeout terminates that process, unlike a background thread whose caller
can time out while calculation continues. Worker-count, bus-count, file-size and
iteration limits are operational policies. They do not replace engineering limits
such as the user's acceptable motor-start voltage dip.

The API returns existing result contracts and their solver/version/input hash.
Motor-start and fault studies hash the selected network and request through their
existing entry points. API load flow uses the in-memory solver's canonical input
hash, including the request; CLI legacy load flow retains its network-byte hash.
An HTTP 200 means a contract-shaped study response was produced. Inspect the
study's convergence, availability and compliance before treating it as acceptable.
Unknown or invalid input returns named diagnostics rather than numerical zeros.

Editing needs a second boundary. Read a model and retain its etag, a SHA-256 of
its current bytes. Submit that etag with the edited payload. If it changed, reload
and reconcile instead of replacing someone else's save. The API validates bus
references and retained asset/motor bindings, then replaces just the selected
model file. Other domain representations and the manifest remain intact.

Path confinement and an explicit project root keep a caller from selecting any
arbitrary machine file. Loopback binding and browser-origin checks keep this first
slice local. They are not authentication for public deployment. Multiple service
processes or external file writers need a stronger coordinated locking design.

The added model read/save routes are the recorded WP-1.5 design change required
by the approved editor package. Contracts remain frozen; browser layout is not
stored in electrical input. The next workbench can therefore edit a network, run
its study and inspect traceable results through one service boundary.
