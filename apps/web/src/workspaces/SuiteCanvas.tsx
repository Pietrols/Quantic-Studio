import { useState } from "react";
import { applyLayout, positions, type DiagramNode, type DiagramEdge, type Layout } from "@quantic/canvas";
import { GraphCanvas } from "../GraphCanvas";
export function SuiteCanvas({ nodes, edges, layoutKey }: {
  nodes: DiagramNode[]; edges: DiagramEdge[]; layoutKey: string;
}) {
  const [layout, setLayout] = useState<Layout>(() => {
    try { return JSON.parse(localStorage.getItem(layoutKey) ?? "{}"); } catch { return {}; }
  });
  return <GraphCanvas nodes={applyLayout(nodes, layout)} edges={edges}
    onNodes={next => {const value = positions(next); setLayout(value); localStorage.setItem(layoutKey, JSON.stringify(value));}}
    onSelect={() => {}} onConnect={() => {}} valid={() => false} />;
}
