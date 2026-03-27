import React from 'react';
import { 
  ShieldAlert, AlertTriangle, TrendingDown, TrendingUp,
  Activity, Heart, LifeBuoy, Mail, ArrowRight
} from 'lucide-react';

function getRiskConfig(level) {
  const configs = {
    critical: { color: 'rose', gradient: 'from-rose-500 to-rose-600', icon: '🔴', bgRing: 'ring-rose-500/30' },
    high: { color: 'orange', gradient: 'from-orange-500 to-orange-600', icon: '🟠', bgRing: 'ring-orange-500/30' },
    medium: { color: 'amber', gradient: 'from-amber-500 to-amber-600', icon: '🟡', bgRing: 'ring-amber-500/30' },
    low: { color: 'emerald', gradient: 'from-emerald-500 to-emerald-600', icon: '🟢', bgRing: 'ring-emerald-500/30' },
  };
  return configs[level] || configs.medium;
}

export default function ChurnRiskCard({ result, accountName }) {
  if (!result) return null;

  const config = getRiskConfig(result.risk_level);
  const probability = result.churn_probability || 0;

  return (
    <div className="glass-card p-6 animate-slide-up">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-rose-500/10">
          <ShieldAlert className="w-5 h-5 text-rose-400" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Churn Risk Analysis</h3>
          <p className="text-xs text-surface-200/50">
            {accountName || result.account_info?.name || 'Account'}
          </p>
        </div>
      </div>

      {/* Risk Gauge */}
      <div className="flex items-center gap-6 mb-6 p-4 rounded-xl bg-surface-900/50 border border-white/5">
        <div className="relative flex-shrink-0">
          <svg className="w-24 h-24 -rotate-90" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" strokeWidth="8" className="text-surface-700" />
            <circle
              cx="50" cy="50" r="40" fill="none" strokeWidth="8"
              strokeLinecap="round"
              stroke={probability >= 70 ? '#f43f5e' : probability >= 50 ? '#f59e0b' : probability >= 30 ? '#f59e0b' : '#10b981'}
              strokeDasharray={`${probability * 2.51} 251`}
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-xl font-bold text-white">{probability.toFixed(0)}%</span>
            <span className="text-[10px] text-surface-200/40">CHURN</span>
          </div>
        </div>
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            <span className={`badge badge-${result.risk_level}`}>
              {config.icon} {result.risk_level.toUpperCase()}
            </span>
          </div>
          <p className="text-xs text-surface-200/60">
            Health trend: <span className={`font-medium ${
              result.health_trend === 'declining' ? 'text-rose-400' :
              result.health_trend === 'improving' ? 'text-emerald-400' : 'text-amber-400'
            }`}>
              {result.health_trend === 'declining' && <TrendingDown className="w-3 h-3 inline mr-1" />}
              {result.health_trend === 'improving' && <TrendingUp className="w-3 h-3 inline mr-1" />}
              {result.health_trend}
            </span>
          </p>
          <p className="text-xs text-surface-200/40">
            Predicted window: {result.predicted_churn_window}
          </p>
          {result.account_info && (
            <p className="text-xs text-surface-200/40">
              MRR at risk: <span className="text-rose-400 font-medium">${result.account_info.mrr?.toLocaleString()}</span>
            </p>
          )}
        </div>
      </div>

      {/* Risk Factors */}
      <div className="mb-5">
        <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-400" />
          Risk Factors
        </h4>
        <div className="space-y-2">
          {result.risk_factors?.map((factor, idx) => (
            <div key={idx} className="flex items-start gap-2 text-xs text-surface-200/60 py-1.5 px-3 rounded-lg bg-surface-800/50">
              <span className="text-amber-400 mt-0.5">⚠</span>
              {factor}
            </div>
          ))}
        </div>
      </div>

      {/* Intervention */}
      {result.intervention && (
        <div className="mb-5 p-4 rounded-xl bg-gradient-to-r from-primary-500/5 to-cyan-500/5 border border-primary-500/10">
          <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
            <LifeBuoy className="w-4 h-4 text-primary-400" />
            Recommended Intervention
          </h4>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="badge badge-medium">{result.intervention.urgency}</span>
              <span className="text-sm font-medium text-white">{result.intervention.type}</span>
            </div>
            <p className="text-xs text-surface-200/60 leading-relaxed">{result.intervention.description}</p>
            <p className="text-xs text-surface-200/40 italic">{result.intervention.expected_impact}</p>
          </div>
        </div>
      )}

      {/* Save Email */}
      {result.save_email_draft && (
        <div>
          <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Mail className="w-4 h-4 text-cyan-400" />
            Retention Email Draft
          </h4>
          <div className="p-4 rounded-xl bg-surface-900/50 border border-white/5 max-h-[200px] overflow-y-auto">
            <pre className="text-xs text-surface-200/60 whitespace-pre-wrap font-sans leading-relaxed">
              {result.save_email_draft}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
