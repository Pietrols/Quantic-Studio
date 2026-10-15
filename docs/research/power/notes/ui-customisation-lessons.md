# Interface customisation: what ETAP and PowerFactory do, and what Quantic should do (WP-2.10)

Peter's priority for the workbench redesign is **customisability** (forms plus JSON),
with a white and grey look and an ETAP-PowerFactory blend. This note collects the
evidence from both dossiers, so the redesign WP starts from facts.

Sources:

- P82: PowerFactory's "Customising the PowerFactory User Interface" paper page, read
  2026-10-15;
- PowerFactory dossier sec. 6;
- ETAP dossier sec. 6 and `notes/etap-platform.md` (E-numbered sources there);
- E91: ETAP 2026 release notes.

## PowerFactory: three layers of customisation [P82]

1. **Per user** (user settings):
   - light or dark mode and background colours;
   - hide unneeded dialog pages and parameters;
   - split and tabbed window layout (diagrams, data managers and reports in tab groups;
     pinnable panels);
   - editable hot keys;
   - a personal Quick Access menu.
2. **Per group, by the administrator** (profiles):
   - users belong to groups; profiles are assigned to groups (built-ins "Standard" and
     "Base Package");
   - a profile can:
     - add or remove toolbar icons and define new toolboxes;
     - publish scripts as a "User-defined Tools" toolbox with custom icons;
     - restrict context menus;
     - **remove whole dialog pages or individual attributes**.
   - Licence modules are also granted by group.
3. **Per project** (network representation):
   - map services (WMS and WMTS);
   - **custom element symbols** from a graphical editor;
   - **user-defined colouring filters**.

The paper page does not say how profiles are stored or shared, and some options need the
Team Edition or the administrator account.

## ETAP (dossier)

- **Study modes:** 27 in version 16, each with its own toolbar.
- **Theme manager:** colour by voltage, area, grounding, earthing system or switch state;
  per-diagram themes; alert colours.
- **Templates and project and theme toolbars.**
- **2026 additions [E91]:**
  - Network Manager (tabular editing, still limited);
  - Data Manager across revisions;
  - Report Manager with comparison and Excel export;
  - high-DPI support;
  - iSLD result animation.

## What this means for Quantic's workbench

Quantic can match all three PowerFactory layers with **declarative JSON configuration**.
Both products configure through dialogs and an administrator database. Version-controlled
JSON is something neither offers, and it fits Peter's "forms plus JSON" goal: every
setting edited in a form is also a readable, diffable file.

| Layer | Quantic mechanism (proposal) |
| --- | --- |
| User | `user-settings.json`: theme (white and grey default, no blue), layout, hot keys, quick-access list, hidden fields per element type |
| Team or profile | `profiles/<name>.json` in the project or organisation repo: toolbar sets, visible studies, hidden or read-only fields, element libraries, report templates. Shared by git, not an admin database |
| Project | `project/display.json`: colouring rules (filters as expressions over results), symbol sets (SVG), map layers |
| Element forms | Generated from the JSON Schema contracts. Field order, grouping, labels and units come from a `ui` annotation layer, so customising a form is editing a schema overlay, not code |
| Tools and scripts | User scripts registered in a profile appear as toolbar buttons (PowerFactory's user-defined tools), running through the CLI and API we already have |
| Tables | A spreadsheet view of any element type, editable, from day one. ETAP only reached this in 2026, and with limits |

**Constraint to respect:** hiding a field in a form must never change the calculation.
Hidden fields keep their values and appear in the report's input section. PowerFactory's
page does not say how it handles this.

This note feeds the workbench redesign WP (BOARD follow-up "Workbench redesign").
