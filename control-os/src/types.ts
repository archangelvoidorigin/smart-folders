export interface Folder {
  path: string;
  name: string;
  role: string;
  purpose: string;
  depth: string;
  token_budget: number;
  file_limit: number;
  file_count: number;
  connections: Connections | null;
  has_smart: boolean;
  has_settings: boolean;
  has_ignore: boolean;
  has_laws: boolean;
}

export interface Connections {
  parent?: string;
  children?: string[];
  feeds_into?: string[];
  receives_from?: string[];
}

export interface GraphNode {
  id: string;
  label: string;
  role: string;
  depth: number;
  token_budget: number;
  file_count: number;
  has_settings: boolean;
  has_smartignore: boolean;
  has_laws: boolean;
  purpose: string;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface StatsData {
  folders: number;
  total_budget: number;
  avg_budget: number;
  avg_files: number;
  roles: Record<string, number>;
  has_settings: number;
  has_ignore: number;
  has_laws: number;
}
