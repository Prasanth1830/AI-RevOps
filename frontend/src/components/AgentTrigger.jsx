import React, { useState } from 'react';
import { 
  Bot, Search, AlertTriangle, ShieldAlert, Swords,
  Loader2, Play, CheckCircle2, XCircle, Clock
} from 'lucide-react';

const agentConfigs = {
  prospect: {
    name: 'Prospecting Agent',
    description: 'Score leads, generate outreach',
    icon: Search,
    color: 'primary',
    gradient: 'from-primary-500 to-primary-600',
    bgColor: 'bg-primary-500/10',
    textColor: 'text-primary-400',
  },
  deal_risk: {
    name: 'Deal Intelligence',
    description: 'Analyze deal risks & recovery',
    icon: AlertTriangle,
    color: 'amber',
    gradient: 'from-amber-500 to-amber-600',
    bgColor: 'bg-amber-500/10',
    textColor: 'text-amber-400',
  },
  churn: {
    name: 'Revenue Retention',
    description: 'Predict churn, save accounts',
    icon: ShieldAlert,
    color: 'rose',
    gradient: 'from-rose-500 to-rose-600',
    bgColor: 'bg-rose-500/10',
    textColor: 'text-rose-400',
  },
  competitive: {
    name: 'Competitive Intel',
    description: 'Battlecards & win strategies',
    icon: Swords,
    color: 'cyan',
    gradient: 'from-cyan-500 to-cyan-600',
    bgColor: 'bg-cyan-500/10',
    textColor: 'text-cyan-400',
  },
};

export default function AgentTrigger({ agentType, onTrigger, isLoading, lastResult }) {
  const config = agentConfigs[agentType];
  if (!config) return null;

  const Icon = config.icon;
  const statusIcon = isLoading ? (
    <Loader2 className="w-4 h-4 animate-spin text-primary-400" />
  ) : lastResult?.status === 'completed' ? (
    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
  ) : lastResult?.status === 'failed' ? (
    <XCircle className="w-4 h-4 text-rose-400" />
  ) : null;

  return (
    <div className="glass-card-hover p-4">
      <div className="flex items-center gap-3">
        <div className={`p-2.5 rounded-xl ${config.bgColor}`}>
          <Icon className={`w-5 h-5 ${config.textColor}`} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h4 className="text-sm font-semibold text-white">{config.name}</h4>
            {statusIcon}
          </div>
          <p className="text-xs text-surface-200/50 truncate">{config.description}</p>
        </div>
        <button
          onClick={onTrigger}
          disabled={isLoading}
          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
            isLoading
              ? 'bg-surface-700/50 text-surface-200/40 cursor-not-allowed'
              : `bg-gradient-to-r ${config.gradient} text-white hover:shadow-lg hover:shadow-${config.color}-500/20`
          }`}
        >
          {isLoading ? (
            <span className="flex items-center gap-1.5">
              <Loader2 className="w-3 h-3 animate-spin" />
              Running...
            </span>
          ) : (
            <span className="flex items-center gap-1.5">
              <Play className="w-3 h-3" />
              Run
            </span>
          )}
        </button>
      </div>

      {lastResult && lastResult.duration_ms && (
        <div className="mt-2 flex items-center gap-1 text-xs text-surface-200/30">
          <Clock className="w-3 h-3" />
          Last run: {lastResult.duration_ms}ms
        </div>
      )}
    </div>
  );
}
