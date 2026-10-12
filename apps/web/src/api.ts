import type {
  LoadflowResult,
  ShortcircuitResult,
  MotorstartResult,
} from "@quantic/contracts";
import type { Network } from "@quantic/power";
export type Diagnostic = {
  code: string;
  message: string;
  severity?: string;
  element_ref?: {
    element_type: string;
    element_id: string;
    field: string;
  } | null;
};
export type ProjectInfo = {
  name: string;
  models: { model_id: string; model_type: string; file: string }[];
  studies: { study_id: string; study_type: string; model_id: string }[];
  assets: {
    asset_id: string;
    representations: {
      model_id: string;
      element_type: string;
      element_id: string;
    }[];
  }[];
  diagnostics: Diagnostic[];
};
export type ModelInfo = {
  model_id: string;
  model_type: string;
  data: Network;
  etag: string;
  diagnostics: Diagnostic[];
};
export type StudyResponse = {
  study_type: string;
  model_id: string;
  result: LoadflowResult | ShortcircuitResult | MotorstartResult;
  report_markdown: string;
  report_pdf_base64?: string;
  project_diagnostics: Diagnostic[];
};
export class ApiError extends Error {
  constructor(
    public diagnostics: Diagnostic[],
    public status: number,
  ) {
    super(diagnostics.map((d) => `${d.code}: ${d.message}`).join("\n"));
  }
}
async function request<T>(url: string, body?: unknown): Promise<T> {
  const response = await fetch(
    url,
    body === undefined
      ? {}
      : {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        },
  );
  const data = await response
    .json()
    .catch(() => ({
      diagnostics: [{ code: "HTTP_ERROR", message: `HTTP ${response.status}` }],
    }));
  if (!response.ok)
    throw new ApiError(
      data.diagnostics ?? [
        { code: "HTTP_ERROR", message: `HTTP ${response.status}` },
      ],
      response.status,
    );
  return data as T;
}
export const api = {
  projects: () => request<{ projects: string[] }>("/api/projects"),
  health: () => request<{ report_formats: string[] }>("/health"),
  project: (path: string) =>
    request<ProjectInfo>(
      "/api/project?" + new URLSearchParams({ project_path: path }),
    ),
  model: (path: string, id: string) =>
    request<ModelInfo>(
      "/api/model?" + new URLSearchParams({ project_path: path, model_id: id }),
    ),
  save: (path: string, model: ModelInfo, data: Network) =>
    request<{ etag: string }>("/api/model/save", {
      project_path: path,
      model_id: model.model_id,
      etag: model.etag,
      data,
    }),
  run: (path: string, id: string, format = "markdown") =>
    request<StudyResponse>("/api/studies/run", {
      project_path: path,
      study_id: id,
      ...(format === "pdf" ? { report_format: "pdf" } : {}),
    }),
};
