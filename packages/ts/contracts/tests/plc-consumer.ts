import type {PlcModel, PlcScanRequest, PlcScanResult} from '../src/index';
// Compile the generated public API as a downstream client without Node types.
export function inspect(model: PlcModel, request: PlcScanRequest, result: PlcScanResult) {
  const period: number = model.task.period_ms;
  const body: string = model.program.body;
  const coil: string | undefined = model.process?.wiring.coil;
  const binding = request.bindings[0].target;
  const where: string = binding.kind === 'variable' ? binding.variable : binding.port;
  const firstCommit: number | undefined = result.scans[0]?.commit_ms;
  const status: 'complete' | 'partial' | 'failed' = result.execution.status;
  return {period, body, coil, where, firstCommit, status};
}
