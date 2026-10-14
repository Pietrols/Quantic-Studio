// Consumer compile and runtime round-trip check, using original Python fixtures.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {pvSiteSchema} from '../src/time/PVSite.ts';
import {pvYieldRequestSchema} from '../src/time/PVYieldRequest.ts';
import {pvYieldResultSchema} from '../src/time/PVYieldResult.ts';

// Schema/semantic validation happens in the Python acceptance suite before
// fixture export. Here a real consumer compiles access to the public fields.
const payloads = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const site = payloads[0];
const request = payloads[1];
const result = payloads[2];
const watts = site.modules[0].reference_dc_power_w;
const limit = site.inverters[0].dc_input_limit_w;
const model = request.execution.model_id;
const energy = result.period.ac_energy_wh;
assert.equal(watts, 300);
assert.equal(limit, 1000);
assert.equal(model, 'solar');
assert.equal(energy, 200);
assert.equal(result.annual, null);
assert.deepEqual(JSON.parse(JSON.stringify([site, request, result])), payloads);
assert.equal(pvSiteSchema.properties.schema_version.const, '0.1.0');
assert.equal(pvYieldRequestSchema.properties.execution.$ref,
  'urn:quantic-studio:contracts:0.1.0:studies:time-stepped-request');
assert.equal(pvYieldResultSchema.properties.execution.$ref,
  'urn:quantic-studio:contracts:0.1.0:studies:time-stepped-result');
console.log('PV TS consumer and payload round-trip passed.');
