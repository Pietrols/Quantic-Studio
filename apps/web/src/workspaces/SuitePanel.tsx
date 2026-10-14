import { useState, type ReactNode } from "react";
import { api, ApiError, type Diagnostic, type StudyResponse } from "../api";
import type { WorkspaceProps } from "./types";
export type ModelData = Record<string, unknown>;
export function SuitePanel({ context, title, graph, editor }: {
  context: WorkspaceProps; title: string;
  graph: (data: ModelData) => ReactNode;
  editor?: (data: ModelData, update: (data: ModelData) => void) => ReactNode;
}) {
  const [data, setData] = useState<ModelData>(context.model.data as unknown as ModelData);
  const [text, setText] = useState(JSON.stringify(data, null, 2));
  const [etag, setEtag] = useState(context.model.etag);
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);
  const [issues, setIssues] = useState<Diagnostic[]>([]);
  const [result, setResult] = useState<StudyResponse>();
  const update = (value: ModelData) => {
    setData(value); setText(JSON.stringify(value, null, 2)); setDirty(true); setResult(undefined);
  };
  const fail = (error: unknown) => setIssues(error instanceof ApiError ? error.diagnostics :
    [{ code: "MODEL_INPUT", message: String(error), severity: "error" }]);
  async function save() {
    setBusy(true); setIssues([]);
    try {
      const value: unknown = JSON.parse(text);
      if (!value || typeof value !== "object" || Array.isArray(value)) throw Error("Model must be an object");
      const saved = await api.save(context.projectPath, { ...context.model, etag }, value as ModelData);
      setEtag(saved.etag); setData(value as ModelData); setDirty(false);
    } catch (error) { fail(error); } finally { setBusy(false); }
  }
  async function run() {
    setBusy(true); setIssues([]); setResult(undefined);
    try { setResult(await api.run(context.projectPath, context.studyId, context.reportFormat)); }
    catch (error) { fail(error); } finally { setBusy(false); }
  }
  function download(name: string, content: string) {
    const url = URL.createObjectURL(new Blob([content], {type: "text/plain"}));
    const link = document.createElement("a"); link.href = url; link.download = name; link.click(); URL.revokeObjectURL(url);
  }
  return <section className="suite-workspace" aria-label={title}>
    <h2>{title}</h2>
    <p>Local studies only. No live equipment or online data access.</p>
    <div className="suite-graph">{graph(data)}</div>
    {editor?.(data, update)}
    <details><summary>Model properties JSON</summary>
      <textarea aria-label="Suite model JSON" value={text} disabled={busy}
        onChange={event => {setText(event.target.value); setDirty(true); setResult(undefined);}} />
    </details>
    <div className="suite-actions">
      <button onClick={save} disabled={!dirty || busy}>Save suite model</button>
      <button onClick={run} disabled={dirty || busy || !context.studyId}>Run suite study</button>
      <span role="status">{dirty ? "Unsaved model changes" : "Saved suite model"}</span>
    </div>
    <ul aria-label="Suite diagnostics">{issues.map((issue, i) => <li key={i}>
      <strong>{issue.code}</strong>: {issue.message}
    </li>)}</ul>
    {result && <section aria-label="Suite result">
      <pre>{JSON.stringify(result.result, null, 2)}</pre>
      <button onClick={() => download(`${context.studyId}-report.md`, result.report_markdown)}>Download suite Markdown</button>
      <button onClick={() => download(`${context.studyId}-results.json`, JSON.stringify(result.result, null, 2))}>Download suite results</button>
      <pre>{result.report_markdown}</pre>
    </section>}
  </section>;
}
