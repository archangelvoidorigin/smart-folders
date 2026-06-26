import type { GraphData, StatsData, Folder } from './types';

const BASE = '/api';

export async function fetchGraph(): Promise<GraphData> {
  const res = await fetch(`${BASE}/graph`);
  return res.json();
}

export async function fetchStats(): Promise<StatsData> {
  const res = await fetch(`${BASE}/stats`);
  return res.json();
}

export async function fetchFolder(path: string): Promise<Folder | null> {
  const res = await fetch(`${BASE}/folders/${path}`);
  if (!res.ok) return null;
  return res.json();
}

export async function fetchFile(path: string, resource: string): Promise<string | null> {
  const res = await fetch(`${BASE}/folders/${path}/${resource}`);
  if (!res.ok) return null;
  return res.text();
}
