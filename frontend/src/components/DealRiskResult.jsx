import React from 'react';
import {
  AlertTriangle, Shield, Zap, MessageCircle,
  ArrowRight, CheckCircle2, TrendingDown, TrendingUp
} from 'lucide-react';

function getRiskColor(level) {
  const colors = {
    critical: { text: 'text-rose-400', bg: 'bg-rose-500/10', border: 'border-rose-500/20' },
    high: { text: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/20' },
    medium: { text: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
    low: { text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
  };
  return colors[level] || colors.medium;
}

export default function DealRiskResult({ result }) {
  if (!result) return null;

  const riskColor = getRiskColor(result.risk_level);
  const scoreColor = result.risk_score >= 70 ? 'text-rose-400' :
    result.risk_score >= 50 ? 'text-amber-400' : 
    result.risk_score >= 25 ? 'text-amber-400' : 'text-emerald-400';

  return (
    <div className="glass-card p-6 animate-slide-up">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-amber-500/10">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Deal Risk Analysis</h3>
          <p className="text-xs text-surface-200/50">
            {result.deal_info?.name || 'Deal'}
          </p>
        </div>
      </div>

      {/* Risk Score Summary */}
      <div className="flex items-center gap-6 mb-6 p-4 rounded-xl bg-surface-900/50 border border-white/5">
        <div className="text-center">
          <div className={`text-4xl font-bold ${scoreColor}`}>{result.risk_score?.toFixed(0)}</div>
          <div className="text-[10px] text-surface-200/40 uppercase tracking-wider mt-1">Risk Score</div>
        </div>
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            <span className={`badge badge-${result.risk_level}`}>
              {result.risk_level?.toUpperCase()}
            </span>
            <span className={`text-xs ${
              result.engagement_trend === 'declining' ? 'text-rose-400' :
              result.engagement_trend === 'improving' ? 'text-emerald-400' : 'text-amber-400'
            }`}>
              {result.engagement_trend === 'declining' && <TrendingDown className="w-3 h-3 inline mr-1" />}
              {result.engagement_trend === 'improving' && <TrendingUp className="w-3 h-3 inline mr-1" />}
              {result.engagement_trend} engagement
            </span>
          </div>
          {result.deal_info && (
            <div className="text-xs text-surface-200/40">
              <span className="text-white font-medium">${result.deal_info.amount?.toLocaleString()}</span>
              {' · '}{result.deal_info.stage}{' · '}{result.deal_info.owner}
            </div>
          )}
        </div>
      </div>

      {/* Health Summary */}
      <div className="mb-5 p-4 rounded-xl bg-gradient-to-r from-amber-500/5 to-rose-500/5 border border-amber-500/10">
        <p className="text-xs text-surface-200/60 leading-relaxed">{result.deal_health_summary}</p>
      </div>

      {/* Risk Reasons */}
      <div className="mb-5">
        <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-rose-400" />
          Risk Signals ({result.risk_reasons?.length || 0})
        </h4>
        <div className="space-y-2">
          {result.risk_reasons?.map((reason, idx) => (
            <div key={idx} className="flex items-start gap-2 text-xs text-surface-200/60 py-2 px-3 rounded-lg bg-surface-800/50">
              <span className="text-rose-400 mt-0.5">●</span>
              {reason}
            </div>
          ))}
        </div>
      </div>

      {/* Recovery Plan */}
      {result.recovery_plan && result.recovery_plan.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Shield className="w-4 h-4 text-primary-400" />
            Recovery Plan
          </h4>
          <div className="space-y-3">
            {result.recovery_plan.map((action, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-surface-900/50 border border-white/5">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`badge badge-${action.priority === 'urgent' ? 'critical' : action.priority === 'high' ? 'high' : 'medium'}`}>
                    {action.priority}
                  </span>
                  <span className="text-sm font-medium text-white">{action.action}</span>
                  <span className="text-xs text-surface-200/30 ml-auto">{action.timeline}</span>
                </div>
                <div className="space-y-1.5 mt-2">
                  {action.talking_points?.map((point, pidx) => (
                    <div key={pidx} className="flex items-start gap-2 text-xs text-surface-200/50">
                      <ArrowRight className="w-3 h-3 text-primary-400/60 flex-shrink-0 mt-0.5" />
                      {point}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
