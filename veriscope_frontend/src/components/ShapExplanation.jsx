import React from 'react';
import { formatFeatureName } from '../utils/formatters';
import { TrendingUp, TrendingDown, HelpCircle } from 'lucide-react';

export default function ShapExplanation({ reasons = [] }) {
  return (
    <div className="bg-radar-900 border border-radar-border rounded-lg p-5 mb-6">
      <div className="flex items-center justify-between pb-4 mb-4 border-b border-radar-800">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono">
            Why did the engine reach this decision?
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Local SHAP value contribution breakdown determining risk deviation.
          </p>
        </div>
        <div className="flex items-center text-xs text-slate-500 gap-1">
          <HelpCircle className="h-3.5 w-3.5" />
          <span>Explainable AI (XAI)</span>
        </div>
      </div>

      {(!reasons || reasons.length === 0) ? (
        <p className="text-xs text-slate-500 italic">No direct feature anomalies identified for this transaction event.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {reasons.map((item, index) => {
            const isIncrease = item.direction === 'increases';
            return (
              <div 
                key={index} 
                className="bg-radar-950/70 border border-radar-800 rounded-md p-3 flex items-center justify-between hover:border-radar-700 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <div className={`p-1.5 rounded ${isIncrease ? 'bg-rose-500/10 text-rose-400' : 'bg-emerald-500/10 text-emerald-400'}`}>
                    {isIncrease ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                  </div>
                  <div>
                    <div className="text-xs font-medium text-slate-200">
                      {formatFeatureName(item.feature)}
                    </div>
                    <div className="text-[10px] font-mono text-slate-400 uppercase">
                      Impact: {item.direction} risk
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <div className={`font-mono text-xs font-bold ${isIncrease ? 'text-rose-400' : 'text-emerald-400'}`}>
                    {isIncrease ? `+${item.shap_value.toFixed(2)}` : item.shap_value.toFixed(2)}
                  </div>
                  <div className="text-[9px] font-mono text-slate-500 uppercase">SHAP Weight</div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}