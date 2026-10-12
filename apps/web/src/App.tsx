import { useEffect, useMemo, useState } from "react";
import type { Connection } from "@xyflow/react";
import { positions, type DiagramNode, type Layout } from "@quantic/canvas";
import {
  collections,
  toGraph,
  reference,
  element,
  replaceElement,
  removeElement,
  addElement,
  validateNetwork,
  validConnection,
  connectEquipment,
  assetsForModel,
  type Network,
  type Collection,
  type Ref,
} from "@quantic/power";
import {
  api,
  ApiError,
  type ProjectInfo,
  type ModelInfo,
  type StudyResponse,
  type Diagnostic,
} from "./api";
import { GraphCanvas } from "./GraphCanvas";
import { Symbol } from "./Symbol";
const emptyTemplates: Record<Collection, Record<string, unknown>> = {
  buses: { bus_id: "", vn_kv: null, bus_type: "pq" },
  lines: {
    line_id: "",
    from_bus: "",
    to_bus: "",
    length_km: null,
    r_ohm_per_km: null,
    x_ohm_per_km: null,
  },
  transformers: {
    transformer_id: "",
    hv_bus: "",
    lv_bus: "",
    sn_mva: null,
    vn_hv_kv: null,
    vn_lv_kv: null,
    r_pu: null,
    x_pu: null,
  },
  loads: { load_id: "", bus_id: "", p_mw: null, q_mvar: null },
  generators: {
    generator_id: "",
    bus_id: "",
    p_mw: null,
    vm_setpoint_pu: null,
  },
  external_grids: {
    external_grid_id: "",
    bus_id: "",
    vm_setpoint_pu: null,
    va_setpoint_degree: null,
  },
  shunts: { shunt_id: "", bus_id: "", p_mw: null, q_mvar: null },
};
function storedLayout(key: string): Layout {
  try {
    const value = JSON.parse(localStorage.getItem(key) || "{}");
    return value && typeof value === "object" && !Array.isArray(value)
      ? value
      : {};
  } catch {
    return {};
  }
}
function textError(error: unknown): Diagnostic[] {
  return error instanceof ApiError
    ? error.diagnostics
    : [
        {
          code: "REQUEST_FAILED",
          message: error instanceof Error ? error.message : String(error),
        },
      ];
}
function download(name: string, content: string, type: string, base64 = false) {
  const bytes = base64
    ? Uint8Array.from(atob(content), (c) => c.charCodeAt(0))
    : content;
  const url = URL.createObjectURL(new Blob([bytes], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
type ResultView = {
  status?: string;
  convergence?: { converged: boolean };
  diagnostics: Diagnostic[];
  bus_results?: Record<string, unknown>[];
  case_results?: {
    case: string;
    bus_results: Record<string, unknown>[];
    diagnostics: Diagnostic[];
  }[];
  passes_limit?: boolean | null;
  dip_limit_percent?: number;
};
function number(value: unknown) {
  return typeof value === "number" ? value.toFixed(6) : "n/a";
}
export function App() {
  const [paths, setPaths] = useState<string[]>([]),
    [path, setPath] = useState(""),
    [info, setInfo] = useState<ProjectInfo>(),
    [modelId, setModelId] = useState(""),
    [model, setModel] = useState<ModelInfo>(),
    [network, setNetwork] = useState<Network>(),
    [dirty, setDirty] = useState(false),
    [busy, setBusy] = useState(false),
    [notice, setNotice] = useState("Connecting to local project API..."),
    [issues, setIssues] = useState<Diagnostic[]>([]),
    [layout, setLayout] = useState<Layout>({}),
    [selection, setSelection] = useState<Ref>(),
    [properties, setProperties] = useState(""),
    [propertyDirty, setPropertyDirty] = useState(false),
    [wholeJson, setWholeJson] = useState(false),
    [studyId, setStudyId] = useState(""),
    [result, setResult] = useState<StudyResponse>(),
    [formats, setFormats] = useState(["markdown"]),
    [format, setFormat] = useState("markdown"),
    [addKind, setAddKind] = useState<Collection | null>(null),
    [addJson, setAddJson] = useState("");
  const layoutKey = `quantic.layout.v1:${path}:${modelId}`;
  useEffect(() => {
    let active = true;
    Promise.all([api.projects(), api.health()])
      .then(([projects, health]) => {
        if (!active) return;
        setPaths(projects.projects);
        setPath(
          projects.projects.includes("multi_domain")
            ? "multi_domain"
            : projects.projects[0] || "",
        );
        setFormats(health.report_formats);
        setNotice("Connected to local API");
      })
      .catch((e) => {
        if (active) {
          setIssues(textError(e));
          setNotice("Start the local API to open a project");
        }
      });
    return () => {
      active = false;
    };
  }, []);
  useEffect(() => {
    if (!path) return;
    let active = true;
    setModel(undefined);
    setNetwork(undefined);
    setInfo(undefined);
    setResult(undefined);
    setSelection(undefined);
    setDirty(false);
    api
      .project(path)
      .then((value) => {
        if (!active) return;
        setInfo(value);
        setModelId(
          value.models.find((m) => m.model_type === "power.network")
            ?.model_id ??
            value.models[0]?.model_id ??
            "",
        );
        setIssues(value.diagnostics);
      })
      .catch((e) => active && setIssues(textError(e)));
    return () => {
      active = false;
    };
  }, [path]);
  useEffect(() => {
    if (!path || !modelId) return;
    let active = true;
    setModel(undefined);
    setNetwork(undefined);
    setNotice("Opening model...");
    setSelection(undefined);
    setResult(undefined);
    setDirty(false);
    setWholeJson(false);
    api
      .model(path, modelId)
      .then((value) => {
        if (!active) return;
        setModel(value);
        setNetwork(
          value.model_type === "power.network" ? value.data : undefined,
        );
        setLayout(storedLayout(layoutKey));
        setIssues(value.diagnostics);
        setStudyId(
          info?.studies.find((s) => s.model_id === modelId)?.study_id || "",
        );
        setNotice("Model opened");
      })
      .catch((e) => active && setIssues(textError(e)));
    return () => {
      active = false;
    };
  }, [path, modelId, info]);
  const assetMap = useMemo(
    () => assetsForModel(info?.assets ?? [], modelId),
    [info, modelId],
  );
  const graph = useMemo(
    () =>
      network ? toGraph(network, layout, assetMap) : { nodes: [], edges: [] },
    [network, layout, assetMap],
  );
  const decorated = useMemo(
    () =>
      graph.nodes.map((node) => ({
        ...node,
        data: {
          ...node.data,
          glyph: <Symbol kind={reference(node.id).collection} />,
        },
      })),
    [graph.nodes],
  );
  function confirmLeave() {
    return (
      (!dirty && !propertyDirty) ||
      window.confirm("Discard unsaved engineering changes?")
    );
  }
  function select(id: string) {
    if (
      !network ||
      (propertyDirty && !window.confirm("Discard unapplied property changes?"))
    )
      return;
    setPropertyDirty(false);
    const ref = reference(id);
    const value = element(network, ref);
    if (value) {
      setSelection(ref);
      setProperties(JSON.stringify(value, null, 2));
      setWholeJson(false);
    }
  }
  function edit(next: Network) {
    const errors = validateNetwork(next);
    if (errors.length) {
      setIssues(errors);
      return false;
    }
    setNetwork(next);
    setDirty(true);
    setResult(undefined);
    setNotice("Engineering changes are not saved");
    setIssues([]);
    return true;
  }
  function apply() {
    try {
      const value = JSON.parse(properties);
      if (wholeJson) {
        if (edit(value)) {
          setSelection(undefined);
          setPropertyDirty(false);
        }
      } else if (network && selection) {
        if (edit(replaceElement(network, selection, value)))
          setPropertyDirty(false);
      }
    } catch (e) {
      setIssues([{ code: "JSON_INVALID", message: String(e) }]);
    }
  }
  function nodesChanged(nodes: DiagramNode[]) {
    const next = positions(nodes);
    setLayout(next);
    try {
      localStorage.setItem(layoutKey, JSON.stringify(next));
    } catch {
      setNotice(
        "Layout storage is unavailable; electrical inputs are unaffected",
      );
    }
  }
  function connect(connection: Connection) {
    if (!network) return;
    const from = reference(connection.source),
      to = reference(connection.target);
    if (to.collection === "buses") {
      const kind: Collection =
        network.buses.find((b) => b.bus_id === from.id)?.vn_kv ===
        network.buses.find((b) => b.bus_id === to.id)?.vn_kv
          ? "lines"
          : "transformers";
      setAddKind(kind);
      setAddJson(
        JSON.stringify(
          {
            ...emptyTemplates[kind],
            ...(kind === "lines"
              ? { from_bus: from.id, to_bus: to.id }
              : { hv_bus: from.id, lv_bus: to.id }),
          },
          null,
          2,
        ),
      );
    } else {
      try {
        edit(connectEquipment(network, connection.source, connection.target));
      } catch (e) {
        setIssues(textError(e));
      }
    }
  }
  async function save() {
    if (!model || !network) return;
    setBusy(true);
    try {
      const response = await api.save(path, model, network);
      setModel({ ...model, data: network, etag: response.etag });
      setDirty(false);
      setIssues([]);
      setNotice("Model saved. Other project files preserved.");
    } catch (e) {
      setIssues(textError(e));
      setNotice("Save failed; your edits remain in this window");
    } finally {
      setBusy(false);
    }
  }
  async function run() {
    if (dirty || propertyDirty) {
      setNotice("Save engineering changes before running a study");
      return;
    }
    setBusy(true);
    setResult(undefined);
    try {
      const response = await api.run(path, studyId, format);
      setResult(response);
      setIssues(response.project_diagnostics);
      setNotice(
        "Study response received. Review status, limits and diagnostics.",
      );
    } catch (e) {
      setIssues(textError(e));
      setNotice("Study failed; no verified result is shown");
    } finally {
      setBusy(false);
    }
  }
  const chosenStudy = info?.studies.find((s) => s.study_id === studyId);
  const view = result?.result as unknown as ResultView | undefined;
  const numericalIssues = view
    ? [
        ...(view.diagnostics ?? []),
        ...(view.case_results?.flatMap((c) => c.diagnostics) ?? []),
      ]
    : [];
  const status = view
    ? result?.study_type === "loadflow"
      ? view.convergence?.converged
        ? "CONVERGED"
        : "NOT CONVERGED"
      : (view.status ?? "unknown").toUpperCase()
    : "";
  const rows = view
    ? (view.case_results?.flatMap((c) =>
        c.bus_results.map((r) => ({ ...r, case: c.case })),
      ) ??
      view.bus_results ??
      [])
    : [];
  return (
    <div className="app-shell">
      <aside className="rail">
        <a className="brand" href="#workspace" aria-label="Quantic Studio">
          <span className="brand-mark">Q</span>
          <span>
            QUANTIC<strong>STUDIO</strong>
          </span>
        </a>
        <div className="rail-label">ENGINEERING SUITES</div>
        <div className="suite active">
          <span>01</span>Power systems
        </div>
        <div className="suite future">
          <span>02</span>Industrial automation<small>Planned</small>
        </div>
        <div className="suite future">
          <span>03</span>Electronics & control<small>Planned</small>
        </div>
        <div className="suite future">
          <span>04</span>Solar PV<small>Planned</small>
        </div>
        <div className="rail-label">PROJECT</div>
        <label className="rail-field">
          Open project
          <select
            aria-label="Project"
            value={path}
            disabled={busy}
            onChange={(e) => confirmLeave() && setPath(e.target.value)}
          >
            <option value="">Select project</option>
            {paths.map((p) => (
              <option key={p}>{p}</option>
            ))}
          </select>
        </label>
        <div className="model-list" aria-label="Project models">
          {info?.models.map((m) => (
            <button
              key={m.model_id}
              className={m.model_id === modelId ? "model active" : "model"}
              disabled={busy}
              onClick={() => confirmLeave() && setModelId(m.model_id)}
            >
              <span className="model-dot" />
              <span>
                {m.model_id}
                <small>{m.model_type}</small>
              </span>
            </button>
          ))}
        </div>
        <div className="rail-footer">
          <span className="online-dot" />
          Local project service
          <br />
          <small>Versioned models. Traceable results.</small>
        </div>
      </aside>
      <main id="workspace">
        <header className="workspace-header">
          <div>
            <div className="eyebrow">POWER WORKSPACE / SINGLE-LINE MODEL</div>
            <h1>{info?.name || "Open an engineering project"}</h1>
          </div>
          <div
            className={
              "save-state " + (dirty || propertyDirty ? "unsaved" : "")
            }
          >
            <span>
              {propertyDirty
                ? "Unapplied properties"
                : dirty
                  ? "Unsaved changes"
                  : "Saved model"}
            </span>
            <button
              disabled={!dirty || propertyDirty || busy || !network}
              onClick={save}
            >
              {busy ? "Working..." : "Save model"}
            </button>
          </div>
        </header>
        <section className="toolbar">
          <div className="model-heading">
            <strong>{modelId || "No model"}</strong>
            <span>
              {network
                ? `${network.buses.length} buses | ${network.lines.length + network.transformers.length} branches`
                : "Model data"}
            </span>
          </div>
          <button
            disabled={!network || busy}
            onClick={() => {
              setAddKind("buses");
              setAddJson(JSON.stringify(emptyTemplates.buses, null, 2));
            }}
          >
            + Add element
          </button>
          <button
            disabled={!network || busy}
            onClick={() => {
              if (
                propertyDirty &&
                !window.confirm("Discard unapplied property changes?")
              )
                return;
              setPropertyDirty(false);
              setWholeJson(true);
              setSelection(undefined);
              setProperties(JSON.stringify(network, null, 2));
            }}
          >
            Model JSON
          </button>
          <button
            disabled={!network}
            onClick={() => {
              setLayout({});
              localStorage.removeItem(layoutKey);
              setNotice("Diagram layout reset; electrical inputs unchanged");
            }}
          >
            Reset layout
          </button>
          <span className="toolbar-divider" />
          <label>
            Study
            <select
              aria-label="Study"
              value={studyId}
              disabled={busy || !network}
              onChange={(e) => {
                setStudyId(e.target.value);
                setResult(undefined);
              }}
            >
              {info?.studies
                .filter((s) => s.model_id === modelId)
                .map((s) => (
                  <option key={s.study_id} value={s.study_id}>
                    {s.study_id}
                  </option>
                ))}
            </select>
          </label>
          <label>
            Report
            <select
              aria-label="Report format"
              value={format}
              disabled={busy}
              onChange={(e) => setFormat(e.target.value)}
            >
              {formats.map((f) => (
                <option key={f} value={f}>
                  {f === "pdf" ? "PDF" : "Markdown"}
                </option>
              ))}
            </select>
          </label>
          <button
            className="primary"
            disabled={
              busy ||
              dirty ||
              propertyDirty ||
              !!addKind ||
              !chosenStudy ||
              !network
            }
            onClick={run}
          >
            Run study
          </button>
        </section>
        <div className="status-line" role="status">
          <span className={dirty ? "amber-dot" : "online-dot"} />
          {notice}
          <span className="layout-note">
            Drag symbols to arrange. Layout is browser-local.
          </span>
        </div>
        <div className="work-area">
          <section className="canvas-area" aria-label="Engineering diagram">
            {network ? (
              <GraphCanvas
                key={modelId}
                nodes={decorated}
                edges={graph.edges}
                onNodes={nodesChanged}
                onSelect={select}
                onConnect={connect}
                valid={(c) =>
                  validConnection(
                    network,
                    graph.nodes,
                    c.source,
                    c.target,
                    c.sourceHandle || "",
                    c.targetHandle || "",
                  )
                }
              />
            ) : model ? (
              <div className="foreign-model">
                <h2>Stored model</h2>
                <p>
                  {model.model_type} is retained in this project. Its editor and
                  engine are planned.
                </p>
                <pre>{JSON.stringify(model.data, null, 2)}</pre>
              </div>
            ) : (
              <div className="empty">
                <span className="empty-icon">Q</span>
                <h2>One project, specialised models</h2>
                <p>
                  Start the local API, then select a project and power model.
                </p>
                <code>uv run qe-api --project-root examples</code>
              </div>
            )}
          </section>
          <aside className="inspector">
            <div className="panel-title">
              <span>PROPERTIES</span>
              <span className="panel-count">
                {selection
                  ? selection.collection
                  : wholeJson
                    ? "Model"
                    : "Selection"}
              </span>
            </div>
            {selection || wholeJson ? (
              <>
                <h2>{wholeJson ? "Complete model" : selection?.id}</h2>
                {selection &&
                assetMap[selection.collection + ":" + selection.id]?.length ? (
                  <p>
                    Linked asset:{" "}
                    {assetMap[selection.collection + ":" + selection.id].join(
                      ", ",
                    )}
                  </p>
                ) : null}
                <p className="hint">
                  Edit explicit values. Existing optional fields are retained.
                  kV, MW, Mvar and impedance bases follow the contract.
                </p>
                <label className="editor-label">
                  {wholeJson ? "Model payload" : "Element properties"}
                  <textarea
                    aria-label={
                      wholeJson ? "Model payload" : "Element properties"
                    }
                    spellCheck={false}
                    value={properties}
                    onChange={(e) => {
                      setProperties(e.target.value);
                      setPropertyDirty(true);
                      setResult(undefined);
                      setNotice(
                        "Apply property changes before saving or running",
                      );
                    }}
                  />
                </label>
                <button className="full-width" disabled={busy} onClick={apply}>
                  Apply properties
                </button>
                {selection ? (
                  <button
                    className="danger full-width"
                    disabled={propertyDirty || busy}
                    onClick={() => {
                      if (network && edit(removeElement(network, selection)))
                        setSelection(undefined);
                    }}
                  >
                    Remove element
                  </button>
                ) : null}
              </>
            ) : (
              <div className="inspector-empty">
                <h2>Inspect an element</h2>
                <p>
                  Select a bus, equipment symbol or branch to edit its contract
                  fields.
                </p>
                <dl>
                  <dt>Model identity</dt>
                  <dd>{modelId || "None"}</dd>
                  <dt>Linked physical assets</dt>
                  <dd>{Object.keys(assetMap).length}</dd>
                  <dt>Layout</dt>
                  <dd>Separate from solver inputs</dd>
                </dl>
              </div>
            )}
          </aside>
        </div>
        {issues.length || numericalIssues.length ? (
          <section className="diagnostics" aria-label="Diagnostics">
            <h2>
              Diagnostics <span>{issues.length + numericalIssues.length}</span>
            </h2>
            {[...issues, ...numericalIssues].map((d, i) => (
              <div key={i} className={"diagnostic " + (d.severity || "error")}>
                <strong>{d.code}</strong>
                <span>
                  {d.element_ref
                    ? `${d.element_ref.element_type}:${d.element_ref.element_id}.${d.element_ref.field} - `
                    : ""}
                  {d.message}
                </span>
              </div>
            ))}
          </section>
        ) : null}
        {result ? (
          <section className="results" aria-label="Study results">
            <div className="results-heading">
              <div>
                <div className="eyebrow">
                  {result.study_type.toUpperCase()} / {result.model_id}
                </div>
                <h2>
                  {status}
                  {view?.passes_limit !== undefined
                    ? ` | Dip limit ${view.passes_limit === null ? "UNKNOWN" : view.passes_limit ? "PASS" : "FAIL"}`
                    : ""}
                </h2>
                {view?.dip_limit_percent !== undefined ? (
                  <p>
                    User limit: {view.dip_limit_percent}% | dip = 100 ×
                    (pre-start - locked rotor) / pre-start
                  </p>
                ) : null}
              </div>
              <div className="download-actions">
                <button
                  onClick={() =>
                    download(
                      `${studyId}-report.md`,
                      result.report_markdown,
                      "text/markdown",
                    )
                  }
                >
                  Download Markdown
                </button>
                {result.report_pdf_base64 ? (
                  <button
                    onClick={() =>
                      download(
                        `${studyId}-report.pdf`,
                        result.report_pdf_base64!,
                        "application/pdf",
                        true,
                      )
                    }
                  >
                    Download PDF
                  </button>
                ) : null}
                <button
                  onClick={() =>
                    download(
                      `${studyId}-results.json`,
                      JSON.stringify(result.result, null, 2),
                      "application/json",
                    )
                  }
                >
                  Results JSON
                </button>
              </div>
            </div>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th scope="col">Bus</th>
                    {result.study_type === "loadflow" ? (
                      <>
                        <th scope="col">Voltage (pu)</th>
                        <th scope="col">Angle (°)</th>
                      </>
                    ) : result.study_type === "motorstart" ? (
                      <>
                        <th scope="col">Pre-start (pu)</th>
                        <th scope="col">Locked rotor (pu)</th>
                        <th scope="col">Dip (%)</th>
                        <th scope="col">Limit</th>
                      </>
                    ) : (
                      <>
                        <th scope="col">Case</th>
                        <th scope="col">Ik'' (kA RMS)</th>
                        <th scope="col">ip (kA peak)</th>
                        <th scope="col">Ith (kA RMS)</th>
                      </>
                    )}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r, i) => {
                    const data = r as unknown as Record<string, unknown>;
                    return (
                      <tr key={i}>
                        <th scope="row">{String(data.bus_id)}</th>
                        {result.study_type === "loadflow" ? (
                          <>
                            <td>{number(data.vm_pu)}</td>
                            <td>{number(data.va_degree)}</td>
                          </>
                        ) : result.study_type === "motorstart" ? (
                          <>
                            <td>{number(data.prestart_vm_pu)}</td>
                            <td>{number(data.locked_rotor_vm_pu)}</td>
                            <td>{number(data.dip_percent)}</td>
                            <td>
                              {data.passes_limit === null
                                ? "UNKNOWN"
                                : data.passes_limit
                                  ? "PASS"
                                  : "FAIL"}
                            </td>
                          </>
                        ) : (
                          <>
                            <td>{String(data.case)}</td>
                            <td>{number(data.ikss_ka)}</td>
                            <td>{number(data.ip_ka)}</td>
                            <td>{number(data.ith_ka)}</td>
                          </>
                        )}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <details>
              <summary>Report, assumptions and provenance</summary>
              <pre>{result.report_markdown}</pre>
            </details>
          </section>
        ) : null}
        <footer className="workspace-footer">
          Quantic Studio <span>Power systems | Balanced static studies</span>
          <span>
            Solver data and limitations remain visible in every report.
          </span>
        </footer>
      </main>
      {addKind ? (
        <div className="modal-backdrop">
          <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="add-title"
          >
            <h2 id="add-title">Add electrical element</h2>
            <label>
              Element type
              <select
                aria-label="Element type"
                value={addKind}
                onChange={(e) => {
                  const kind = e.target.value as Collection;
                  setAddKind(kind);
                  setAddJson(JSON.stringify(emptyTemplates[kind], null, 2));
                }}
              >
                {collections.map((c) => (
                  <option key={c}>{c}</option>
                ))}
              </select>
            </label>
            <p>
              Supply all required equipment values. Null placeholders are not
              defaults.
            </p>
            <textarea
              aria-label="New element JSON"
              value={addJson}
              onChange={(e) => setAddJson(e.target.value)}
              spellCheck={false}
            />
            <div className="modal-actions">
              <button onClick={() => setAddKind(null)}>Cancel</button>
              <button
                className="primary"
                onClick={() => {
                  try {
                    if (
                      network &&
                      edit(addElement(network, addKind, JSON.parse(addJson)))
                    )
                      setAddKind(null);
                  } catch (e) {
                    setIssues(textError(e));
                  }
                }}
              >
                Add to model
              </button>
            </div>
          </section>
        </div>
      ) : null}
    </div>
  );
}
