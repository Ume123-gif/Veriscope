import React from 'react';
import { getDecisionTheme, getRiskTheme } from '../utils/formatters';
import { ShieldCheck, ShieldAlert, AlertCircle, Ban } from 'lucide-react';

const DECISION_ICONS = {
  ALLOW: ShieldCheck,
  REVIEW: AlertCircle,
  HOLD: ShieldAlert,
  BLOCK: Ban
};

export default function DecisionBanner({ data }) {
  const { decision, risk_level, risk_score, risk_score_percent, transaction_id, account_id, predicted_class } = data;
  const dTheme = getDecisionTheme(decision);
  const rTheme = getRiskTheme(risk_level);
  const Icon = DECISION_ICONS[decision?.toUpperCase()] || AlertCircle;

  return (
    <div className={`border rounded-lg p-5 mb-6 ${dTheme.bg} ${dTheme.border} relative overflow-hidden`}>
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        
        {/* Left: Decision Tag */}
        <div className="flex items-center space-x-4">
          <div className={`p-3 rounded-lg border bg-radar-950/80 ${dTheme.border}`}>
            <Icon className={`h-8 w-8 ${dTheme.text}`} />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <span className="text-xs font-mono tracking-wider uppercase text-slate-400 font-semibold">Engine Verdict</span>
              <span className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold tracking-wide border ${rTheme.border} ${rTheme.badge}`}>
                {risk_level} RISK
              </span>
            </div>
            <h2 className={`text-3xl font-mono font-black tracking-tight ${dTheme.text}`}>
              {decision}
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">{dTheme.sub}</p>
          </div>
        </div>

        {/* Center: Metadata Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 border-t lg:border-t-0 lg:border-l border-radar-700/60 pt-4 lg:pt-0 lg:pl-6 text-xs">
          <div>
            <span className="block text-slate-500 font-mono text-[10px] uppercase">Transaction ID</span>
            <span className="font-mono text-slate-200 select-all font-medium truncate block max-w-[140px]">{transaction_id}</span>
          </div>
          <div>
            <span className="block text-slate-500 font-mono text-[10px] uppercase">Account ID</span>
            <span className="font-mono text-slate-200 select-all font-medium truncate block max-w-[140px]">{account_id}</span>
          </div>
          <div>
            <span className="block text-slate-500 font-mono text-[10px] uppercase">Classification</span>
            <span className="font-mono text-cyan-400 font-medium uppercase">{predicted_class || 'Standard'}</span>
          </div>
        </div>

        {/* Right: Risk Gauge Meter */}
        <div className="w-full lg:w-auto flex flex-row lg:flex-col items-center justify-between lg:items-end border-t lg:border-t-0 border-radar-700/60 pt-3 lg:pt-0">
          <span className="text-[10px] font-mono text-slate-500 uppercase">Composite Risk Score</span>
          <div className="flex items-baseline space-x-1">
            <span className="text-3xl font-mono font-black text-slate-100">
              {risk_score_percent !== undefined ? risk_score_percent.toFixed(1) : (risk_score * 100).toFixed(1)}
            </span>
            <span className="text-xs font-mono text-slate-500">/100</span>
          </div>
        </div>

      </div>
    </div>
  );
}