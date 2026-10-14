import { afterEach, it, expect, vi } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { PVWorkspace, pvGraph } from "../../src/workspaces/pv";
import type { WorkspaceProps } from "../../src/workspaces/types";
const fixture = resolve(import.meta.dirname, "../../e2e/pv/fixture");
const manifest = JSON.parse(readFileSync(resolve(fixture, "manifest.json"), "utf8"));
const data = JSON.parse(readFileSync(resolve(fixture, manifest.models[0].file), "utf8"));
vi.mock("../../src/GraphCanvas", () => ({GraphCanvas: ({nodes}: {nodes: {id: string}[]}) =>
  <div>{nodes.map(node => <span key={node.id}>{node.id}</span>)}</div>}));
afterEach(() => {cleanup();vi.unstubAllGlobals();});
function context(): WorkspaceProps {
 return {projectPath: "demo", project: {...manifest, assets: [], diagnostics: []},
  model: {model_id: "solar", model_type: manifest.models[0].model_type, data, etag: "old", diagnostics: []},
  studyId: manifest.studies[0].study_id, reportFormat: "markdown"};
}
it("reports the unavailable engine through the API", async () => {
 vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({diagnostics: [
  {code: "ENGINE_UNAVAILABLE", message: "Suite is not connected"}]}), {status: 422})));
 render(<PVWorkspace {...context()} />);
 await userEvent.click(screen.getByRole("button", {name: "Run suite study"}));
 expect(await screen.findByText("ENGINE_UNAVAILABLE")).toBeTruthy();
 expect(screen.queryByLabelText("Suite result")).toBeNull();
});
it("invalid edits are retained and prevent running", async () => {
 render(<PVWorkspace {...context()} />);
 await userEvent.click(screen.getByText("Model properties JSON"));
 const editor = screen.getByLabelText("Suite model JSON");
 await userEvent.clear(editor); await userEvent.type(editor, "invalid");
 expect((screen.getByRole("button", {name: "Run suite study"}) as HTMLButtonElement).disabled).toBe(true);
 await userEvent.click(screen.getByRole("button", {name: "Save suite model"}));
 expect(await screen.findByText("MODEL_INPUT")).toBeTruthy();
 expect((editor as HTMLTextAreaElement).value).toBe("invalid");
});
it("uses named typed ports in the generic graph", () => {
 const graph = pvGraph(data);
 expect(graph.nodes.length).toBeGreaterThan(1);
 expect(graph.edges.length).toBeGreaterThan(0);
 for (const edge of graph.edges) {
   expect(graph.nodes.find(node => node.id === edge.source)?.data.ports.find(port => port.id === edge.sourceHandle)?.direction).toBe("out");
   expect(graph.nodes.find(node => node.id === edge.target)?.data.ports.find(port => port.id === edge.targetHandle)?.direction).toBe("in");
 }
});
