import React from 'react';
import { 
  TrendingUp, TrendingDown, DollarSign, Users, 
  Target, ShieldAlert, Activity, Zap
} from 'lucide-react';

function StatsCard({ title, value, subtitle, icon: Icon, trend, trendValue, color = 'primary' }) {
  const colorMap = {
    primary: 'from-primary-500/20 to-primary-600/5 border-primary-500/10',
    cyan: 'from-cyan-500/20 to-cyan-600/5 border-cyan-500/10',
    emerald: 'from-emerald-500/20 to-emerald-600/5 border-emerald-500/10',
    amber: 'from-amber-500/20 to-amber-600/5 border-amber-500/10',
    rose: 'from-rose-500/20 to-rose-600/5 border-rose-500/10',
    violet: 'from-violet-500/20 to-violet-600/5 border-violet-500/10',
  };
  const iconColorMap = {
    primary: 'text-primary-400 bg-primary-500/10',
    cyan: 'text-cyan-400 bg-cyan-500/10',
    emerald: 'text-emerald-400 bg-emerald-500/10',
    amber: 'text-amber-400 bg-amber-500/10',
    rose: 'text-rose-400 bg-rose-500/10',
    violet: 'text-violet-400 bg-violet-500/10',
  };

  return (
    <div className={`stat-card bg-gradient-to-br ${colorMap[color]} animate-fade-in`}>
      <div className="flex items-start justify-between mb-3">
        <div className={`p-2.5 rounded-xl ${iconColorMap[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
        {trend && (
          <div className={`flex items-center gap-1 text-xs font-medium ${
            trend === 'up' ? 'text-emerald-400' : 'text-rose-400'
          }`}>
            {trend === 'up' ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
            {trendValue}
          </div>
        )}
      </div>
      <div className="space-y-1">
        <p className="text-2xl font-bold text-white">{value}</p>
        <p className="text-xs text-surface-200/60 font-medium uppercase tracking-wider">{title}</p>
        {subtitle && <p className="text-xs text-surface-200/40 mt-1">{subtitle}</p>}
      </div>
    </div>
  );
}

export default function StatsOverview({ data }) {
  if (!data) return null;

  const { pipeline, leads, accounts } = data;

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <StatsCard
        title="Pipeline Value"
        value={`$${(pipeline.total_value / 1000).toFixed(0)}K`}
        subtitle={`${pipeline.active_deals} active deals`}
        icon={DollarSign}
        trend="up"
        trendValue="+12%"
        color="primary"
      />
      <StatsCard
        title="Win Rate"
        value={`${pipeline.win_rate}%`}
        subtitle={`${pipeline.total_deals} total deals`}
        icon={Target}
        trend="up"
        trendValue="+5%"
        color="emerald"
      />
      <StatsCard
        title="Total Leads"
        value={leads.total}
        subtitle={`${leads.qualified} qualified`}
        icon={Users}
        trend="up"
        trendValue="+8%"
        color="cyan"
      />
      <StatsCard
        title="Avg Lead Score"
        value={leads.avg_score}
        subtitle={`${leads.conversion_rate}% conversion`}
        icon={Zap}
        color="violet"
      />
      <StatsCard
        title="Accounts At Risk"
        value={accounts.at_risk}
        subtitle={`of ${accounts.total} total`}
        icon={ShieldAlert}
        trend="down"
        trendValue="-2"
        color="rose"
      />
      <StatsCard
        title="Avg Health Score"
        value={accounts.avg_health_score}
        subtitle={`$${(accounts.total_mrr / 1000).toFixed(0)}K MRR`}
        icon={Activity}
        trend="up"
        trendValue="+3%"
        color="amber"
      />
    </div>
  );
}
