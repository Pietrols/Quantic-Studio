import type { PVSite } from "@quantic/contracts";
import type { DiagramNode, DiagramEdge } from "@quantic/canvas";
import type { WorkspaceProps } from "../types";
import { SuitePanel } from "../SuitePanel";
import { SuiteCanvas } from "../SuiteCanvas";
export function pvGraph(site: PVSite) {
  const nodes: DiagramNode[] = site.arrays.map((array, i) => ({
    id: array.array_id, position: {x: 30, y: 30 + i * 150}, data: {
      label: array.array_id, subtitle: `${array.module_count} modules, ${array.tilt_deg} degree tilt`,
      ports: [{id: "dc", kind: "dc_power", direction: "out", side: "right"}]
    }
  }));
  nodes.push(...site.inverters.map((inverter, i): DiagramNode => ({id: inverter.inverter_id,
    position: {x: 350, y: 30 + i * 150}, data: {label: inverter.inverter_id,
      subtitle: `${inverter.ac_rating_w} W AC rating`, ports: [
        {id: "dc", kind: "dc_power", direction: "in", side: "left"},
        {id: "ac", kind: "ac_power", direction: "out", side: "right"}]
    }})));
  const edges: DiagramEdge[] = site.arrays.map(array => ({id: `${array.array_id}-dc`, source: array.array_id,
    target: array.inverter_id, sourceHandle: "dc", targetHandle: "dc"}));
  return {nodes, edges};
}
export function PVWorkspace(props: WorkspaceProps) {
  return <SuitePanel context={props} title="Solar PV workspace" graph={data => {
    const graph = pvGraph(data as unknown as PVSite);
    return <SuiteCanvas {...graph} layoutKey={`quantic.pv.layout:${props.projectPath}:${props.model.model_id}`} />;
  }} />;
}
