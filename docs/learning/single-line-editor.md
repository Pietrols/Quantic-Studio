# A diagram is a view of an engineering model

A single-line diagram represents a balanced network graph. Buses are electrical
connection nodes. Lines and transformers join buses; equipment is connected to
its declared bus. The solver reads the network contract, not screen coordinates.
Moving a symbol therefore cannot change resistance, voltage base or power.

Quantic's canvas defines nodes, ports and edges without electrical equations.
Each port has a kind and direction; matching ports can connect. The power layer
adds bus/equipment rules and creates the relevant network references. A future
block or SCADA workspace can use the same graph mechanics with its own port kinds.
A ladder program is a different grid structure, not another electrical graph.

Network edits are made on copies. Browser validation uses the current or archived
network schema, then checks IDs and bus references. The API repeats core checks
and additionally protects retained asset and motor-study references. A valid JSON
shape still may have an infeasible operating point or unsupported solver model;
the resulting diagnostic belongs in the study response, not a made-up result.

The generic element property editor retains every allowed optional field. This
matters for fault data and generator limits that a simplified symbol view would
otherwise drop. New equipment templates use null placeholders: the user must
supply ratings and impedance values. Lines use ohm/km and km. Transformer r/x use
its own MVA and LV-kV base. Motor-start nameplate data remain study-local under the
existing contract, not silently converted into network loads by the diagram.

Core's model ID selects the representation. Physical asset IDs can link that
representation to another suite. Opening or saving a power model must preserve
foreign payloads and those identity links. Etag saves detect newer API edits.
A failed save leaves the browser's draft intact. Studies run only after a save,
so displayed numerical results cannot quietly refer to an older engineering draft.

Presentation layout is stored only in this browser, per project/model. It is
separate from the contract and solver input hash. Shared/exportable layout needs
a later contract rather than an undocumented field in the electrical payload.

Results report both numerical status and engineering checks. Unavailable duties
are n/a. A converged load flow may violate voltage/reactive limits; a calculated
motor-start dip may exceed the selected limit. Reports retain assumptions,
diagnostics and provenance. The editor displays these outcomes and lets the user
download the underlying report/result rather than hiding uncertainty behind green
symbols. Tests verify property round trips, legacy versions, typed non-power ports,
failed API flows and all three real studies in a browser.
