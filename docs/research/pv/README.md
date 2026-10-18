# PV reference-product research

WP-2.23, ChatGPT, 2026-10-18. Research-first continuation after power, not an
authorisation to build. Adapted from [power research rules](../power/README.md).
We study public behaviour and independently design functionality; we do not recover
proprietary code or copy vendor text, imagery, interfaces or component datasets.

## Rules

1. Public sources only: official help, release notes, openly published technical
   papers, training, lawful user accounts and public discussions. No leaked,
   cracked or paywalled copies and no sign-in bypass.
2. Paraphrase. Do not commit copied paragraphs, figures, screenshots, worked cases,
   weather files or component libraries. A software licence does not license data.
3. Every factual claim has a dossier source ID, URL, title/type and access date.
   S means explicitly stated/seen in a source, not necessarily executed; I means
   our inference/proposal; U means unresolved, never absent. Retain subset,
   edition and commercial-module qualifiers. No runtime parity is claimed here.
4. No guessed numbers: model constants, limits and defaults require a readable
   source and exact model/version context. No vendor default becomes a site value.
5. Write explicit gaps, their reason and the evidence needed to close them. Public
   evidence cannot prove exhaustive feature absence. Record date and version drift.
6. Weather provenance includes dataset/version, permissions, location, reference
   period, time zone, timestamp convention, interval and measured/synthetic status.
   Energy, average power and irradiance must not be conflated.
7. Yield forecasting is not an electrical safety, grid-code, ride-through or
   protection certificate. Follow the power suite's jurisdiction and source gates.

## Layout

- [pvsyst.md](pvsyst.md): full first-pass PVsyst dossier.
- [other-products.md](other-products.md): lighter HelioScope, SAM, PV*SOL and
  PlantPredict dossier, shared capability table and open-engine/licence crosswalk.

## Dossier template

```
# <Product or comparison group>
## 1. Identity: vendor, current version, editions/licensing, platforms
## 2. Sources: numbered table (URL, title, type, accessed)
## 3. Architecture and data model: projects, variants, component/weather libraries,
##    geometry, electrical topology, scenarios, units and validation
## 4. Element catalogue: object, parameter name, unit and physical meaning
## 5. Studies and modules: purpose, method, options, inputs, outputs, reports,
##    alerts, supported standards and boundaries
## 6. Workflow and interface: editors, results, reports, automation, imports/exports
## 7. User value and complaints: public user evidence separated from vendor claims
## 8. Engines implied: inferred algorithms, open candidates/licences, verifying books
## 9. Gaps: unknowns, evidence/access blockers and closure route
```

## Capability-table convention

`| ID | Capability and scope | PVsyst | HelioScope | SAM | PV*SOL | PlantPredict |`

Each product cell starts S, I or U, includes its source and scope qualifier.
No score or feature count means product quality or verified numerical accuracy.
Quantic proposals stay outside product cells. Existing PV contracts/earlier
placeholders are not evidence that a PV energy-yield engine is implemented.
