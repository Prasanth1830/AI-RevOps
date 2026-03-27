import React, { useState } from 'react';
import {
  AlertTriangle, DollarSign, Flag, Search,
  TrendingUp, Layers, ChevronRight, Building2,
  User, BarChart3, Briefcase, Globe, Shield,
  Cpu, Zap, Database
} from 'lucide-react';

const stageConfig = {
  discovery: { label: 'Discovery', color: '#6366f1', dot: 'bg-indigo-500' },
  qualification: { label: 'Qualification', color: '#06b6d4', dot: 'bg-cyan-500' },
  proposal: { label: 'Proposal', color: '#8b5cf6', dot: 'bg-violet-500' },
  negotiation: { label: 'Negotiation', color: '#f59e0b', dot: 'bg-amber-500' },
  closed_won: { label: 'Won', color: '#10b981', dot: 'bg-emerald-500' },
  closed_lost: { label: 'Lost', color: '#f43f5e', dot: 'bg-rose-500' },
};

function getPriorityBadge(riskScore) {
  if (riskScore >= 0.7) return { label: 'AT RISK', bg: 'bg-rose-500/15', text: 'text-rose-400', border: 'border-rose-500/25' };
  if (riskScore >= 0.5) return { label: 'HIGH PRIORITY', bg: 'bg-amber-500/15', text: 'text-amber-400', border: 'border-amber-500/25' };
  if (riskScore >= 0.3) return { label: 'IN PROGRESS', bg: 'bg-primary-500/15', text: 'text-primary-400', border: 'border-primary-500/25' };
  return { label: 'ON TRACK', bg: 'bg-emerald-500/15', text: 'text-emerald-400', border: 'border-emerald-500/25' };
}

// Deterministic icon based on deal name
const dealIcons = [Building2, Globe, Shield, Cpu, Zap, Database, Briefcase, BarChart3, Layers];
function getDealIcon(name) {
  const idx = name.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0) % dealIcons.length;
  return dealIcons[idx];
}

// Deterministic gradient based on deal name
const iconGradients = [
  'from-indigo-500/20 to-violet-500/20',
  'from-cyan-500/20 to-blue-500/20',
  'from-emerald-500/20 to-teal-500/20',
  'from-amber-500/20 to-orange-500/20',
  'from-rose-500/20 to-pink-500/20',
  'from-violet-500/20 to-fuchsia-500/20',
];
function getIconGradient(name) {
  const idx = name.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0) % iconGradients.length;
  return iconGradients[idx];
}

function DealCard({ deal, onAnalyze, onCompetitive, index }) {
  const stage = stageConfig[deal.stage] || stageConfig.discovery;
  const priority = getPriorityBadge(deal.risk_score);
  const hasCompetitors = deal.competitor_mentions && deal.competitor_mentions.length > 0;
  const Icon = getDealIcon(deal.deal_name);
  const gradient = getIconGradient(deal.deal_name);

  return (
    <div
      className="relative rounded-2xl border border-white/[0.06] bg-surface-800/40 backdrop-blur-sm p-5 transition-all duration-300 hover:border-white/[0.12] hover:bg-surface-800/60 hover:shadow-lg hover:shadow-primary-500/5 group animate-slide-up"
      style={{ animationDelay: `${index * 60}ms` }}
    >
      {/* Top Row: Icon + Name + Badge */}
      <div className="flex items-start gap-3.5 mb-4">
        <div className={`flex-shrink-0 w-11 h-11 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center border border-white/5`}>
          <Icon className="w-5 h-5 text-surface-200/70" />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-[15px] font-semibold text-white leading-tight truncate">
            {deal.deal_name}
          </h4>
          <div className="flex items-center gap-1.5 mt-1">
            <User className="w-3 h-3 text-surface-200/30" />
            <span className="text-xs text-surface-200/40">{deal.owner}</span>
          </div>
        </div>
        <span className={`flex-shrink-0 inline-flex items-center px-2.5 py-1 rounded-lg text-[10px] font-bold tracking-wide ${priority.bg} ${priority.text} border ${priority.border}`}>
          {priority.label}
        </span>
      </div>

      {/* Competitors */}
      {hasCompetitors && (
        <div className="flex items-center gap-1.5 mb-3 px-1">
          <Flag className="w-3 h-3 text-amber-400/60" />
          <span className="text-[11px] text-surface-200/40">
            {deal.competitor_mentions.join(', ')}
          </span>
        </div>
      )}

      {/* Value + Stage Row */}
      <div className="flex items-end justify-between mb-4 px-1">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-surface-200/30 font-medium mb-1">Value</p>
          <div className="flex items-center gap-1.5">
            <DollarSign className="w-4 h-4 text-emerald-400/70" />
            <span className="text-xl font-bold text-white tracking-tight">
              ${deal.amount >= 1000000 ? (deal.amount / 1000000).toFixed(1) + 'M' : (deal.amount / 1000).toFixed(0) + 'K' }
            </span>
          </div>
        </div>
        <div className="text-right">
          <p className="text-[10px] uppercase tracking-widest text-surface-200/30 font-medium mb-1">Stage</p>
          <div className="flex items-center gap-2">
            <div className={`w-2.5 h-2.5 rounded-full ${stage.dot} shadow-sm`} style={{ boxShadow: `0 0 8px ${stage.color}40` }} />
            <span className="text-sm font-semibold text-white">{stage.label}</span>
          </div>
        </div>
      </div>

      {/* Win probability bar */}
      <div className="mb-4 px-1">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] text-surface-200/30 uppercase tracking-wider font-medium">Win Probability</span>
          <span className="text-[11px] font-bold text-surface-200/60">{Math.round(deal.probability * 100)}%</span>
        </div>
        <div className="h-1.5 rounded-full bg-surface-700/50 overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-700 ease-out"
            style={{
              width: `${deal.probability * 100}%`,
              background: `linear-gradient(90deg, ${stage.color}, ${stage.color}99)`
            }}
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-2.5">
        <button
          onClick={() => onAnalyze(deal.id)}
          className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-semibold text-surface-200/70 bg-surface-700/40 border border-white/5 hover:bg-primary-500/10 hover:text-primary-400 hover:border-primary-500/20 transition-all duration-200"
        >
          <AlertTriangle className="w-3.5 h-3.5" />
          Analyze Risk
        </button>
        <button
          onClick={() => onCompetitive(deal.id)}
          className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-semibold text-surface-200/70 bg-gradient-to-r from-primary-500/10 to-cyan-500/10 border border-primary-500/15 hover:from-primary-500/20 hover:to-cyan-500/20 hover:text-primary-400 hover:border-primary-500/25 transition-all duration-200"
        >
          <Flag className="w-3.5 h-3.5" />
          Battlecard
        </button>
      </div>
    </div>
  );
}

export default function DealPipeline({ deals, onAnalyze, onCompetitive }) {
  const [activeFilter, setActiveFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  if (!deals || deals.length === 0) return null;

  const activeDeals = deals.filter(d => d.stage !== 'closed_won' && d.stage !== 'closed_lost');
  const totalPipeline = activeDeals.reduce((sum, d) => sum + d.amount, 0);
  const newThisWeek = Math.floor(activeDeals.length * 0.35);

  const filters = [
    { id: 'all', label: 'All Deals' },
    { id: 'high_risk', label: 'At Risk' },
    { id: 'active', label: 'Active' },
    { id: 'won', label: 'Won' },
  ];

  let filteredDeals = deals;
  if (activeFilter === 'high_risk') filteredDeals = deals.filter(d => d.risk_score >= 0.5);
  else if (activeFilter === 'active') filteredDeals = activeDeals;
  else if (activeFilter === 'won') filteredDeals = deals.filter(d => d.stage === 'closed_won');

  if (searchTerm) {
    filteredDeals = filteredDeals.filter(d =>
      d.deal_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.owner.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }

  return (
    <div className="glass-card p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-primary-500/10 to-violet-500/10 border border-primary-500/10">
            <Layers className="w-5 h-5 text-primary-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Pipeline</h3>
            <p className="text-xs text-surface-200/40">{deals.length} deals across all stages</p>
          </div>
        </div>
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-surface-200/30" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search deals..."
            className="pl-9 pr-4 py-2 w-48 rounded-xl bg-surface-800/50 border border-white/5 text-xs text-white placeholder:text-surface-200/25 focus:outline-none focus:border-primary-500/30 transition-colors"
          />
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 gap-3 mb-5">
        <div className="rounded-xl bg-surface-800/40 border border-white/5 p-4">
          <p className="text-[10px] uppercase tracking-widest text-surface-200/30 font-medium mb-1">Total Pipeline</p>
          <p className="text-2xl font-bold text-white">
            ${totalPipeline >= 1000000 ? (totalPipeline / 1000000).toFixed(1) + 'M' : (totalPipeline / 1000).toFixed(0) + 'K'}
          </p>
          <div className="flex items-center gap-1 mt-1">
            <TrendingUp className="w-3 h-3 text-emerald-400" />
            <span className="text-[11px] text-emerald-400 font-medium">↗ 12% vs LW</span>
          </div>
        </div>
        <div className="rounded-xl bg-surface-800/40 border border-white/5 p-4">
          <p className="text-[10px] uppercase tracking-widest text-surface-200/30 font-medium mb-1">Active Deals</p>
          <p className="text-2xl font-bold text-white">{activeDeals.length}</p>
          <div className="flex items-center gap-1 mt-1">
            <span className="text-[11px] text-surface-200/40">≡ {newThisWeek} New this week</span>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-1.5 mb-5 p-1 rounded-xl bg-surface-800/30">
        {filters.map(f => (
          <button
            key={f.id}
            onClick={() => setActiveFilter(f.id)}
            className={`flex-1 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
              activeFilter === f.id
                ? 'bg-primary-500/15 text-primary-400 shadow-sm'
                : 'text-surface-200/40 hover:text-surface-200/60 hover:bg-white/3'
            }`}
          >
            {f.label}
            {f.id === 'high_risk' && (
              <span className="ml-1.5 inline-flex items-center justify-center w-4 h-4 rounded-full bg-rose-500/20 text-rose-400 text-[9px] font-bold">
                {deals.filter(d => d.risk_score >= 0.5).length}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Active Opportunities Header */}
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-sm font-semibold text-white">Active Opportunities</h4>
        <span className="text-xs text-surface-200/30">{filteredDeals.length} deals</span>
      </div>

      {/* Deal Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-[700px] overflow-y-auto pr-1">
        {filteredDeals.map((deal, idx) => (
          <DealCard
            key={deal.id}
            deal={deal}
            index={idx}
            onAnalyze={onAnalyze}
            onCompetitive={onCompetitive}
          />
        ))}
        {filteredDeals.length === 0 && (
          <div className="col-span-3 py-12 text-center text-sm text-surface-200/25">
            No deals match your filters
          </div>
        )}
      </div>
    </div>
  );
}
