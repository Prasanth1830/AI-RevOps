const API_BASE = '/api';

async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

// Dashboard
export const getDashboard = () => fetchAPI('/dashboard');

// Leads
export const getLeads = (params = {}) => {
  const query = new URLSearchParams(params).toString();
  return fetchAPI(`/leads${query ? `?${query}` : ''}`);
};

// Deals
export const getDeals = (stage = null) => fetchAPI(`/deals${stage ? `?stage=${stage}` : ''}`);
export const getDeal = (id) => fetchAPI(`/deals/${id}`);

// Accounts
export const getAccounts = () => fetchAPI('/accounts');
export const getAccount = (id) => fetchAPI(`/accounts/${id}`);

// Agent Runs
export const getAgentRuns = (limit = 20) => fetchAPI(`/agent-runs?limit=${limit}`);
export const getAgentRun = (id) => fetchAPI(`/agent-runs/${id}`);

// Agent Endpoints
export const runProspectAgent = (data) =>
  fetchAPI('/prospect', { method: 'POST', body: JSON.stringify(data) });

export const runDealRiskAgent = (data) =>
  fetchAPI('/deal-risk', { method: 'POST', body: JSON.stringify(data) });

export const runChurnAgent = (data) =>
  fetchAPI('/churn', { method: 'POST', body: JSON.stringify(data) });

export const runCompetitiveAgent = (data) =>
  fetchAPI('/competitive', { method: 'POST', body: JSON.stringify(data) });
