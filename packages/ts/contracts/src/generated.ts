// Generated from repository contracts. Run pnpm generate after a Contract Change.
export type Identifier = string;

/**
 * Engine-neutral steady-state network model for electrical power studies.
 */
export interface PowerNetwork {
  schema_version: "0.2.0";
  network_id: string;
  base_mva: number;
  /**
   * @minItems 1
   */
  buses: [Bus, ...Bus[]];
  lines: Line[];
  transformers: Transformer[];
  loads: Load[];
  generators: Generator[];
  external_grids: ExternalGrid[];
  shunts: Shunt[];
}
export interface Bus {
  bus_id: Identifier;
  name?: string;
  vn_kv: number;
  bus_type: "slack" | "pv" | "pq";
  vm_pu?: number;
  va_degree?: number;
}
export interface Line {
  line_id: Identifier;
  from_bus: Identifier;
  to_bus: Identifier;
  length_km: number;
  r_ohm_per_km: number;
  x_ohm_per_km: number;
  b_us_per_km?: number;
  max_current_ka?: number;
  end_temperature_celsius?: number;
}
export interface Transformer {
  transformer_id: Identifier;
  hv_bus: Identifier;
  lv_bus: Identifier;
  sn_mva: number;
  vn_hv_kv: number;
  vn_lv_kv: number;
  r_pu: number;
  x_pu: number;
  tap_ratio?: number;
  phase_shift_degree?: number;
  power_station_unit?: boolean;
  oltc?: boolean;
}
export interface Load {
  load_id: Identifier;
  bus_id: Identifier;
  p_mw: number;
  q_mvar: number;
}
export interface Generator {
  generator_id: Identifier;
  bus_id: Identifier;
  p_mw: number;
  vm_setpoint_pu: number;
  p_min_mw?: number;
  p_max_mw?: number;
  q_min_mvar?: number;
  q_max_mvar?: number;
  sn_mva?: number;
  vn_kv?: number;
  xdss_pu?: number;
  rdss_ohm?: number;
  cos_phi?: number;
  voltage_control_range_percent?: number;
  power_station_transformer_id?: string;
}
export interface ExternalGrid {
  external_grid_id: Identifier;
  bus_id: Identifier;
  vm_setpoint_pu: number;
  va_setpoint_degree: number;
  s_sc_max_mva?: number;
  s_sc_min_mva?: number;
  rx_max?: number;
  rx_min?: number;
}
/**
 * Shunt power at the connected bus nominal voltage, positive values denote consumption.
 */
export interface Shunt {
  shunt_id: Identifier;
  bus_id: Identifier;
  p_mw: number;
  q_mvar: number;
}

export const powerNetworkSchema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:quantic-studio:contracts:0.2.0:power:network",
  "title": "Power network",
  "description": "Engine-neutral steady-state network model for electrical power studies.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "network_id",
    "base_mva",
    "buses",
    "lines",
    "transformers",
    "loads",
    "generators",
    "external_grids",
    "shunts"
  ],
  "properties": {
    "schema_version": {
      "const": "0.2.0"
    },
    "network_id": {
      "type": "string",
      "minLength": 1
    },
    "base_mva": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "buses": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/$defs/bus"
      }
    },
    "lines": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/line"
      }
    },
    "transformers": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/transformer"
      }
    },
    "loads": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/load"
      }
    },
    "generators": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/generator"
      }
    },
    "external_grids": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/external_grid"
      }
    },
    "shunts": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/shunt"
      }
    }
  },
  "$defs": {
    "identifier": {
      "type": "string",
      "minLength": 1
    },
    "bus": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "bus_id",
        "vn_kv",
        "bus_type"
      ],
      "properties": {
        "bus_id": {
          "$ref": "#/$defs/identifier"
        },
        "name": {
          "type": "string"
        },
        "vn_kv": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "bus_type": {
          "enum": [
            "slack",
            "pv",
            "pq"
          ]
        },
        "vm_pu": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "va_degree": {
          "type": "number"
        }
      }
    },
    "line": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "line_id",
        "from_bus",
        "to_bus",
        "length_km",
        "r_ohm_per_km",
        "x_ohm_per_km"
      ],
      "properties": {
        "line_id": {
          "$ref": "#/$defs/identifier"
        },
        "from_bus": {
          "$ref": "#/$defs/identifier"
        },
        "to_bus": {
          "$ref": "#/$defs/identifier"
        },
        "length_km": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "r_ohm_per_km": {
          "type": "number",
          "minimum": 0
        },
        "x_ohm_per_km": {
          "type": "number"
        },
        "b_us_per_km": {
          "type": "number",
          "minimum": 0
        },
        "max_current_ka": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "end_temperature_celsius": {
          "type": "number",
          "minimum": 20
        }
      }
    },
    "transformer": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "transformer_id",
        "hv_bus",
        "lv_bus",
        "sn_mva",
        "vn_hv_kv",
        "vn_lv_kv",
        "r_pu",
        "x_pu"
      ],
      "properties": {
        "transformer_id": {
          "$ref": "#/$defs/identifier"
        },
        "hv_bus": {
          "$ref": "#/$defs/identifier"
        },
        "lv_bus": {
          "$ref": "#/$defs/identifier"
        },
        "sn_mva": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "vn_hv_kv": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "vn_lv_kv": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "r_pu": {
          "type": "number",
          "minimum": 0
        },
        "x_pu": {
          "type": "number"
        },
        "tap_ratio": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "phase_shift_degree": {
          "type": "number"
        },
        "power_station_unit": {
          "type": "boolean"
        },
        "oltc": {
          "type": "boolean"
        }
      }
    },
    "load": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "load_id",
        "bus_id",
        "p_mw",
        "q_mvar"
      ],
      "properties": {
        "load_id": {
          "$ref": "#/$defs/identifier"
        },
        "bus_id": {
          "$ref": "#/$defs/identifier"
        },
        "p_mw": {
          "type": "number",
          "minimum": 0
        },
        "q_mvar": {
          "type": "number"
        }
      }
    },
    "generator": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "generator_id",
        "bus_id",
        "p_mw",
        "vm_setpoint_pu"
      ],
      "properties": {
        "generator_id": {
          "$ref": "#/$defs/identifier"
        },
        "bus_id": {
          "$ref": "#/$defs/identifier"
        },
        "p_mw": {
          "type": "number"
        },
        "vm_setpoint_pu": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "p_min_mw": {
          "type": "number"
        },
        "p_max_mw": {
          "type": "number"
        },
        "q_min_mvar": {
          "type": "number"
        },
        "q_max_mvar": {
          "type": "number"
        },
        "sn_mva": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "vn_kv": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "xdss_pu": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "rdss_ohm": {
          "type": "number",
          "minimum": 0
        },
        "cos_phi": {
          "type": "number",
          "exclusiveMinimum": 0,
          "maximum": 1
        },
        "voltage_control_range_percent": {
          "type": "number",
          "minimum": 0
        },
        "power_station_transformer_id": {
          "type": "string",
          "minLength": 1
        }
      }
    },
    "external_grid": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "external_grid_id",
        "bus_id",
        "vm_setpoint_pu",
        "va_setpoint_degree"
      ],
      "properties": {
        "external_grid_id": {
          "$ref": "#/$defs/identifier"
        },
        "bus_id": {
          "$ref": "#/$defs/identifier"
        },
        "vm_setpoint_pu": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "va_setpoint_degree": {
          "type": "number"
        },
        "s_sc_max_mva": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "s_sc_min_mva": {
          "type": "number",
          "exclusiveMinimum": 0
        },
        "rx_max": {
          "type": "number",
          "minimum": 0
        },
        "rx_min": {
          "type": "number",
          "minimum": 0
        }
      }
    },
    "shunt": {
      "type": "object",
      "description": "Shunt power at the connected bus nominal voltage, positive values denote consumption.",
      "additionalProperties": false,
      "required": [
        "shunt_id",
        "bus_id",
        "p_mw",
        "q_mvar"
      ],
      "properties": {
        "shunt_id": {
          "$ref": "#/$defs/identifier"
        },
        "bus_id": {
          "$ref": "#/$defs/identifier"
        },
        "p_mw": {
          "type": "number"
        },
        "q_mvar": {
          "type": "number"
        }
      }
    }
  }
} as const;
/**
 * Per-bus and per-branch outputs plus convergence, diagnostics, and provenance.
 */
export interface LoadflowResult {
  schema_version: string;
  result_id: string;
  network_id: string;
  bus_results: BusResult[];
  branch_results: BranchResult[];
  convergence: Convergence;
  diagnostics: Diagnostic[];
  provenance: Provenance;
}
export interface BusResult {
  bus_id: string;
  vm_pu: number;
  va_degree: number;
}
export interface BranchResult {
  branch_id: string;
  branch_type: "line" | "transformer";
  p_from_mw: number;
  q_from_mvar: number;
  p_to_mw: number;
  q_to_mvar: number;
  p_loss_mw: number;
  q_loss_mvar: number;
  loading_pct: number | null;
}
export interface Convergence {
  converged: boolean;
  iterations: number;
  largest_mismatch_mva: number;
}
/**
 * A machine-readable explanation of a validation or study condition.
 */
export interface Diagnostic {
  code: string;
  severity: "info" | "warning" | "error";
  message: string;
  element_ref: null | {
    element_type: string;
    element_id: string;
    field?: string;
  };
}
/**
 * Origin and reproducibility metadata for a solver result.
 */
export interface Provenance {
  solver_name: string;
  solver_version: string;
  input_hash_sha256: string;
  timestamp: string;
}
export type ShortcircuitResult = {
  [k: string]: unknown;
} & {
  schema_version: "0.3.0";
  result_id: string;
  network_id: string;
  fault_type: "3ph";
  fault_duration_s: number;
  frequency_hz: 50 | 60;
  lv_tolerance_percent: 6 | 10;
  status: "success" | "partial" | "failed";
  /**
   * @minItems 1
   * @maxItems 2
   */
  case_results:
    | [
        {
          [k: string]: unknown;
        } & {
          [k: string]: unknown;
        } & {
          [k: string]: unknown;
        }
      ]
    | [
        {
          [k: string]: unknown;
        } & {
          [k: string]: unknown;
        } & {
          [k: string]: unknown;
        },
        {
          [k: string]: unknown;
        } & {
          [k: string]: unknown;
        } & {
          [k: string]: unknown;
        }
      ];
  /**
   * @minItems 1
   */
  assumptions: [string, ...string[]];
  diagnostics: Diagnostic[];
  provenance: Provenance;
};

/**
 * A machine-readable explanation of a validation or study condition.
 */
export interface Diagnostic {
  code: string;
  severity: "info" | "warning" | "error";
  message: string;
  element_ref: null | {
    element_type: string;
    element_id: string;
    field?: string;
  };
}
/**
 * Origin and reproducibility metadata for a solver result.
 */
export interface Provenance {
  solver_name: string;
  solver_version: string;
  input_hash_sha256: string;
  timestamp: string;
}
export interface MotorstartResult {
  schema_version: "0.4.0";
  result_id: string;
  network_id: string;
  motor: {
    motor_id: string;
    bus_id: string;
    shaft_rated_kw: number;
    efficiency: number;
    rated_power_factor: number;
    rated_voltage_kv: number;
    locked_rotor_current_ratio: number;
    locked_rotor_power_factor: number;
  };
  dip_limit_percent: number;
  dip_definition: "100*(prestart_vm_pu-locked_rotor_vm_pu)/prestart_vm_pu";
  status: "success" | "failed";
  passes_limit: boolean | null;
  /**
   * @minItems 1
   */
  bus_results: [
    {
      bus_id: string;
      prestart_vm_pu: number | null;
      locked_rotor_vm_pu: number | null;
      dip_percent: number | null;
      passes_limit: boolean | null;
    },
    ...{
      bus_id: string;
      prestart_vm_pu: number | null;
      locked_rotor_vm_pu: number | null;
      dip_percent: number | null;
      passes_limit: boolean | null;
    }[]
  ];
  /**
   * @minItems 1
   */
  assumptions: [string, ...string[]];
  diagnostics: Diagnostic[];
  provenance: Provenance;
  motor_trace?: {
    bus_kv: number;
    rated_current_ka: number;
    locked_rotor_current_ka: number;
    z_lr_ohm: number;
    r_lr_ohm: number;
    shunt_p_mw: number;
    locked_rotor_angle_deg: number;
    x_lr_ohm: number;
    shunt_q_mvar: number;
  } | null;
}
/**
 * A machine-readable explanation of a validation or study condition.
 */
export interface Diagnostic {
  code: string;
  severity: "info" | "warning" | "error";
  message: string;
  element_ref: null | {
    element_type: string;
    element_id: string;
    field?: string;
  };
}
/**
 * Origin and reproducibility metadata for a solver result.
 */
export interface Provenance {
  solver_name: string;
  solver_version: string;
  input_hash_sha256: string;
  timestamp: string;
}
export interface ProjectManifest {
  schema_version: "1.0.0";
  name: string;
  /**
   * @minItems 1
   */
  models: [
    {
      model_id: string;
      model_type: string;
      file: string;
    },
    ...{
      model_id: string;
      model_type: string;
      file: string;
    }[]
  ];
  studies: {
    study_id: string;
    study_type: string;
    model_id: string;
    request_file: string;
  }[];
  asset_registry: UrnQuanticStudioContracts100ProjectAssetRegistry;
}
export interface UrnQuanticStudioContracts100ProjectAssetRegistry {
  schema_version: "1.0.0";
  assets: {
    asset_id: string;
    name?: string;
    /**
     * @minItems 1
     */
    representations: [
      {
        model_id: string;
        element_type: string;
        element_id: string;
      },
      ...{
        model_id: string;
        element_type: string;
        element_id: string;
      }[]
    ];
  }[];
}
