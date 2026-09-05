import React, { useEffect, useState } from 'react';
import { Layers, AlertTriangle, ShieldBan, Clock, AlertCircle } from 'lucide-react';
import { fetchPlatformMetrics } from '../services/api';

export default function OverviewStats() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadMetrics() {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchPlatformMetrics();
        if (isMounted) {
          setMetrics(data);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || 'Failed to load system metrics');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    loadMetrics();

    return () => {
      isMounted = false;
    };
  }, []);

  const cards = [
    {
      label: 'TOTAL TRANSACTIONS',
      value: metrics?.total_transactions !== undefined ? Number(metrics.total_transactions).toLocaleString() : '--',
      icon: Layers,
      color: 'text-slate-400'
    },
    {
      label: 'FRAUD CASES',
      value: metrics?.fraud_cases !== undefined ? Number(metrics.fraud_cases).toLocaleString() : '--',
      icon: AlertTriangle,
      color: 'text-amber-400'
    },
    {
      label: 'FRAUD RING CASES',
      value: metrics?.fraud_ring_cases !== undefined ? Number(metrics.fraud_ring_cases).toLocaleString() : '--',
      icon: ShieldBan,
      color: 'text-rose-400'
    },
    {
      label: 'BEHAVIORAL ANOMALIES',
      value: metrics?.behavioral_anomalies !== undefined ? Number(metrics.behavioral_anomalies).toLocaleString() : '--',
      icon: Clock,
      color: 'text-cyan-400'
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {cards.map((item, idx) => {
        const Icon = item.icon;
        return (
          <div
            key={idx}
            className="bg-radar-900/60 border border-radar-border rounded-lg p-4 relative overflow-hidden backdrop-blur-sm"
          >
            <div className="flex justify-between items-start">
              <div>
                <p className="text-[11px] uppercase tracking-wider font-semibold text-slate-400 mb-1">
                  {item.label}
                </p>
                {loading ? (
                  <div className="h-7 w-24 bg-radar-800 animate-pulse rounded my-0.5" />
                ) : error ? (
                  <div className="flex items-center space-x-1 text-xs text-rose-400 font-mono mt-1">
                    <AlertCircle className="h-3.5 w-3.5 flex-shrink-0" />
                    <span>Unavailable</span>
                  </div>
                ) : (
                  <h3 className="text-xl font-bold font-mono text-slate-100">
                    {item.value}
                  </h3>
                )}
              </div>
              <div className="p-2 rounded bg-radar-850 border border-radar-700/50">
                <Icon className={`h-4 w-4 ${item.color}`} />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}