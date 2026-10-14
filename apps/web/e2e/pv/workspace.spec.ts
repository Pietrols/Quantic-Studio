import { test, expect } from "@playwright/test";
import {readFileSync} from "node:fs";
import {resolve} from "node:path";
test("pv scaffold runs through the real API and preserves inputs", async ({page}) => {
 const folder=resolve(import.meta.dirname, "../../.e2e-projects/phase2_pv");
 const manifest=JSON.parse(readFileSync(resolve(folder,"manifest.json"),"utf8"));
 const before = manifest.models.map((model: {file: string}) => readFileSync(resolve(folder,model.file)));
 await page.goto("/");
 await page.getByLabel("Project", {exact: true}).selectOption("phase2_pv");
 await expect(page.getByRole("heading",{name: "Solar PV workspace"})).toBeVisible();
 await page.getByRole("button",{name: "Run suite study",exact: true}).click();
 await expect(page.getByText("ENGINE_UNAVAILABLE",{exact: true})).toBeVisible();
 await expect(page.getByLabel("Suite result")).toHaveCount(0);
 manifest.models.forEach((model: {file: string}, i: number) => expect(readFileSync(resolve(folder,model.file))).toEqual(before[i]));
});
