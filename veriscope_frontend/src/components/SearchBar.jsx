import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

export default function SearchBar({ onSearch, loading }) {
  const [txnId, setTxnId] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (txnId.trim()) {
      onSearch(txnId.trim());
    }
  };

  return (
    <div className="bg-radar-900 border border-radar-border rounded-lg p-4 mb-6">
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
          <input
            type="text"
            value={txnId}
            onChange={(e) => setTxnId(e.target.value)}
            placeholder="Enter Transaction ID (e.g. txn_9f81d4a0, 0a8312e9-4e0...)"
            className="w-full bg-radar-950 border border-radar-700/70 focus:border-cyan-500/60 rounded-md pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-500 font-mono focus:outline-none transition-colors"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !txnId.trim()}
          className="w-full sm:w-auto px-5 py-2 bg-cyan-600 hover:bg-cyan-500 disabled:bg-radar-800 disabled:text-slate-500 text-slate-950 font-semibold text-xs tracking-wider uppercase rounded-md transition-all flex items-center justify-center space-x-2 cursor-pointer disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Analyzing</span>
            </>
          ) : (
            <span>Inspect Risk</span>
          )}
        </button>
      </form>
    </div>
  );
}