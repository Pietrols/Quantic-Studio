import type {PVSite, PVYieldRequest, PVYieldResult} from '../src/index';
// Compile the generated public API as a downstream client without Node types.
export function inspect(site: PVSite, request: PVYieldRequest, result: PVYieldResult) {
  const watts: number = site.modules[0].reference_dc_power_w;
  const inputLimit: number = site.inverters[0].dc_input_limit_w;
  const model: string = request.execution.model_id;
  const energy: number | null = result.period.ac_energy_wh;
  const annual: number | null = result.annual?.ac_energy_wh ?? null;
  return {watts, inputLimit, model, energy, annual};
}
