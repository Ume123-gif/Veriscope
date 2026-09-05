import React, { useEffect, useState } from 'react';
import { Clock3, ShieldCheck } from 'lucide-react';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export default function AuditTrail() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAuditTrail = async () => {
      try {
        const response = await fetch(`${BASE_URL}/audit-trail`);

        if (!response.ok) {
          throw new Error('Failed to fetch audit trail');
        }

        const data = await response.json();
        setLogs(data);
      } catch (error) {
        console.error('Audit trail error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAuditTrail();
  }, []);

  return (
    <section className="rounded-xl border border-radar-border bg-radar-900/40 overflow-hidden">
      <div className="px-5 py-4 border-b border-radar-border flex items-center justify-between">
        <div>
          <h2 className="text-sm font-mono font-bold tracking-wider text-white">
            INVESTIGATION HISTORY
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Recent transaction risk decisions recorded by Veriscope
          </p>
        </div>

        <Clock3 className="h-4 w-4 text-slate-500" />
      </div>

      {loading ? (
        <div className="px-5 py-8 text-center text-xs font-mono text-slate-500">
          Loading investigation history...
        </div>
      ) : logs.length === 0 ? (
        <div className="px-5 py-8 text-center text-xs font-mono text-slate-500">
          No investigations recorded yet.
        </div>
      ) : (
        <div className="divide-y divide-radar-border">
          {logs.map((log, index) => (
            <div
              key={`${log.transaction_id}-${log.timestamp}-${index}`}
              className="px-5 py-4 flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-3 min-w-0">
                <div className="h-8 w-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
                  <ShieldCheck className="h-4 w-4 text-cyan-400" />
                </div>

                <div className="min-w-0">
                  <p className="text-sm font-mono text-white truncate">
                    {log.transaction_id}
                  </p>

                  <p className="text-[11px] font-mono text-slate-500 mt-1">
                    {log.timestamp
                      ? new Date(log.timestamp).toLocaleString()
                      : 'Unknown time'}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-6 shrink-0">
                <div className="text-right">
                  <p className="text-[10px] font-mono text-slate-500 uppercase">
                    Risk
                  </p>
                  <p className="text-sm font-mono text-white">
                    {Number(log.risk_score).toFixed(1)}
                  </p>
                </div>

                <div className="text-right min-w-[70px]">
                  <p className="text-[10px] font-mono text-slate-500 uppercase">
                    Decision
                  </p>
                  <p className="text-xs font-mono font-bold text-cyan-400">
                    {log.decision}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}