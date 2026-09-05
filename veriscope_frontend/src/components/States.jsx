import React from 'react';
import { Search, AlertTriangle, Radio } from 'lucide-react';

export function EmptyState() {
  return (
    <div className="border border-dashed border-radar-700/80 bg-radar-900/30 rounded-lg p-12 text-center">
      <div className="mx-auto w-12 h-12 rounded-full bg-radar-850 border border-radar-700 flex items-center justify-center text-slate-400 mb-4">
        <Search className="h-6 w-6" />
      </div>
      <h3 className="text-base font-medium text-slate-200">Investigation Console Idle</h3>
      <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1.5 leading-relaxed">
        Enter a transaction ID to begin risk analysis. The platform queries gradient boost models, behavioral baselines, and syndicated graph clusters.
      </p>
      <div className="mt-5 inline-flex items-center space-x-2 text-[11px] font-mono text-slate-400 bg-radar-850 px-3 py-1.5 rounded border border-radar-800">
        <Radio className="h-3 w-3 text-emerald-400" />
        <span>Ready for query ingestion</span>
      </div>
    </div>
  );
}

export function ErrorState({ error }) {
  return (
    <div className="border border-rose-500/30 bg-rose-950/10 rounded-lg p-6 text-center">
      <div className="mx-auto w-10 h-10 rounded-full bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 mb-3">
        <AlertTriangle className="h-5 w-5" />
      </div>
      <h3 className="text-sm font-semibold text-rose-300 uppercase font-mono">TRANSACTION NOT FOUND </h3>
      <p className="text-xs text-slate-400 max-w-md mx-auto mt-1 leading-relaxed">
        {error}
      </p>
    </div>
  );
}

export function SkeletonLoader() {
  return (
    <div className="animate-pulse space-y-6">
      <div className="h-28 bg-radar-900 border border-radar-800 rounded-lg" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="h-32 bg-radar-900 border border-radar-800 rounded-lg" />
        <div className="h-32 bg-radar-900 border border-radar-800 rounded-lg" />
        <div className="h-32 bg-radar-900 border border-radar-800 rounded-lg" />
      </div>
      <div className="h-48 bg-radar-900 border border-radar-800 rounded-lg" />
      <div className="h-48 bg-radar-900 border border-radar-800 rounded-lg" />
    </div>
  );
}