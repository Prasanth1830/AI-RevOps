import React from 'react';
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from 'recharts';
import { TrendingUp, PieChart as PieIcon, BarChart3 } from 'lucide-react';

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e', '#8b5cf6'];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload) return null;
  return (
    <div className="bg-surface-800/95 backdrop-blur-xl border border-white/10 rounded-xl p-3 shadow-2xl">
      <p className="text-xs font-medium text-white mb-1">{label}</p>
      {payload.map((entry, idx) => (
        <p key={idx} className="text-xs" style={{ color: entry.color }}>
          {entry.name}: {typeof entry.value === 'number'
            ? entry.value >= 1000 ? `$${(entry.value/1000).toFixed(0)}K` : entry.value.toFixed(1)
            : entry.value}
        </p>
      ))}
    </div>
  );
};

export function ChurnTrendChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-rose-500/10">
          <TrendingUp className="w-5 h-5 text-rose-400" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">Churn Trend</h3>
          <p className="text-xs text-surface-200/50">Monthly churn rate & MRR loss</p>
        </div>
      </div>
      <div className="h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="churnGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#f43f5e" stopOpacity={0.3} />
                <stop offset="100%" stopColor="#f43f5e" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" />
            <XAxis dataKey="month" tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.3)' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.3)' }} axisLine={false} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="churn_rate"
              stroke="#f43f5e"
              strokeWidth={2}
              fill="url(#churnGradient)"
              name="Churn Rate %"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export function PipelineHealthChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-primary-500/10">
          <BarChart3 className="w-5 h-5 text-primary-400" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">Pipeline Health</h3>
          <p className="text-xs text-surface-200/50">Monthly pipeline value & win/loss</p>
        </div>
      </div>
      <div className="h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" />
            <XAxis dataKey="month" tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.3)' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.3)' }} axisLine={false} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="won_deals" name="Won" fill="#10b981" radius={[4, 4, 0, 0]} />
            <Bar dataKey="new_deals" name="New" fill="#6366f1" radius={[4, 4, 0, 0]} />
            <Bar dataKey="lost_deals" name="Lost" fill="#f43f5e" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export function DealStageChart({ dealsByStage }) {
  if (!dealsByStage) return null;

  const data = Object.entries(dealsByStage).map(([stage, count]) => ({
    name: stage.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
    value: count
  }));

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-violet-500/10">
          <PieIcon className="w-5 h-5 text-violet-400" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">Deal Distribution</h3>
          <p className="text-xs text-surface-200/50">Deals by pipeline stage</p>
        </div>
      </div>
      <div className="h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={80}
              paddingAngle={3}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '11px' }}
              formatter={(value) => <span className="text-surface-200/60">{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
