import type { ReactNode } from "react";
import type { Edge, Node } from "@xyflow/react";
export type Port = {
  id: string;
  kind: string;
  direction: "in" | "out";
  side: "left" | "right" | "top" | "bottom";
};
export type CanvasData = Record<string, unknown> & {
  label: string;
  subtitle?: string;
  ports: Port[];
  glyph?: ReactNode;
  assetIds?: string[];
};
export type DiagramNode = Node<CanvasData>;
export type DiagramEdge = Edge;
export type Layout = Record<string, { x: number; y: number }>;
export function canConnect(
  nodes: DiagramNode[],
  source: string,
  target: string,
  sourcePort: string,
  targetPort: string,
): boolean {
  if (source === target) return false;
  const out = nodes
    .find((n) => n.id === source)
    ?.data.ports.find((p) => p.id === sourcePort);
  const input = nodes
    .find((n) => n.id === target)
    ?.data.ports.find((p) => p.id === targetPort);
  return (
    !!out &&
    !!input &&
    out.direction === "out" &&
    input.direction === "in" &&
    out.kind === input.kind
  );
}
export function positions(nodes: DiagramNode[]): Layout {
  return Object.fromEntries(nodes.map((n) => [n.id, n.position]));
}
export function applyLayout(
  nodes: DiagramNode[],
  layout: Layout,
): DiagramNode[] {
  return nodes.map((n) => {
    const p = layout[n.id];
    return p && Number.isFinite(p.x) && Number.isFinite(p.y)
      ? { ...n, position: p }
      : n;
  });
}
