import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("real API model edits, layout and all three studies preserve foreign models", async ({
  page,
}, testInfo) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const control = resolve(
    import.meta.dirname,
    "../.e2e-projects/multi_domain/control.json",
  );
  const foreign = readFileSync(control);
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Authored mixed-domain project" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "motor-feeder power.network" })
    .click();
  await expect(page.getByText("motor_bus", { exact: true })).toBeVisible();
  const node = page
    .locator(".react-flow__node")
    .filter({ hasText: "motor_bus" });
  const box = await node.boundingBox();
  expect(box).toBeTruthy();
  await page.mouse.move(box!.x + box!.width / 2, box!.y + box!.height / 2);
  await page.mouse.down();
  await page.mouse.move(
    box!.x + box!.width / 2 + 55,
    box!.y + box!.height / 2 + 30,
    { steps: 6 },
  );
  await page.mouse.up();
  await expect(page.getByText("Saved model", { exact: true })).toBeVisible();
  await node.click();
  const props = JSON.parse(
    await page.getByLabel("Element properties").inputValue(),
  );
  props.name = "Edited motor bus";
  await page
    .getByLabel("Element properties")
    .fill(JSON.stringify(props, null, 2));
  await page.getByRole("button", { name: "Apply properties" }).click();
  await expect(
    page.getByRole("button", { name: "Run study", exact: true }),
  ).toBeDisabled();
  await page.getByRole("button", { name: "Save model", exact: true }).click();
  await expect(
    page.getByText("Model saved. Other project files preserved."),
  ).toBeVisible();
  await page.getByRole("button", { name: "Run study", exact: true }).click();
  await expect(
    page.getByRole("heading", {
      name: "SUCCESS | Dip limit PASS",
      exact: true,
    }),
  ).toBeVisible();
  await expect(page.getByText("4.853752", { exact: true })).toBeVisible();
  const pending = page.waitForEvent("download");
  await page.getByRole("button", { name: "Download Markdown" }).click();
  const download = await pending;
  const report = testInfo.outputPath("motor-report.md");
  await download.saveAs(report);
  expect(readFileSync(report, "utf8")).toContain("input_hash_sha256");
  await page.getByRole("button", { name: "Fit diagram to view" }).click();
  await page.screenshot({
    path: testInfo.outputPath("power-workspace.png"),
    fullPage: true,
  });
  await page.getByRole("button", { name: "plant power.network" }).click();
  await page.getByLabel("Study", { exact: true }).selectOption("plant-flow");
  await page.getByRole("button", { name: "Run study", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "CONVERGED", exact: true }),
  ).toBeVisible();
  await page.getByLabel("Study", { exact: true }).selectOption("plant-fault");
  await page.getByRole("button", { name: "Run study", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "SUCCESS", exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("columnheader", { name: "Ik'' (kA RMS)" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "control automation.plc" }).click();
  await expect(
    page.getByRole("heading", { name: "Stored model" }),
  ).toBeVisible();
  expect(readFileSync(control).equals(foreign)).toBe(true);
  expect(errors).toEqual([]);
});

test("invalid nameplate/topology is diagnosed before a save", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("button", { name: "motor-feeder power.network" })
    .click();
  await page.getByRole("button", { name: "+ Add element" }).click();
  await page
    .getByLabel("New element JSON")
    .fill(JSON.stringify({ bus_id: "bad", vn_kv: -1, bus_type: "pq" }));
  await page.getByRole("button", { name: "Add to model" }).click();
  await page.getByRole("button", { name: "Cancel", exact: true }).click();
  await expect(page.getByText("SCHEMA_INVALID", { exact: true })).toBeVisible();
  await expect(page.getByText("Saved model", { exact: true })).toBeVisible();
});
