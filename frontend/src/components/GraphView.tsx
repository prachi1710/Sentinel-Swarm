'use client';
import { useCallback, useEffect } from 'react';
import { ReactFlow, MiniMap, Controls, Background, useNodesState, useEdgesState } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

export default function GraphView({ refreshTrigger }: { refreshTrigger: number }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const fetchGraph = useCallback(async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/graph');
      const data = await res.json();
      
      const formattedNodes = data.nodes.map((n: any, i: number) => ({
        id: n.id,
        data: { label: `${n.label}\n(${n.status})` },
        position: { x: 250 + (i * 200), y: 150 + (i % 2 === 0 ? 50 : -50) },
        style: {
          background: n.status === 'compromised' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(34, 197, 94, 0.2)',
          border: `1px solid ${n.status === 'compromised' ? '#ef4444' : '#22c55e'}`,
          color: 'white',
          borderRadius: '8px',
          padding: '10px',
        }
      }));
      
      const formattedEdges = data.edges.map((e: any) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        animated: true,
        style: { stroke: 'rgba(255, 255, 255, 0.5)' }
      }));

      setNodes(formattedNodes);
      setEdges(formattedEdges);
    } catch (err) {
      console.error('Failed to fetch graph', err);
    }
  }, [setNodes, setEdges]);

  useEffect(() => {
    fetchGraph();
  }, [fetchGraph, refreshTrigger]);

  return (
    <div className="w-full h-full min-h-[400px]">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        colorMode="dark"
      >
        <Controls />
        <MiniMap />
        <Background gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}
