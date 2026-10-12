import { useMemo, useEffect, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  Position,
  type NodeProps,
  type Connection,
  type NodeChange,
  applyNodeChanges,
} from "@xyflow/react";
import type { DiagramNode, DiagramEdge } from "@quantic/canvas";
import "@xyflow/react/dist/style.css";
function CanvasNode({ data, selected }: NodeProps<DiagramNode>) {
  return (
    <div className={"diagram-node" + (selected ? " selected" : "")}>
      <div className="node-symbol">
        {data.glyph ?? <span className="generic-symbol" />}
      </div>
      <strong>{data.label}</strong>
      <small>{data.subtitle}</small>
      {data.assetIds?.length ? (
        <span className="asset-tag">Asset: {data.assetIds.join(", ")}</span>
      ) : null}
      {data.ports.map((p) => (
        <Handle
          key={p.id}
          id={p.id}
          type={p.direction === "in" ? "target" : "source"}
          position={
            {
              left: Position.Left,
              right: Position.Right,
              top: Position.Top,
              bottom: Position.Bottom,
            }[p.side]
          }
          aria-label={`${data.label} ${p.id} ${p.kind} port`}
        />
      ))}
    </div>
  );
}
const nodeTypes = { diagram: CanvasNode };
export function GraphCanvas({
  nodes,
  edges,
  onNodes,
  onSelect,
  onConnect,
  valid,
}: {
  nodes: DiagramNode[];
  edges: DiagramEdge[];
  onNodes: (nodes: DiagramNode[]) => void;
  onSelect: (id: string) => void;
  onConnect: (connection: Connection) => void;
  valid: (connection: Connection) => boolean;
}) {
  const typed = useMemo(
    () => nodes.map((n) => ({ ...n, type: "diagram" })),
    [nodes],
  );
  const [visible, setVisible] = useState<DiagramNode[]>(typed);
  useEffect(
    () =>
      setVisible((previous) =>
        typed.map((node) => {
          const old = previous.find((n) => n.id === node.id);
          return { ...node, measured: old?.measured, selected: old?.selected };
        }),
      ),
    [typed],
  );
  return (
    <ReactFlow
      nodes={visible}
      edges={edges}
      nodeTypes={nodeTypes}
      onNodesChange={(changes: NodeChange<DiagramNode>[]) => {
        const next = applyNodeChanges(changes, visible);
        setVisible(next);
        if (changes.some((c) => c.type === "position")) onNodes(next);
      }}
      onNodeClick={(_, node) => onSelect(node.id)}
      onEdgeClick={(_, edge) =>
        onSelect(edge.id.startsWith("connection:") ? edge.target : edge.id)
      }
      onConnect={onConnect}
      isValidConnection={(c) => valid(c as Connection)}
      nodesFocusable
      edgesFocusable
      deleteKeyCode={null}
      fitView
      minZoom={0.2}
      maxZoom={2.5}
      ariaLabelConfig={{ "controls.fitView.ariaLabel": "Fit diagram to view" }}
    >
      <Background gap={24} color="#d7e0e8" />
      <Controls />
    </ReactFlow>
  );
}
