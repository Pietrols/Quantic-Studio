# Power reference-product research

Purpose: before building more of the power suite, learn in detail what ETAP, DIgSILENT
PowerFactory and PowerWorld Simulator let an engineer do, so every later engine and
interface package is chosen from evidence, not guesswork. Peter's ruling (2026-10-15):
research comes first for as long as it takes. We recreate the functionality in our own
way; we never copy code, text, screenshots, icons or data.

## Rules

1. **Public sources only:** vendor product pages, brochures and datasheets, user guides
   and help pages the vendor publishes openly, release notes, training and webinar
   pages, conference papers, theses, user articles, forum posts and video descriptions.
   Never use leaked, cracked or paywalled copies.
2. **Paraphrase, never copy.** Describe what a feature does in our own words. Short
   names of menus, studies and parameters may be recorded as facts. No copied
   paragraphs, tables, figures or screenshots.
3. **Cite every claim:** each fact lists the source number from the dossier's source
   table (URL, title, type, access date). Mark anything not directly read as
   `inferred` and say from what.
4. **No guessed numbers.** Defaults, limits or constants are recorded only when a source
   states them, with that source.
5. **Write as you go** and push often. A dossier is never finished until its gaps list
   is empty or every gap names why it cannot be closed from public sources.

## Layout

- `etap.md`, `powerfactory.md`, `powerworld.md`: one dossier per product, using the
  template below.
- `parity-matrix.md`: one row per capability across the three products, with our status
  and the owned book that will verify it.
- `engines.md`: the calculation engines the products imply (methods, standards,
  models), which ones we have, and which we lack.

## Dossier template

```
# <Product>
## 1. Identity: vendor, current version, editions and licensing, platforms
## 2. Sources: numbered table (URL, title, type, accessed)
## 3. Architecture and data model: project, network database, libraries, study cases,
##    scenarios, revisions, variants, units, data validation
## 4. Element catalogue: each element type, its key parameters (name, unit, meaning)
## 5. Studies and modules: for each, purpose, method, options, inputs, outputs,
##    reports, alerts, standards supported, limits
## 6. Workflow and interface: editors, views, result display, alerts, reports,
##    libraries, scripting and automation, import and export formats
## 7. What users value and what they complain about (articles, forums)
## 8. Engines implied: algorithms and models behind each study
## 9. Gaps: what could not be found, and why
```

## Parity matrix row

`| ID | Area | Capability | ETAP | PowerFactory | PowerWorld | Quantic status | Verifying book | Sources |`

Status values: `none`, `partial`, `done`. Product cells: `yes`, `no`, `module <name>`,
or `unknown`.
