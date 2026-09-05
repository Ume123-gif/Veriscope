import React from 'react';
import { Share2, Network, Cpu } from 'lucide-react';

export default function NetworkIntelligence({ communityId, graphScore }) {
  return (
    <div className="bg-radar-900 border border-radar-border rounded-lg p-5 mb-6">
      <div className="flex items-center justify-between pb-4 mb-4 border-b border-radar-800">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono">
            Network Intelligence
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Graph intelligence engine detecting suspicious entity-sharing networks across accounts, devices, cards, and IPs.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left: Community Stats */}
        <div className="space-y-4">
          <div className="bg-radar-950 p-3.5 rounded border border-radar-800">
            <span className="text-[10px] font-mono text-slate-400 uppercase block mb-1">Graph Cluster Identifier</span>
            <div className="flex items-baseline space-x-2">
              <span className="text-xl font-mono font-bold text-cyan-400">
                {communityId !== undefined && communityId !== null ? `COMMUNITY #${communityId}` : 'ISOLATED'}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">
              Deterministic subgraph partition clustered via Louvain modularity algorithm.
            </p>
          </div>

          <div className="bg-radar-950 p-3.5 rounded border border-radar-800">
            <span className="text-[10px] font-mono text-slate-400 uppercase block mb-1">Graph Risk Index</span>
            <div className="flex items-baseline space-x-2">
              <span className="text-xl font-mono font-bold text-slate-200">
                {(graphScore * 10).toFixed(2)}
              </span>
              <span className="text-xs font-mono text-slate-400">Graph Risk Index</span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">
              Composite structural risk derived from community density, connectivity, and cluster characteristics.
            </p>
          </div>
        </div>

        {/* Right: Visual Node Schematic Diagram */}
        <div className="lg:col-span-2 bg-radar-950 border border-radar-800 rounded-lg p-4 flex flex-col justify-between relative overflow-hidden min-h-[190px]">
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b12_1px,transparent_1px),linear-gradient(to_bottom,#1e293b12_1px,transparent_1px)] bg-[size:16px_16px]" />

          <div className="relative z-10 flex items-center justify-between text-xs text-slate-400 border-b border-radar-800 pb-2 font-mono">
            <span>TOPOLOGY PREVIEW</span>
            <span className="text-emerald-400 text-[11px]">CLUSTER RESOLVED</span>
          </div>

          <div className="relative z-10 flex items-center justify-around py-4">
            
            {/* Account Node */}
            <div className="flex flex-col items-center">
              <div className="h-10 w-10 rounded-full bg-cyan-950/80 border border-cyan-500/50 flex items-center justify-center text-cyan-400">
                <Network className="h-5 w-5" />
              </div>
              <span className="text-[10px] font-mono text-slate-300 mt-1.5">Account</span>
              <span className="text-[9px] font-mono text-slate-400">Origin Node</span>
            </div>

            <div className="h-[1px] flex-1 bg-gradient-to-r from-cyan-500/40 via-rose-500/40 to-slate-700 mx-2" />

            {/* Device Node */}
            <div className="flex flex-col items-center">
              <div className="h-10 w-10 rounded-full bg-radar-850 border border-radar-700 flex items-center justify-center text-slate-300">
                <Cpu className="h-5 w-5" />
              </div>
              <span className="text-[10px] font-mono text-slate-300 mt-1.5">Hardware Fingerprint</span>
              <span className="text-[9px] font-mono text-slate-400">Shared Device</span>
            </div>

            <div className="h-[1px] flex-1 bg-gradient-to-r from-slate-700 via-rose-500/40 to-amber-500/40 mx-2" />

            {/* Ring Anchor */}
            <div className="flex flex-col items-center">
              <div className="h-10 w-10 rounded-full bg-rose-950/80 border border-rose-500/50 flex items-center justify-center text-rose-400">
                <Share2 className="h-5 w-5" />
              </div>
              <span className="text-[10px] font-mono text-slate-300 mt-1.5">Shared Subnet</span>
              <span className="text-[9px] font-mono text-rose-400">Collision Flagged</span>
            </div>

          </div>

          <div className="relative z-10 text-[10px] font-mono text-slate-400 border-t border-radar-800 pt-2 flex justify-between">
            <span>Community Structure: RESOLVED</span>
            <span>Cluster Density: High</span>
          </div>
        </div>

      </div>
    </div>
  );
}