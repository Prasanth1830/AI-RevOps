import React from 'react';
import {
  Swords, Shield, Target, MessageCircle,
  CheckCircle2, XCircle, Zap, ArrowRight
} from 'lucide-react';

export default function CompetitiveResult({ result }) {
  if (!result) return null;

  const riskColors = {
    critical: 'badge-critical',
    high: 'badge-high',
    medium: 'badge-medium',
    low: 'badge-low',
  };

  return (
    <div className="glass-card p-6 animate-slide-up">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-cyan-500/10">
          <Swords className="w-5 h-5 text-cyan-400" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Competitive Intelligence</h3>
          <p className="text-xs text-surface-200/50">
            vs. {result.primary_competitor} — {result.deal_info?.name || 'Deal'}
          </p>
        </div>
      </div>

      {/* Risk & Competitor Summary */}
      <div className="flex items-center gap-4 mb-6 p-4 rounded-xl bg-surface-900/50 border border-white/5">
        <div>
          <span className={`badge ${riskColors[result.competitor_risk_flag]}`}>
            {result.competitor_risk_flag?.toUpperCase()} RISK
          </span>
        </div>
        <div className="text-xs text-surface-200/50">
          Primary: <span className="text-white font-medium">{result.primary_competitor}</span>
        </div>
        {result.competitors_analyzed && (
          <div className="text-xs text-surface-200/40">
            {result.competitors_analyzed.length} competitor(s) analyzed
          </div>
        )}
      </div>

      {/* Positioning */}
      <div className="mb-5 p-4 rounded-xl bg-gradient-to-r from-cyan-500/5 to-primary-500/5 border border-cyan-500/10">
        <h4 className="text-sm font-semibold text-white mb-2">🎯 Competitive Positioning</h4>
        <p className="text-xs text-surface-200/60 leading-relaxed">{result.competitive_positioning}</p>
      </div>

      {/* Battlecards */}
      {result.battlecard && result.battlecard.length > 0 && (
        <div className="mb-5">
          <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Shield className="w-4 h-4 text-cyan-400" />
            Battlecards
          </h4>
          <div className="space-y-3">
            {result.battlecard.map((card, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-surface-900/50 border border-white/5">
                <h5 className="text-sm font-semibold text-white mb-3">{card.category}</h5>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div>
                    <p className="text-[10px] uppercase tracking-wider text-emerald-400/60 font-semibold mb-2">Our Strengths</p>
                    {card.our_strengths?.map((s, i) => (
                      <div key={i} className="flex items-start gap-1.5 text-xs text-surface-200/60 mb-1.5">
                        <CheckCircle2 className="w-3 h-3 text-emerald-400/60 flex-shrink-0 mt-0.5" />
                        {s}
                      </div>
                    ))}
                  </div>
                  <div>
                    <p className="text-[10px] uppercase tracking-wider text-rose-400/60 font-semibold mb-2">
                      Their Weaknesses
                    </p>
                    {card.competitor_weaknesses?.map((w, i) => (
                      <div key={i} className="flex items-start gap-1.5 text-xs text-surface-200/60 mb-1.5">
                        <XCircle className="w-3 h-3 text-rose-400/60 flex-shrink-0 mt-0.5" />
                        {w}
                      </div>
                    ))}
                  </div>
                  <div>
                    <p className="text-[10px] uppercase tracking-wider text-primary-400/60 font-semibold mb-2">
                      Differentiators
                    </p>
                    {card.key_differentiators?.map((d, i) => (
                      <div key={i} className="flex items-start gap-1.5 text-xs text-surface-200/60 mb-1.5">
                        <Zap className="w-3 h-3 text-primary-400/60 flex-shrink-0 mt-0.5" />
                        {d}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Win Strategy */}
      <div className="mb-5 p-4 rounded-xl bg-surface-900/50 border border-white/5">
        <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
          <Target className="w-4 h-4 text-emerald-400" />
          Win Strategy
        </h4>
        <pre className="text-xs text-surface-200/60 whitespace-pre-wrap font-sans leading-relaxed">
          {result.win_strategy}
        </pre>
      </div>

      {/* Objection Handlers */}
      {result.objection_handlers && result.objection_handlers.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <MessageCircle className="w-4 h-4 text-violet-400" />
            Objection Handlers
          </h4>
          <div className="space-y-3">
            {result.objection_handlers.map((handler, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-surface-800/50 border border-white/5">
                <p className="text-xs font-medium text-rose-300 mb-1.5">
                  ❝ {handler.objection}
                </p>
                <p className="text-xs text-surface-200/60 leading-relaxed">
                  → {handler.response}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
