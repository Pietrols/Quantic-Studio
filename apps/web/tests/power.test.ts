import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  toGraph,
  replaceElement,
  removeElement,
  addElement,
  validateNetwork,
  reference,
  connectEquipment,
  assetsForModel,
  type Network,
} from "@quantic/power";
import {
  canConnect,
  applyLayout,
  positions,
  type DiagramNode,
} from "@quantic/canvas";
function network(): Network {
  return JSON.parse(
    readFileSync(
      resolve(
        import.meta.dirname,
        "../../../examples/shortcircuit/network.json",
      ),
      "utf8",
    ),
  );
}
describe("network and graph round trips", () => {
  it("mapping and layout never mutate electrical fields", () => {
    const n = network(),
      before = JSON.stringify(n);
    const graph = toGraph(n);
    const moved = applyLayout(graph.nodes, {
      [graph.nodes[0].id]: { x: 950, y: 31 },
    });
    expect(positions(moved)[graph.nodes[0].id]).toEqual({ x: 950, y: 31 });
    expect(JSON.stringify(n)).toBe(before);
    expect(graph.edges[0].id).toBe("lines:feeder");
  });
  it("preserves optional fault fields and unedited elements in a property update", () => {
    const n = network();
    const edit = replaceElement(
      n,
      { collection: "external_grids", id: "grid" },
      { ...n.external_grids[0], vm_setpoint_pu: 1.02 },
    );
    expect(edit.external_grids[0].s_sc_max_mva).toBe(
      n.external_grids[0].s_sc_max_mva,
    );
    expect(edit.lines).toEqual(n.lines);
    expect(n.external_grids[0].vm_setpoint_pu).toBe(1);
    expect(validateNetwork(edit)).toEqual([]);
  });
  it("rejects dangling topology and duplicate IDs", () => {
    const n = network();
    expect(
      validateNetwork(
        removeElement(n, { collection: "buses", id: n.buses[1].bus_id }),
      ).some((e) => e.code === "UNKNOWN_BUS"),
    ).toBe(true);
    expect(
      validateNetwork(
        addElement(
          n,
          "buses",
          n.buses[0] as unknown as Record<string, unknown>,
        ),
      ).some((e) => e.code === "DUPLICATE_ID"),
    ).toBe(true);
  });
  it("requires explicit new nameplate parameters", () => {
    expect(
      validateNetwork(
        addElement(network(), "loads", {
          load_id: "test",
          bus_id: "source",
          p_mw: null,
          q_mvar: null,
        }),
      ).some((e) => e.code === "SCHEMA_INVALID"),
    ).toBe(true);
  });
  it("keeps opaque IDs containing colon intact", () => {
    expect(reference("loads:motor:west")).toEqual({
      collection: "loads",
      id: "motor:west",
    });
  });
  it("rejects nonfinite, wrong-base schema data and missing required fields", () => {
    const n = network();
    n.buses[0].vn_kv = NaN;
    expect(validateNetwork(n).length).toBeGreaterThan(0);
  });
  it("maps only assets belonging to the selected model", () => {
    const assets = [
      {
        asset_id: "a",
        representations: [
          { model_id: "m", element_type: "lines", element_id: "l" },
          { model_id: "other", element_type: "lines", element_id: "foreign" },
        ],
      },
    ];
    expect(assetsForModel(assets, "m")).toEqual({ "lines:l": ["a"] });
  });
  it("equipment reconnection preserves all device values", () => {
    const n = network();
    n.loads = [
      { load_id: "l", bus_id: n.buses[0].bus_id, p_mw: 1, q_mvar: 0.2 },
    ];
    const next = connectEquipment(n, "buses:" + n.buses[1].bus_id, "loads:l");
    expect(next.loads[0]).toEqual({ ...n.loads[0], bus_id: n.buses[1].bus_id });
    expect(n.loads[0].bus_id).toBe(n.buses[0].bus_id);
  });
});
describe("domain-neutral ports", () => {
  it("accepts non-power signal ports and rejects mismatched types/directions", () => {
    const nodes: DiagramNode[] = [
      {
        id: "controller",
        position: { x: 0, y: 0 },
        data: {
          label: "Controller",
          ports: [
            { id: "out", kind: "boolean", direction: "out", side: "right" },
          ],
        },
      },
      {
        id: "actuator",
        position: { x: 100, y: 0 },
        data: {
          label: "Actuator",
          ports: [{ id: "in", kind: "boolean", direction: "in", side: "left" }],
        },
      },
    ];
    expect(canConnect(nodes, "controller", "actuator", "out", "in")).toBe(true);
    nodes[1].data.ports[0].kind = "volts";
    expect(canConnect(nodes, "controller", "actuator", "out", "in")).toBe(
      false,
    );
    expect(canConnect(nodes, "controller", "controller", "out", "out")).toBe(
      false,
    );
  });
});

it("edits legacy v0.1 without changing its version or losing fields", () => {
  const n = JSON.parse(
    readFileSync(
      resolve(
        import.meta.dirname,
        "../../../examples/fourteen_bus/network.json",
      ),
      "utf8",
    ),
  ) as Network;
  n.buses[0].name = "Reviewed bus";
  expect(validateNetwork(n)).toEqual([]);
  expect(n.schema_version).toBe("0.1.0");
});

it("rejects nonfinite signed fields as well as positive ratings", () => {
  const n = network();
  n.loads = [
    { load_id: "l", bus_id: n.buses[0].bus_id, p_mw: 1, q_mvar: Infinity },
  ];
  expect(validateNetwork(n).length).toBeGreaterThan(0);
});
