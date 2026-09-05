const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export async function fetchTransactionRisk(transactionId) {
  try {
    const response = await fetch(`${BASE_URL}/transactions/${encodeURIComponent(transactionId)}/risk`, {
      headers: {
        'Accept': 'application/json',
      }
    });

    if (response.status === 404) {
      throw new Error(`Transaction ID "${transactionId}" was not found in the cluster.`);
    }

    if (!response.ok) {
      throw new Error(`Platform API error: status ${response.status} (${response.statusText})`);
    }

    return await response.json();
  } catch (err) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      throw new Error('Backend engine is unreachable. Ensure the FastAPI service is running on ' + BASE_URL);
    }
    throw err;
  }
}

export async function fetchPlatformMetrics() {
  try {
    const response = await fetch(`${BASE_URL}/metrics`, {
      headers: {
        'Accept': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`Metrics API error: status ${response.status} (${response.statusText})`);
    }

    return await response.json();
  } catch (err) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      throw new Error('Backend engine unreachable on ' + BASE_URL);
    }
    throw err;
  }
}