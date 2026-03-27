import React, { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Bot, LayoutDashboard, Search, AlertTriangle,
  ShieldAlert, Swords, Activity, Wifi, WifiOff,
  Sparkles, ChevronRight, Zap
} from 'lucide-react';

// Components
import StatsOverview from './components/StatsOverview';
import DealPipeline from './components/DealPipeline';
import ProspectForm from './components/ProspectForm';
import ProspectResult from './components/ProspectResult';
import ChurnRiskCard from './components/ChurnRiskCard';
import DealRiskResult from './components/DealRiskResult';
import CompetitiveResult from './components/CompetitiveResult';
import AgentTrigger from './components/AgentTrigger';
import AgentLogs from './components/AgentLogs';
import NotificationPanel from './components/NotificationPanel';
import { ChurnTrendChart, PipelineHealthChart, DealStageChart } from './components/Charts';

// Services
import * as api from './services/api';
import { useWebSocket } from './hooks/useWebSocket';

const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'prospect', label: 'Prospect', icon: Search },
  { id: 'deals', label: 'Deal Intel', icon: AlertTriangle },
  { id: 'churn', label: 'Churn Risk', icon: ShieldAlert },
  { id: 'competitive', label: 'Competitive', icon: Swords },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [expandedLog, setExpandedLog] = useState(null);
  const [agentResults, setAgentResults] = useState({});
  const [selectedDealId, setSelectedDealId] = useState(null);
  const [selectedAccountId, setSelectedAccountId] = useState(null);

  const queryClient = useQueryClient();
  const { notifications, isConnected, clearNotification } = useWebSocket();

  // Queries
  const { data: dashboardData, isLoading: dashLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: api.getDashboard,
    refetchInterval: 30000,
  });

  const { data: dealsData } = useQuery({
    queryKey: ['deals'],
    queryFn: () => api.getDeals(),
  });

  const { data: accountsData } = useQuery({
    queryKey: ['accounts'],
    queryFn: api.getAccounts,
  });

  // Agent Mutations
  const prospectMutation = useMutation({
    mutationFn: api.runProspectAgent,
    onSuccess: (data) => {
      setAgentResults(prev => ({ ...prev, prospect: data }));
      queryClient.invalidateQueries(['dashboard']);
    },
  });

  const dealRiskMutation = useMutation({
    mutationFn: api.runDealRiskAgent,
    onSuccess: (data) => {
      setAgentResults(prev => ({ ...prev, deal_risk: data }));
      queryClient.invalidateQueries(['dashboard']);
    },
  });

  const churnMutation = useMutation({
    mutationFn: api.runChurnAgent,
    onSuccess: (data) => {
      setAgentResults(prev => ({ ...prev, churn: data }));
      queryClient.invalidateQueries(['dashboard']);
    },
  });

  const competitiveMutation = useMutation({
    mutationFn: api.runCompetitiveAgent,
    onSuccess: (data) => {
      setAgentResults(prev => ({ ...prev, competitive: data }));
      queryClient.invalidateQueries(['dashboard']);
    },
  });

  // Handlers
  const handleAnalyzeDeal = useCallback((dealId) => {
    setSelectedDealId(dealId);
    dealRiskMutation.mutate({ deal_id: dealId, include_engagements: true });
    setActiveTab('deals');
  }, []);

  const handleCompetitiveDeal = useCallback((dealId) => {
    setSelectedDealId(dealId);
    competitiveMutation.mutate({ deal_id: dealId });
    setActiveTab('competitive');
  }, []);

  const handleRunChurn = useCallback((accountId) => {
    setSelectedAccountId(accountId);
    churnMutation.mutate({ account_id: accountId, include_usage: true });
  }, []);

  // Collect all agent runs for logs
  const allRuns = [
    ...(agentResults.prospect ? [{ id: 1, agent_type: 'prospect', status: prospectMutation.isError ? 'failed' : 'completed', ...agentResults.prospect, execution_log: agentResults.prospect?.result?.execution?.log || [] }] : []),
    ...(agentResults.deal_risk ? [{ id: 2, agent_type: 'deal_risk', status: dealRiskMutation.isError ? 'failed' : 'completed', ...agentResults.deal_risk, execution_log: agentResults.deal_risk?.result?.execution?.log || [] }] : []),
    ...(agentResults.churn ? [{ id: 3, agent_type: 'churn', status: churnMutation.isError ? 'failed' : 'completed', ...agentResults.churn, execution_log: agentResults.churn?.result?.execution?.log || [] }] : []),
    ...(agentResults.competitive ? [{ id: 4, agent_type: 'competitive', status: competitiveMutation.isError ? 'failed' : 'completed', ...agentResults.competitive, execution_log: agentResults.competitive?.result?.execution?.log || [] }] : []),
  ];

  return (
    <div className="min-h-screen bg-surface-900 bg-noise">
      {/* Background gradient orbs */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-primary-500/5 rounded-full blur-[150px]" />
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[150px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-violet-500/3 rounded-full blur-[120px]" />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-white/5 bg-surface-900/80 backdrop-blur-xl sticky top-0">
        <div className="max-w-[1600px] mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-gradient-to-br from-primary-500 to-cyan-500 shadow-lg shadow-primary-500/20">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-white flex items-center gap-2">
                  RevOps AI
                  <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20">
                    v1.0
                  </span>
                </h1>
                <p className="text-[11px] text-surface-200/40 flex items-center gap-1.5">
                  Multi-Agent Sales Intelligence Platform
                  <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[9px] font-semibold">
                    <Zap className="w-2.5 h-2.5" />
                    Powered by Gemini AI
                  </span>
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* Connection Status */}
              <div className={`flex items-center gap-1.5 text-xs ${isConnected ? 'text-emerald-400' : 'text-rose-400'}`}>
                {isConnected ? <Wifi className="w-3.5 h-3.5" /> : <WifiOff className="w-3.5 h-3.5" />}
                {isConnected ? 'Connected' : 'Offline'}
              </div>

              {/* Navigation Tabs */}
              <nav className="flex items-center gap-1 p-1 rounded-xl bg-surface-800/50 border border-white/5">
                {tabs.map(tab => {
                  const Icon = tab.icon;
                  const isActive = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 ${
                        isActive
                          ? 'bg-primary-500/20 text-primary-400 shadow-sm'
                          : 'text-surface-200/50 hover:text-surface-200/80 hover:bg-white/5'
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      <span className="hidden md:inline">{tab.label}</span>
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-[1600px] mx-auto px-6 py-6">
        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6 animate-fade-in">
            {/* Welcome */}
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-white">
                  Sales Intelligence <span className="gradient-text">Dashboard</span>
                </h2>
                <p className="text-sm text-surface-200/50 mt-1">
                  AI-powered insights across your entire revenue pipeline
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-surface-200/30">4 AI Agents Ready</span>
                <Sparkles className="w-4 h-4 text-primary-400 animate-pulse-soft" />
                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-gradient-to-r from-blue-500/10 to-cyan-500/10 text-blue-400 border border-blue-500/15 text-[10px] font-semibold">
                  <Zap className="w-3 h-3" />
                  Gemini 2.0 Flash
                </span>
              </div>
            </div>

            {/* Stats */}
            <StatsOverview data={dashboardData} />

            {/* Charts Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <ChurnTrendChart data={dashboardData?.churn_trend} />
              <PipelineHealthChart data={dashboardData?.pipeline_health} />
              <DealStageChart dealsByStage={dashboardData?.pipeline?.deals_by_stage} />
            </div>

            {/* Deal Pipeline */}
            <DealPipeline
              deals={dealsData?.deals || []}
              onAnalyze={handleAnalyzeDeal}
              onCompetitive={handleCompetitiveDeal}
            />

            {/* Bottom Row: Agent Quick Actions + Notifications + Logs */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Bot className="w-4 h-4 text-primary-400" />
                  AI Agents
                </h3>
                <AgentTrigger
                  agentType="prospect"
                  onTrigger={() => setActiveTab('prospect')}
                  isLoading={prospectMutation.isPending}
                  lastResult={agentResults.prospect}
                />
                <AgentTrigger
                  agentType="deal_risk"
                  onTrigger={() => {
                    const firstDeal = dealsData?.deals?.[0];
                    if (firstDeal) handleAnalyzeDeal(firstDeal.id);
                  }}
                  isLoading={dealRiskMutation.isPending}
                  lastResult={agentResults.deal_risk}
                />
                <AgentTrigger
                  agentType="churn"
                  onTrigger={() => {
                    setActiveTab('churn');
                    handleRunChurn(1);
                  }}
                  isLoading={churnMutation.isPending}
                  lastResult={agentResults.churn}
                />
                <AgentTrigger
                  agentType="competitive"
                  onTrigger={() => {
                    const firstDeal = dealsData?.deals?.[0];
                    if (firstDeal) handleCompetitiveDeal(firstDeal.id);
                  }}
                  isLoading={competitiveMutation.isPending}
                  lastResult={agentResults.competitive}
                />
              </div>

              <NotificationPanel
                notifications={notifications}
                onClear={clearNotification}
                isConnected={isConnected}
              />

              <AgentLogs
                runs={allRuns}
                expandedRun={expandedLog}
                onToggleExpand={(id) => setExpandedLog(expandedLog === id ? null : id)}
              />
            </div>
          </div>
        )}

        {/* Prospect Tab */}
        {activeTab === 'prospect' && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center gap-2 text-sm text-surface-200/40">
              <button onClick={() => setActiveTab('dashboard')} className="hover:text-white transition-colors">
                Dashboard
              </button>
              <ChevronRight className="w-3.5 h-3.5" />
              <span className="text-white font-medium">Prospecting Agent</span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ProspectForm
                onSubmit={(data) => prospectMutation.mutate(data)}
                isLoading={prospectMutation.isPending}
              />
              <ProspectResult result={agentResults.prospect?.result} />
            </div>
          </div>
        )}

        {/* Deal Risk Tab */}
        {activeTab === 'deals' && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center gap-2 text-sm text-surface-200/40">
              <button onClick={() => setActiveTab('dashboard')} className="hover:text-white transition-colors">
                Dashboard
              </button>
              <ChevronRight className="w-3.5 h-3.5" />
              <span className="text-white font-medium">Deal Intelligence Agent</span>
            </div>

            {/* Quick Deal Selector */}
            <div className="glass-card p-4">
              <h4 className="text-sm font-semibold text-white mb-3">Select a Deal to Analyze</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {dealsData?.deals?.slice(0, 8).map(deal => (
                  <button
                    key={deal.id}
                    onClick={() => handleAnalyzeDeal(deal.id)}
                    className={`p-3 rounded-xl text-left transition-all border ${
                      selectedDealId === deal.id
                        ? 'bg-primary-500/10 border-primary-500/20 text-white'
                        : 'bg-surface-800/30 border-white/5 text-surface-200/60 hover:border-white/10 hover:text-white'
                    }`}
                  >
                    <p className="text-xs font-medium truncate">{deal.deal_name}</p>
                    <p className="text-[10px] text-surface-200/40 mt-0.5">${(deal.amount/1000).toFixed(0)}K · {deal.stage}</p>
                  </button>
                ))}
              </div>
            </div>

            {dealRiskMutation.isPending && (
              <div className="glass-card p-12 text-center">
                <div className="inline-flex flex-col items-center gap-2 text-primary-400">
                  <Activity className="w-5 h-5 animate-pulse" />
                  <span className="text-sm font-medium">Analyzing deal risks with Gemini AI...</span>
                  <span className="text-[10px] text-surface-200/30">Generating recovery plan & talking points</span>
                </div>
              </div>
            )}

            <DealRiskResult result={agentResults.deal_risk?.result} />
          </div>
        )}

        {/* Churn Tab */}
        {activeTab === 'churn' && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center gap-2 text-sm text-surface-200/40">
              <button onClick={() => setActiveTab('dashboard')} className="hover:text-white transition-colors">
                Dashboard
              </button>
              <ChevronRight className="w-3.5 h-3.5" />
              <span className="text-white font-medium">Revenue Retention Agent</span>
            </div>

            {/* Account Selector */}
            <div className="glass-card p-4">
              <h4 className="text-sm font-semibold text-white mb-3">Select an Account to Analyze</h4>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                {accountsData?.accounts?.map(account => (
                  <button
                    key={account.id}
                    onClick={() => handleRunChurn(account.id)}
                    className={`p-3 rounded-xl text-left transition-all border ${
                      selectedAccountId === account.id
                        ? 'bg-rose-500/10 border-rose-500/20 text-white'
                        : 'bg-surface-800/30 border-white/5 text-surface-200/60 hover:border-white/10 hover:text-white'
                    }`}
                  >
                    <p className="text-xs font-medium truncate">{account.company_name}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[10px] text-surface-200/40">${(account.mrr/1000).toFixed(1)}K MRR</span>
                      <span className={`w-1.5 h-1.5 rounded-full ${
                        account.churn_risk > 0.5 ? 'bg-rose-500' : account.churn_risk > 0.3 ? 'bg-amber-500' : 'bg-emerald-500'
                      }`} />
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {churnMutation.isPending && (
              <div className="glass-card p-12 text-center">
                <div className="inline-flex flex-col items-center gap-2 text-rose-400">
                  <Activity className="w-5 h-5 animate-pulse" />
                  <span className="text-sm font-medium">Detecting churn signals with Gemini AI...</span>
                  <span className="text-[10px] text-surface-200/30">Generating intervention & save email</span>
                </div>
              </div>
            )}

            <ChurnRiskCard result={agentResults.churn?.result} />
          </div>
        )}

        {/* Competitive Tab */}
        {activeTab === 'competitive' && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center gap-2 text-sm text-surface-200/40">
              <button onClick={() => setActiveTab('dashboard')} className="hover:text-white transition-colors">
                Dashboard
              </button>
              <ChevronRight className="w-3.5 h-3.5" />
              <span className="text-white font-medium">Competitive Intelligence Agent</span>
            </div>

            {/* Deal Selector for Competitive */}
            <div className="glass-card p-4">
              <h4 className="text-sm font-semibold text-white mb-3">Select a Deal for Competitive Analysis</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {dealsData?.deals?.filter(d => d.competitor_mentions?.length > 0).slice(0, 8).map(deal => (
                  <button
                    key={deal.id}
                    onClick={() => handleCompetitiveDeal(deal.id)}
                    className={`p-3 rounded-xl text-left transition-all border ${
                      selectedDealId === deal.id
                        ? 'bg-cyan-500/10 border-cyan-500/20 text-white'
                        : 'bg-surface-800/30 border-white/5 text-surface-200/60 hover:border-white/10 hover:text-white'
                    }`}
                  >
                    <p className="text-xs font-medium truncate">{deal.deal_name}</p>
                    <p className="text-[10px] text-amber-400/60 mt-0.5">
                      vs. {deal.competitor_mentions?.join(', ')}
                    </p>
                  </button>
                ))}
              </div>
            </div>

            {competitiveMutation.isPending && (
              <div className="glass-card p-12 text-center">
                <div className="inline-flex flex-col items-center gap-2 text-cyan-400">
                  <Activity className="w-5 h-5 animate-pulse" />
                  <span className="text-sm font-medium">Gathering competitive intelligence with Gemini AI...</span>
                  <span className="text-[10px] text-surface-200/30">Generating battlecards & win strategies</span>
                </div>
              </div>
            )}

            <CompetitiveResult result={agentResults.competitive?.result} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/5 mt-12 py-6">
        <div className="max-w-[1600px] mx-auto px-6 flex items-center justify-between">
          <div className="text-xs text-surface-200/30">
            RevOps AI Platform · Hackathon 2024 · Multi-Agent Sales Intelligence
          </div>
          <div className="flex items-center gap-4 text-xs text-surface-200/20">
            <span className="inline-flex items-center gap-1 text-blue-400/50">
              <Zap className="w-3 h-3" />
              Powered by Google Gemini AI
            </span>
            <span>·</span>
            <span>4 AI Agents</span>
            <span>·</span>
            <span>Real-time WebSocket</span>
            <span>·</span>
            <span>FastAPI + React + LangChain</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
