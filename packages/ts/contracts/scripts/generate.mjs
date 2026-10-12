import { readFile, writeFile, readdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { compile } from "json-schema-to-typescript";
const root = fileURLToPath(new URL("../../../../contracts/", import.meta.url));
const output = fileURLToPath(new URL("../src/generated.ts", import.meta.url));
const schemas = new Map();
async function scan(path) {
  for (const item of await readdir(path, { withFileTypes: true })) {
    const p = path + "/" + item.name;
    if (item.isDirectory()) await scan(p);
    else if (item.name.endsWith(".schema.json")) {
      const schema = JSON.parse(await readFile(p, "utf8"));
      schemas.set(schema.$id, schema);
    }
  }
}
await scan(root);
function inline(value) {
  if (Array.isArray(value)) return value.map(inline);
  if (value && typeof value === "object") {
    if (value.$ref?.startsWith("urn:")) {
      const ref = schemas.get(value.$ref);
      if (!ref) throw new Error("Unknown contract " + value.$ref);
      return inline(ref);
    }
    return Object.fromEntries(
      Object.entries(value).map(([k, v]) => [k, inline(v)]),
    );
  }
  return value;
}
let text =
  "// Generated from repository contracts. Run pnpm generate after a Contract Change.\n";
for (const [name, path] of [
  ["PowerNetwork", "power/network"],
  ["LoadflowResult", "power/loadflow-result"],
  ["ShortcircuitResult", "power/shortcircuit-result"],
  ["MotorstartResult", "power/motorstart-result"],
  ["ProjectManifest", "project/manifest"],
]) {
  const schema = JSON.parse(
    await readFile(root + "/" + path + ".schema.json", "utf8"),
  );
  text += await compile({ ...inline(schema), title: name }, name, {
    bannerComment: "",
    additionalProperties: false,
    declareExternallyReferenced: true,
  });
  if (name === "PowerNetwork")
    text +=
      "\nexport const powerNetworkSchema = " +
      JSON.stringify(schema, null, 2) +
      " as const;\n";
}
const legacy = JSON.parse(
  await readFile(root + "/v0.1/power/network.schema.json", "utf8"),
);
let legacyText = await compile(
  { ...legacy, title: "LegacyPowerNetwork" },
  "LegacyPowerNetwork",
  { bannerComment: "", additionalProperties: false },
);
legacyText +=
  "\nexport const legacyPowerNetworkSchema = " +
  JSON.stringify(legacy, null, 2) +
  " as const;\n";
const outputs = [
  [output, text],
  [output.replace("generated.ts", "legacy.ts"), legacyText],
];
for (const [path, content] of outputs) {
  if (process.argv.includes("--check")) {
    if ((await readFile(path, "utf8")) !== content)
      throw new Error("Generated contract types are stale; run pnpm generate");
  } else await writeFile(path, content);
}
console.log(
  "Generated contract types " +
    (process.argv.includes("--check") ? "match source schemas." : "written."),
);
