import { defineConfig } from "@playwright/test";
import { mkdirSync, cpSync } from "node:fs";
import { resolve } from "node:path";
const repo = resolve(import.meta.dirname, "../..");
const projects = resolve(import.meta.dirname, ".e2e-projects");
mkdirSync(projects, { recursive: true });
for (const name of ["multi_domain", "fourteen_bus"])
  cpSync(resolve(repo, "examples", name), resolve(projects, name), {
    recursive: true,
  });
export default defineConfig({
  testDir: "e2e",
  workers: 1,
  timeout: 60000,
  use: {
    baseURL: "http://127.0.0.1:5173",
    viewport: { width: 1440, height: 1000 },
    trace: "retain-on-failure",
  },
  webServer: [
    {
      command: `uv run qe-api --project-root ${projects}`,
      cwd: repo,
      url: "http://127.0.0.1:8765/health",
      reuseExistingServer: false,
      timeout: 60000,
    },
    {
      command: "pnpm dev",
      cwd: import.meta.dirname,
      url: "http://127.0.0.1:5173",
      reuseExistingServer: false,
      timeout: 60000,
    },
  ],
});
