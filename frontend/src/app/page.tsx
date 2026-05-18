'use client';
import { useState } from 'react';
import GraphView from '@/components/GraphView';
import EventFeed from '@/components/EventFeed';
import AttackSimulator from '@/components/AttackSimulator';
import { Shield } from 'lucide-react';

export default function Home() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  return (
    <main className="min-h-screen p-6 max-w-[1600px] mx-auto flex flex-col gap-6">
      <header className="flex items-center gap-3 py-4">
        <Shield className="text-blue-500" size={32} />
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
            Sentinel Swarm
          </h1>
          <p className="text-gray-400 text-sm">AI Immune System Dashboard</p>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        {/* Left Column: Simulator & Events */}
        <div className="flex flex-col gap-6 lg:col-span-1">
          <section className="glass-panel p-5 flex flex-col">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500"></span>
              Attack Simulator
            </h2>
            <AttackSimulator />
          </section>

          <section className="glass-panel p-5 flex-1 flex flex-col overflow-hidden min-h-[400px]">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              Live Event Feed
            </h2>
            <div className="flex-1 overflow-hidden">
              <EventFeed onNewEvent={() => setRefreshTrigger(prev => prev + 1)} />
            </div>
          </section>
        </div>

        {/* Right Column: Threat Graph */}
        <section className="glass-panel p-5 lg:col-span-2 flex flex-col min-h-[600px]">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-purple-500"></span>
            Real-time Threat Graph
          </h2>
          <div className="flex-1 rounded-xl overflow-hidden border border-white/5 bg-black/20">
            <GraphView refreshTrigger={refreshTrigger} />
          </div>
        </section>
      </div>
    </main>
  );
}
