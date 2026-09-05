import React from 'react';
import { Cpu, Activity, GitFork } from 'lucide-react';

function GaugeCard({ title, score, icon: Icon, description }) {
  const percentage = Math.min(Math.max(score * 100, 0), 100).toFixed(1);
  
  let barColor = 'bg-emerald-500';
  if (percentage > 40) barColor = 'bg-amber-500';
  if (percentage > 70) barColor = 'bg-rose-500';

  return (
    <div className="bg-radar-900 border border-radar-border rounded-lg p-5 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium uppercase tracking-wider text-slate-400 flex items-center gap-2">
            <Icon className="h-4 w-4 text-cyan-400" />
            {title}
          </span>
          <span className="font-mono font-bold text-sm text-slate-200">{score.toFixed(2)}</span>
        </div>
        <p className="text-[11px] text-slate-400 leading-snug mb-4">{description}</p>
      </div>

      <div>
        <div className="flex justify-between text-[11px] font-mono text-slate-400 mb-1">
          <span>Likelihood</span>
          <span>{percentage}%</span>
        </div>
        <div className="w-full bg-radar-950 h-2 rounded-full overflow-hidden border border-radar-800">
          <div
            className={`h-full transition-all duration-700 ease-out ${barColor}`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    </div>
  );
}

export default function RiskScores({ data }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <GaugeCard
        title="XGBoost Classifier"
        score={data.xgb_score ?? 0}
        icon={Cpu}
        description="Gradient boosting model assessing tabular behavioral anomalies & velocity."
      />
      <GaugeCard
        title="Behavioral Anomaly"
        score={data.anomaly_score ?? 0}
        icon={Activity}
        description="Isolation-based metric scoring divergence from the customer's typical baseline."
      />
      <GaugeCard
        title="Graph Network Risk"
        score={data.graph_score ?? 0}
        icon={GitFork}
        description="Relational node risk based on proximity to flagged entities & synthetic clusters."
      />
    </div>
  );
}