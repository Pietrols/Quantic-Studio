import Ajv2020 from "ajv/dist/2020.js";
import {
  powerNetworkSchema,
  legacyPowerNetworkSchema,
  type PowerNetwork,
  type LegacyPowerNetwork,
} from "@quantic/contracts";
import {
  type DiagramNode,
  type DiagramEdge,
  type Layout,
  applyLayout,
  canConnect,
} from "@quantic/canvas";
export type Network = PowerNetwork | LegacyPowerNetwork;
export const collections = [
  "buses",
  "lines",
  "transformers",
  "loads",
  "generators",
  "external_grids",
  "shunts",
] as const;
export type Collection = (typeof collections)[number];
export type Ref = { collection: Collection; id: string };
export type Issue = {
  code: string;
  message: string;
  element_ref?: { element_type: string; element_id: string; field: string };
};
const keys: Record<Collection, string> = {
  buses: "bus_id",
  lines: "line_id",
  transformers: "transformer_id",
  loads: "load_id",
  generators: "generator_id",
  external_grids: "external_grid_id",
  shunts: "shunt_id",
};
const ajv = new Ajv2020({
  allErrors: true,
  strict: false,
  strictNumbers: true,
});
const latestValidator = ajv.compile(powerNetworkSchema);
const legacyValidator = ajv.compile(legacyPowerNetworkSchema);
export function validateNetwork(data: unknown): Issue[] {
  const version = (data as { schema_version?: string } | null)?.schema_version;
  const validator = version === "0.1.0" ? legacyValidator : latestValidator;
  if (!validator(data))
    return (validator.errors ?? []).map((e) => ({
      code: "SCHEMA_INVALID",
      message: `${e.instancePath || "/"} ${e.message}`,
    }));
  const net = data as Network,
    issues: Issue[] = [];
  const buses = new Set(net.buses.map((b) => b.bus_id));
  for (const collection of collections) {
    const seen = new Set<string>();
    for (const element of net[collection] as unknown as Record<
      string,
      unknown
    >[]) {
      const id = String(element[keys[collection]]);
      if (seen.has(id))
        issues.push({
          code: "DUPLICATE_ID",
          message: `${collection}: ${id} must be unique`,
        });
      seen.add(id);
      for (const field of [
        "bus_id",
        "from_bus",
        "to_bus",
        "hv_bus",
        "lv_bus",
      ]) {
        if (
          collection !== "buses" &&
          field in element &&
          !buses.has(String(element[field]))
        )
          issues.push({
            code: "UNKNOWN_BUS",
            message: `${collection}:${id}.${field} names a missing bus`,
            element_ref: { element_type: collection, element_id: id, field },
          });
      }
    }
  }
  return issues;
}
export function graphId(ref: Ref) {
  return ref.collection + ":" + ref.id;
}
export function reference(id: string): Ref {
  const split = id.indexOf(":");
  return {
    collection: id.slice(0, split) as Collection,
    id: id.slice(split + 1),
  };
}
export function element(
  network: Network,
  ref: Ref,
): Record<string, unknown> | undefined {
  return (network[ref.collection] as unknown as Record<string, unknown>[]).find(
    (e) => e[keys[ref.collection]] === ref.id,
  );
}
export function replaceElement(
  network: Network,
  ref: Ref,
  value: Record<string, unknown>,
): Network {
  const next = structuredClone(network);
  (next[ref.collection] as unknown as Record<string, unknown>[]) = (
    next[ref.collection] as unknown as Record<string, unknown>[]
  ).map((e) =>
    e[keys[ref.collection]] === ref.id ? structuredClone(value) : e,
  );
  return next;
}
export function removeElement(network: Network, ref: Ref): Network {
  const next = structuredClone(network);
  (next[ref.collection] as unknown as Record<string, unknown>[]) = (
    next[ref.collection] as unknown as Record<string, unknown>[]
  ).filter((e) => e[keys[ref.collection]] !== ref.id);
  return next;
}
export function addElement(
  network: Network,
  collection: Collection,
  value: Record<string, unknown>,
): Network {
  const next = structuredClone(network);
  (next[collection] as unknown as Record<string, unknown>[]).push(
    structuredClone(value),
  );
  return next;
}
export function toGraph(
  network: Network,
  layout: Layout = {},
  assets: Record<string, string[]> = {},
): { nodes: DiagramNode[]; edges: DiagramEdge[] } {
  const nodes: DiagramNode[] = network.buses.map((b, i) => ({
    id: graphId({ collection: "buses", id: b.bus_id }),
    position: { x: 100 + (i % 4) * 240, y: 70 + Math.floor(i / 4) * 230 },
    data: {
      label: b.name || b.bus_id,
      subtitle: `${b.vn_kv} kV | ${b.bus_type.toUpperCase()}`,
      ports: [
        { id: "out", kind: "ac", direction: "out", side: "right" },
        { id: "in", kind: "ac", direction: "in", side: "left" },
      ],
      assetIds: assets["buses:" + b.bus_id] ?? [],
    },
  }));
  const edges: DiagramEdge[] = [];
  for (const collection of ["lines", "transformers"] as Collection[]) {
    for (const item of network[collection] as unknown as Record<
      string,
      unknown
    >[]) {
      const id = String(item[keys[collection]]),
        from = String(item.from_bus ?? item.hv_bus),
        to = String(item.to_bus ?? item.lv_bus);
      edges.push({
        id: graphId({ collection, id }),
        source: "buses:" + from,
        target: "buses:" + to,
        sourceHandle: "out",
        targetHandle: "in",
        label: collection === "lines" ? id : `Transformer ${id}`,
        type: "smoothstep",
        style: {
          stroke: collection === "lines" ? "#66829b" : "#aa7c3e",
          strokeWidth: 2,
        },
      });
    }
  }
  for (const collection of [
    "loads",
    "generators",
    "external_grids",
    "shunts",
  ] as Collection[]) {
    for (const [i, item] of (
      network[collection] as unknown as Record<string, unknown>[]
    ).entries()) {
      const id = String(item[keys[collection]]),
        bus = String(item.bus_id),
        anchor = nodes.find((n) => n.id === "buses:" + bus)?.position ?? {
          x: 100,
          y: 100,
        };
      const nodeId = graphId({ collection, id });
      nodes.push({
        id: nodeId,
        position: {
          x: anchor.x + 80 + (i % 2) * 150,
          y: anchor.y + 100 + (i % 3) * 55,
        },
        data: {
          label: String(item.name ?? id),
          subtitle: collection.replaceAll("_", " "),
          ports: [{ id: "in", kind: "ac", direction: "in", side: "top" }],
          assetIds: assets[nodeId] ?? [],
        },
      });
      edges.push({
        id: "connection:" + nodeId,
        source: "buses:" + bus,
        target: nodeId,
        sourceHandle: "out",
        targetHandle: "in",
        type: "smoothstep",
        style: { stroke: "#7c98b2" },
      });
    }
  }
  return { nodes: applyLayout(nodes, layout), edges };
}
export function connectEquipment(
  network: Network,
  source: string,
  target: string,
): Network {
  const from = reference(source),
    to = reference(target);
  if (
    from.collection !== "buses" ||
    ["buses", "lines", "transformers"].includes(to.collection)
  )
    throw new Error(
      "Connect a bus to equipment, or create a branch between buses.",
    );
  const data = element(network, to);
  if (!data) throw new Error("Equipment no longer exists");
  return replaceElement(network, to, { ...data, bus_id: from.id });
}
export function validConnection(
  network: Network,
  nodes: DiagramNode[],
  source: string,
  target: string,
  sourcePort: string,
  targetPort: string,
) {
  return (
    canConnect(nodes, source, target, sourcePort, targetPort) &&
    reference(source).collection === "buses" &&
    !["lines", "transformers"].includes(reference(target).collection)
  );
}
export function assetsForModel(
  assets: {
    asset_id: string;
    representations: {
      model_id: string;
      element_type: string;
      element_id: string;
    }[];
  }[],
  modelId: string,
) {
  const result: Record<string, string[]> = {};
  for (const asset of assets)
    for (const ref of asset.representations)
      if (ref.model_id === modelId)
        (result[ref.element_type + ":" + ref.element_id] ??= []).push(
          asset.asset_id,
        );
  return result;
}
