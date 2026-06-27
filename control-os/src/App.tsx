import { useEffect, useState, useCallback, useRef } from 'react';
import cytoscape, { type Core, type EventObject, type NodeSingular, type EdgeSingular } from 'cytoscape';
import { fetchGraph, fetchFolder, fetchStats } from './api';
import type { GraphData, GraphNode, Folder, StatsData } from './types';

const ROLE_COLORS: Record<string, string> = {
  'Knowledge Keeper': '#60A5FA',
  'Creator': '#F87171',
  'Architect': '#FBBF24',
  'Connector': '#C026D3',
  'Chronicler': '#22C55E',
  'Enabler': '#06B6D4',
  'Archive': '#94A3B8',
  'Staging': '#A78BFA',
  'Custom': '#64748B',
};

const EDGE_COLORS: Record<string, string> = {
  'parent': '#A78BFA',
  'child': '#22C55E',
  'feeds_into': '#4ADE80',
  'receives_from': '#60A5FA',
};

function getRoleColor(role: string): string {
  return ROLE_COLORS[role] || ROLE_COLORS['Custom'];
}

function getNodeSize(budget: number): number {
  return Math.max(20, Math.min(60, 20 + budget / 500));
}

export default function App() {
  const [graph, setGraph] = useState<GraphData | null>(null);
  const [stats, setStats] = useState<StatsData | null>(null);
  const [selected, setSelected] = useState<Folder | null>(null);
  const [search, setSearch] = useState('');
  const [layout, setLayout] = useState<'force' | 'tree' | 'concentric'>('force');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);

  useEffect(() => {
    Promise.all([fetchGraph(), fetchStats()])
      .then(([g, s]) => {
        setGraph(g);
        setStats(s);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!graph || !containerRef.current || cyRef.current) return;
    initCy();
    return () => {
      cyRef.current?.destroy();
      cyRef.current = null;
    };
  }, [graph]);

  useEffect(() => {
    if (!cyRef.current || !graph) return;
    const layoutName = layout === 'force' ? 'cose' : layout === 'tree' ? 'breadthfirst' : 'concentric';
    const layoutOpts = {
      name: layoutName,
      animate: true,
      animationDuration: 400,
      fit: true,
      padding: 40,
    } as cytoscape.LayoutOptions;
    cyRef.current.layout(layoutOpts).run();
  }, [layout]);

  useEffect(() => {
    if (!cyRef.current) return;
    cyRef.current.nodes().filter((n) => {
      const label = n.data('label') as string;
      const role = n.data('role') as string;
      const match = !search || label.toLowerCase().includes(search.toLowerCase()) || role.toLowerCase().includes(search.toLowerCase());
      n.style('display', match ? 'element' : 'none');
      return true;
    });
  }, [search]);

  function initCy() {
    if (!containerRef.current || !graph) return;

    const cy = cytoscape({
      container: containerRef.current,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': (ele: NodeSingular) => getRoleColor(ele.data('role')),
            'label': 'data(label)',
            'color': '#F1F5F9',
            'font-size': 11,
            'font-family': 'Inter, sans-serif',
            'text-valign': 'bottom',
            'text-halign': 'center',
            'text-margin-y': 8,
            'width': (ele: NodeSingular) => getNodeSize(ele.data('token_budget')),
            'height': (ele: NodeSingular) => getNodeSize(ele.data('token_budget')),
            'border-width': (ele: NodeSingular) => Math.min(3, ele.data('depth') || 1),
            'border-color': (ele: NodeSingular) => getRoleColor(ele.data('role')),
            'border-opacity': 0.6,
          } as any,
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 3,
            'border-color': '#22C55E',
          } as any,
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': (ele: EdgeSingular) => EDGE_COLORS[ele.data('type')] || '#475569',
            'target-arrow-color': (ele: EdgeSingular) => EDGE_COLORS[ele.data('type')] || '#475569',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'arrow-scale': 1.2,
            'opacity': 0.6,
          },
        },
        {
          selector: 'edge:selected',
          style: {
            'opacity': 1,
            'width': 3,
          },
        },
        {
          selector: 'node.highlighted',
          style: {} as any,
        },
        {
          selector: 'edge.highlighted',
          style: {
            'opacity': 0.9,
            'width': 3,
          },
        },
      ],
      layout: { name: 'cose', fit: true, padding: 40 },
      elements: (() => {
        const nodeIds = new Set(graph.nodes.map((n) => n.id));
        // Cytoscape throws on an edge with a missing endpoint, which would blank
        // the whole graph. Drop any edge that references a non-existent node.
        const validEdges = graph.edges.filter((e) => nodeIds.has(e.source) && nodeIds.has(e.target));
        return [
          ...graph.nodes.map((n) => ({
            data: { id: n.id, label: n.label, role: n.role, depth: n.depth, token_budget: n.token_budget, purpose: n.purpose },
          })),
          ...validEdges.map((e) => ({
            data: { id: e.id, source: e.source, target: e.target, type: e.type, label: e.label },
          })),
        ];
      })(),
      wheelSensitivity: 0.3,
    });

    cy.on('tap', 'node', (evt: EventObject) => {
      const nodeId = evt.target.data('id') as string;
      cy.elements().removeClass('highlighted');
      evt.target.addClass('highlighted');
      evt.target.connectedEdges().addClass('highlighted');
      evt.target.connectedEdges().connectedNodes().addClass('highlighted');

      fetchFolder(nodeId).then((f) => setSelected(f));
    });

    cy.on('tap', (evt: EventObject) => {
      if (evt.target === cy) {
        cy.elements().removeClass('highlighted');
        setSelected(null);
      }
    });

    cyRef.current = cy;
  }

  return (
    <div className="app">
      <div className="topbar">
        <div className="logo">
          <div className="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
            </svg>
          </div>
          <h1>Control OS</h1>
        </div>
        {stats && <span className="badge">{stats.folders} folders</span>}
        <div className="topbar-right">
          <div className="search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              className="search-input"
              placeholder="Filter nodes..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="main">
        <div className="graph-panel">
          {loading && <div className="loading">Loading graph...</div>}
          {error && <div className="error">Error: {error}</div>}
          <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
          {graph && (
            <div className="toggle-layout">
              <button className={layout === 'force' ? 'active' : ''} onClick={() => setLayout('force')}>Force</button>
              <button className={layout === 'tree' ? 'active' : ''} onClick={() => setLayout('tree')}>Tree</button>
              <button className={layout === 'concentric' ? 'active' : ''} onClick={() => setLayout('concentric')}>Circle</button>
            </div>
          )}
        </div>

        <div className="sidebar">
          {selected ? <DetailPanel folder={selected} /> : <EmptyDetail />}
        </div>
      </div>
    </div>
  );
}

function DetailPanel({ folder }: { folder: Folder }) {
  const maxBudget = 50000;
  const bPct = Math.min(100, Math.round(folder.token_budget / maxBudget * 100));
  const fPct = folder.file_limit ? Math.min(100, Math.round(folder.file_count / folder.file_limit * 100)) : 0;

  const c = folder.connections || {};

  return (
    <>
      <div className="detail-header">
        <h2>{folder.name}</h2>
        <span className="role-tag" style={{ background: `${getRoleColor(folder.role)}20`, color: getRoleColor(folder.role) }}>
          {folder.role}
        </span>
      </div>
      <div className="detail-scroll">
        <div className="detail-section">
          <h3>Purpose</h3>
          <p>{folder.purpose || 'Not set'}</p>
        </div>

        <div className="detail-section">
          <h3>Resources</h3>
          <div className="stat-row">
            <span className="label">Token Budget</span>
            <div className="bar-wrap">
              <div className={`bar-fill${bPct > 90 ? ' high' : bPct > 70 ? ' warn' : ''}`} style={{ width: `${bPct}%` }} />
            </div>
            <span className="value">{folder.token_budget.toLocaleString()}</span>
          </div>
          <div className="stat-row">
            <span className="label">Files</span>
            <div className="bar-wrap">
              <div className={`bar-fill${fPct > 90 ? ' high' : fPct > 70 ? ' warn' : ''}`} style={{ width: `${fPct}%` }} />
            </div>
            <span className="value">{folder.file_count}{folder.file_limit ? ` / ${folder.file_limit}` : ''}</span>
          </div>
        </div>

        <div className="detail-section">
          <h3>Details</h3>
          <div className="stat-row"><span className="label">Depth</span><span className="value">{folder.depth}</span></div>
          <div className="stat-row"><span className="label">Path</span><span className="value" style={{ fontSize: 11 }}>{folder.path}</span></div>
          <div className="stat-row"><span className="label">Settings</span><span className="value">{folder.has_settings ? 'Yes' : 'No'}</span></div>
          <div className="stat-row"><span className="label">Ignore Rules</span><span className="value">{folder.has_ignore ? 'Yes' : 'No'}</span></div>
          <div className="stat-row"><span className="label">Laws</span><span className="value">{folder.has_laws ? 'Yes' : 'No'}</span></div>
        </div>

        {c.parent || c.children?.length || c.feeds_into?.length || c.receives_from?.length ? (
          <div className="detail-section">
            <h3>Connections</h3>
            <div className="conn-list">
              {c.parent && (
                <div className="conn-item">
                  <span className="conn-type-badge parent">P</span>
                  {c.parent}
                </div>
              )}
              {c.children?.map((ch, i) => (
                <div className="conn-item" key={i}>
                  <span className="conn-type-badge child">C</span>
                  {ch}
                </div>
              ))}
              {c.feeds_into?.map((fd, i) => (
                <div className="conn-item" key={i}>
                  <span className="conn-type-badge out">→</span>
                  {fd}
                </div>
              ))}
              {c.receives_from?.map((rf, i) => (
                <div className="conn-item" key={i}>
                  <span className="conn-type-badge in">←</span>
                  {rf}
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </>
  );
}

function EmptyDetail() {
  return (
    <div className="empty-detail">
      <div>
        <p style={{ marginBottom: 8, fontWeight: 600, fontSize: 14 }}>Select a Node</p>
        <p>Click any folder node in the graph to see its details, connections, and resource usage.</p>
      </div>
    </div>
  );
}
