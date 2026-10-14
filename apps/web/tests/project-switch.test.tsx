import { afterEach, beforeEach, it, expect, vi } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { App } from "../src/App";

// WP-1.16: switching project must never request the previous project's model.
const net = JSON.parse(
  readFileSync(
    resolve(import.meta.dirname, "../../../examples/motorstart/network.json"),
    "utf8",
  ),
);
const projects: Record<string, string> = { alpha: "model-a", beta: "model-b" };
vi.mock("../src/GraphCanvas", () => ({ GraphCanvas: () => <div>canvas</div> }));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string) => {
      const query = new URLSearchParams(url.split("?")[1] ?? "");
      if (url === "/health")
        return new Response(JSON.stringify({ report_formats: ["markdown"] }));
      if (url === "/api/projects")
        return new Response(
          JSON.stringify({ projects: Object.keys(projects) }),
        );
      if (url.startsWith("/api/project?")) {
        const id = projects[query.get("project_path") ?? ""];
        return new Response(
          JSON.stringify({
            name: query.get("project_path"),
            models: [
              {
                model_id: id,
                model_type: "power.network",
                file: "network.json",
              },
            ],
            studies: [],
            assets: [],
            diagnostics: [],
          }),
        );
      }
      if (url.startsWith("/api/model?")) {
        const wanted = projects[query.get("project_path") ?? ""];
        if (query.get("model_id") !== wanted)
          return new Response(
            JSON.stringify({
              diagnostics: [{ code: "NOT_FOUND", message: "No model" }],
            }),
            { status: 404 },
          );
        return new Response(
          JSON.stringify({
            model_id: wanted,
            model_type: "power.network",
            data: net,
            etag: "e",
            diagnostics: [],
          }),
        );
      }
      throw new Error("Unexpected " + url);
    }),
  );
});
it("does not request a model from the wrong project after switching", async () => {
  const user = userEvent.setup();
  render(<App />);
  const picker = (await screen.findByLabelText("Project", {
    exact: true,
  })) as HTMLSelectElement;
  await user.selectOptions(picker, "alpha");
  await screen.findByText("model-a", { selector: "strong" });
  await user.selectOptions(picker, "beta");
  await screen.findByText("model-b", { selector: "strong" });
  await waitFor(() => {
    const calls = vi
      .mocked(fetch)
      .mock.calls.map((c) => String(c[0]))
      .filter((u) => u.startsWith("/api/model?"));
    expect(calls).toContain("/api/model?project_path=beta&model_id=model-b");
    for (const call of calls) {
      const q = new URLSearchParams(call.split("?")[1]);
      expect(q.get("model_id")).toBe(projects[q.get("project_path") ?? ""]);
    }
  });
});
