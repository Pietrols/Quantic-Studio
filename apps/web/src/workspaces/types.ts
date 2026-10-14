import type { ModelInfo, ProjectInfo } from "../api";
export type WorkspaceProps = {
  projectPath: string;
  project: ProjectInfo;
  model: ModelInfo;
  studyId: string;
  reportFormat: string;
};
