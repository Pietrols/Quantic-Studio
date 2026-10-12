import { afterEach, beforeEach, it, expect, vi } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { App } from "../src/App";
const net = JSON.parse(
  readFileSync(
    resolve(import.meta.dirname, "../../../examples/motorstart/network.json"),
    "utf8",
  ),
);
vi.mock("../src/GraphCanvas", () => ({
  GraphCanvas: ({ onSelect }: { onSelect: (id: string) => void }) => (
    <button onClick={() => onSelect("buses:motor_bus")}>
      Select motor bus
    </button>
  ),
}));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string, options?: RequestInit) => {
      if (url === "/health")
        return new Response(JSON.stringify({ report_formats: ["markdown"] }));
      if (url === "/api/projects")
        return new Response(JSON.stringify({ projects: ["demo"] }));
      if (url.startsWith("/api/project?"))
        return new Response(
          JSON.stringify({
            name: "Demo",
            models: [
              {
                model_id: "m",
                model_type: "power.network",
                file: "network.json",
              },
            ],
            studies: [
              { study_id: "start", study_type: "motorstart", model_id: "m" },
            ],
            assets: [],
            diagnostics: [],
          }),
        );
      if (url.startsWith("/api/model?"))
        return new Response(
          JSON.stringify({
            model_id: "m",
            model_type: "power.network",
            data: net,
            etag: "old",
            diagnostics: [],
          }),
        );
      if (url === "/api/model/save")
        return new Response(JSON.stringify({ etag: "new" }));
      if (url === "/api/studies/run")
        return new Response(
          JSON.stringify({
            study_type: "motorstart",
            model_id: "m",
            result: {
              status: "success",
              passes_limit: false,
              dip_limit_percent: 1,
              diagnostics: [],
              bus_results: [
                {
                  bus_id: "motor_bus",
                  prestart_vm_pu: 1,
                  locked_rotor_vm_pu: 0.9,
                  dip_percent: 10,
                  passes_limit: false,
                },
              ],
            },
            project_diagnostics: [],
            report_markdown: "Result report",
          }),
        );
      throw new Error("Unexpected " + url);
    }),
  );
});
it("edits and saves a selected element through API without losing fields", async () => {
  const user = userEvent.setup();
  render(<App />);
  await screen.findByText("Select motor bus");
  await user.click(screen.getByText("Select motor bus"));
  const field = screen.getByLabelText("Element properties");
  await user.clear(field);
  await user.type(
    field,
    JSON.stringify({ ...net.buses[1], name: "Edited bus" }).replaceAll(
      "{",
      "{{",
    ),
  );
  await user.click(screen.getByText("Apply properties"));
  await waitFor(() => expect(screen.getByText("Unsaved changes")).toBeTruthy());
  expect((screen.getByText("Run study") as HTMLButtonElement).disabled).toBe(
    true,
  );
  await user.click(screen.getByText("Save model"));
  await screen.findByText("Model saved. Other project files preserved.");
  const calls = vi.mocked(fetch).mock.calls;
  const save = calls.find((c) => c[0] === "/api/model/save");
  const body = JSON.parse(String(save?.[1]?.body));
  expect(body.data.lines).toEqual(net.lines);
  expect(body.etag).toBe("old");
  expect(body.data.buses[1].name).toBe("Edited bus");
});
it("shows engineering limit failure independently of calculation success", async () => {
  const user = userEvent.setup();
  render(<App />);
  await screen.findByText("Select motor bus");
  await user.click(screen.getByText("Run study"));
  await screen.findByText("SUCCESS | Dip limit FAIL");
  expect(screen.getByText("10.000000")).toBeTruthy();
});
it("displays structured API errors and retains the model after failed run", async () => {
  const base = fetch;
  vi.stubGlobal(
    "fetch",
    vi.fn((url: string, options?: RequestInit) =>
      url === "/api/studies/run"
        ? Promise.resolve(
            new Response(
              JSON.stringify({
                diagnostics: [
                  { code: "STUDY_TIMEOUT", message: "Execution limit" },
                ],
              }),
              { status: 504 },
            ),
          )
        : base(url, options),
    ),
  );
  const user = userEvent.setup();
  render(<App />);
  await screen.findByText("Select motor bus");
  await user.click(screen.getByText("Run study"));
  await screen.findByText("STUDY_TIMEOUT");
  expect(screen.getByText("Select motor bus")).toBeTruthy();
});

it("blocks saved-model execution while property text has not been applied", async () => {
  const user = userEvent.setup();
  render(<App />);
  await screen.findByText("Select motor bus");
  await user.click(screen.getByText("Select motor bus"));
  await user.clear(screen.getByLabelText("Element properties"));
  await screen.findByText("Unapplied properties");
  expect((screen.getByText("Run study") as HTMLButtonElement).disabled).toBe(
    true,
  );
  expect((screen.getByText("Save model") as HTMLButtonElement).disabled).toBe(
    true,
  );
});
