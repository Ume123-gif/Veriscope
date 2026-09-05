import React, { useState } from 'react';

import Navbar from './components/Navbar';
import OverviewStats from './components/OverviewStats';
import SearchBar from './components/SearchBar';
import DecisionBanner from './components/DecisionBanner';
import RiskScores from './components/RiskScores';
import ShapExplanation from './components/ShapExplanation';
import NetworkIntelligence from './components/NetworkIntelligence';
import AuditTrail from './components/AuditTrail';

import { fetchTransactionRisk } from './services/api';

import {
  EmptyState,
  ErrorState,
  SkeletonLoader
} from './components/States';

export default function App() {
  const [activeTab, setActiveTab] = useState('investigation');

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (transactionId) => {
    if (!transactionId?.trim()) {
      return;
    }

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await fetchTransactionRisk(transactionId.trim());
      setData(result);
    } catch (err) {
      setError(err.message || 'Unable to analyze transaction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-radar-950 text-slate-200">
      
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Platform Overview */}
        <OverviewStats />

        {/* Investigation Tab */}
        {activeTab === 'investigation' ? (
          <div className="mt-8">

            {/* Transaction Search */}
            <SearchBar
              onSearch={handleSearch}
              loading={loading}
            />

            {/* Loading State */}
            {loading && (
              <div className="mt-6">
                <SkeletonLoader />
              </div>
            )}

            {/* Error State */}
            {error && !loading && (
              <div className="mt-6">
                <ErrorState error={error} />
              </div>
            )}

            {/* Initial Empty State */}
            {!loading && !error && !data && (
              <div className="mt-6">
                <EmptyState />
              </div>
            )}

            {/* Investigation Results */}
            {!loading && !error && data && (
              <div className="mt-6 space-y-6">

                {/* Final Decision */}
                <DecisionBanner data={data} />

                {/* Risk Component Scores */}
                <RiskScores data={data} />

                {/* Explainable AI */}
                <ShapExplanation
                  reasons={data.shap_reasons}
                />

                {/* Fraud Network Intelligence */}
                <NetworkIntelligence
                  communityId={data.community_id}
                  graphScore={data.graph_score ?? 0}
                />

              </div>
            )}

          </div>
        ) : (

          /* Investigation History Tab */
          <div className="mt-8">
            <AuditTrail />
          </div>

        )}

      </main>
    </div>
  );
}