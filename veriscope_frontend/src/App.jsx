import React, { useState } from 'react';

import Navbar from './components/Navbar';
import OverviewStats from './components/OverviewStats';
import SearchBar from './components/SearchBar';
import DecisionBanner from './components/DecisionBanner';
import RiskScores from './components/RiskScores';
import ShapExplanation from './components/ShapExplanation';
import NetworkIntelligence from './components/NetworkIntelligence';
import { EmptyState, ErrorState, SkeletonLoader } from './components/States';

import { fetchTransactionRisk } from './services/api';

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (transactionId) => {
    setLoading(true);
    setError(null);

    try {
      const result = await fetchTransactionRisk(transactionId);
      setData(result);
    } catch (err) {
      setError(
        err.message ||
          'An unexpected failure occurred while inspecting this transaction.'
      );
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-radar-950 flex flex-col selection:bg-cyan-500/20 selection:text-cyan-300">

      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <OverviewStats />

        <div>
          <SearchBar
            onSearch={handleSearch}
            loading={loading}
          />

          {loading && <SkeletonLoader />}

          {error && !loading && (
            <ErrorState error={error} />
          )}

          {!loading && !error && !data && (
            <EmptyState />
          )}

          {!loading && !error && data && (
            <div className="space-y-6">

              <DecisionBanner data={data} />

              <RiskScores data={data} />

              <ShapExplanation
                reasons={data.shap_reasons}
              />

              <NetworkIntelligence
                communityId={data.community_id}
                graphScore={data.graph_score ?? 0}
              />

            </div>
          )}
        </div>

      </main>

      <footer className="border-t border-radar-border bg-radar-950 py-4 text-center text-xs font-mono text-slate-600">
        VERISCOPE // AUTONOMOUS TRANSACTION VERIFICATION PLATFORM
      </footer>

    </div>
  );
}