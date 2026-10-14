import type { PlcModel } from "@quantic/contracts";
import type { DiagramNode, DiagramEdge, Port } from "@quantic/canvas";
import type { WorkspaceProps } from "../types";
import { SuitePanel } from "../SuitePanel";
import { SuiteCanvas } from "../SuiteCanvas";
export function plcGraph(model: PlcModel) {
  const ports: Port[] = model.variables.filter(variable => variable.section !== "internal").map(variable => ({
    id: variable.name, kind: variable.type, direction: variable.section === "input" ? "in" : "out",
    side: variable.section === "input" ? "left" : "right"
  }));
  const nodes: DiagramNode[] = [{id: model.controller_id, position: {x: 350, y: 50},
    data: {label: model.controller_id, subtitle: `${model.task.period_ms} ms scan`, ports}}];
  const edges: DiagramEdge[] = [];
  for (const [i, device] of model.devices.entries()) {
    const devicePorts: Port[] = device.io.map(name => {
      const variable = ports.find(port => port.id === name)!;
      return {...variable, direction: variable.direction === "in" ? "out" : "in",
        side: variable.direction === "in" ? "right" : "left"};
    });
    nodes.push({id: device.device_id, position: {x: i % 2 ? 700 : 30, y: 30 + i * 150},
      data: {label: device.label, subtitle: device.device_id, ports: devicePorts}});
    for (const port of devicePorts) edges.push({id: `${device.device_id}:${port.id}`,
      source: port.direction === "out" ? device.device_id : model.controller_id,
      target: port.direction === "out" ? model.controller_id : device.device_id,
      sourceHandle: port.id, targetHandle: port.id});
  }
  return {nodes, edges};
}
export function PLCWorkspace(props: WorkspaceProps) {
  return <SuitePanel context={props} title="PLC process workspace" graph={data => {
    const graph = plcGraph(data as unknown as PlcModel);
    return <SuiteCanvas {...graph} layoutKey={`quantic.plc.layout:${props.projectPath}:${props.model.model_id}`} />;
  }} editor={(data, update) => {
    const model = data as unknown as PlcModel;
    return <label>Structured Text subset
      <textarea aria-label="Structured Text program" value={model.program.body}
        onChange={event => update({...data, program: {...model.program, body: event.target.value}})} />
      <small>quantic-st-0.1 subset. Source text is interpreted only by the future suite handler.</small>
    </label>;
  }} />;
}
