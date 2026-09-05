import React from 'react';
import { ShieldCheck, Terminal } from 'lucide-react';

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-radar-border bg-radar-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-3">
            <div className="h-8 w-8 rounded bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
              <ShieldCheck className="h-5 w-5 text-cyan-400" />
            </div>

            <div>
              <span className="font-mono text-sm tracking-widest font-bold text-white">
                VERISCOPE
              </span>

              <span className="ml-2 text-xs font-semibold px-2 py-0.5 rounded bg-radar-800 text-slate-400 border border-radar-700">
                Fraud Intelligence
              </span>
            </div>
          </div>

          <div className="hidden md:block">
            <span className="px-3 py-1.5 rounded-md text-xs font-medium font-mono text-white bg-radar-850 border border-radar-700 shadow-sm">
              Investigation
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 bg-radar-900 border border-radar-border rounded-full px-3 py-1">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-[11px] font-mono tracking-tight text-slate-300">
              CORE ENGINE: ACTIVE
            </span>
          </div>

          <div className="h-4 w-[1px] bg-radar-700" />

          <div className="text-xs font-mono text-slate-400 flex items-center gap-1.5">
            <Terminal className="h-3.5 w-3.5 text-slate-500" />
            <span>v2.6.4</span>
          </div>
        </div>

      </div>
    </header>
  );
}