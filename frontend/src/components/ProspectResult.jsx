import React from 'react';
import {
  Target, Mail, ArrowRight, Lightbulb, Star,
  MessageSquare, Linkedin, Send
} from 'lucide-react';

export default function ProspectResult({ result }) {
  if (!result) return null;

  const scoreColor = result.lead_score >= 75 ? 'text-emerald-400' :
    result.lead_score >= 50 ? 'text-amber-400' : 'text-rose-400';

  return (
    <div className="glass-card p-6 animate-slide-up">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-primary-500/10">
          <Target className="w-5 h-5 text-primary-400" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Prospect Analysis</h3>
          <p className="text-xs text-surface-200/50">AI-generated insights & outreach</p>
        </div>
      </div>

      {/* Lead Score */}
      <div className="flex items-center gap-6 mb-6 p-4 rounded-xl bg-surface-900/50 border border-white/5">
        <div className="text-center">
          <div className={`text-4xl font-bold ${scoreColor}`}>{result.lead_score?.toFixed(0)}</div>
          <div className="text-[10px] text-surface-200/40 uppercase tracking-wider mt-1">Lead Score</div>
        </div>
        <div className="flex-1 grid grid-cols-2 gap-2">
          {result.score_breakdown && Object.entries(result.score_breakdown).map(([key, value]) => (
            <div key={key} className="text-xs">
              <span className="text-surface-200/40 capitalize">{key.replace(/_/g, ' ')}: </span>
              <span className="text-white font-medium">{typeof value === 'number' ? value.toFixed(1) : value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Key Insights */}
      <div className="mb-5">
        <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
          <Lightbulb className="w-4 h-4 text-amber-400" />
          Key Insights
        </h4>
        <div className="space-y-2">
          {result.key_insights?.map((insight, idx) => (
            <div key={idx} className="flex items-start gap-2 text-xs text-surface-200/60 py-1.5 px-3 rounded-lg bg-surface-800/50">
              <Star className="w-3.5 h-3.5 text-amber-400/60 flex-shrink-0 mt-0.5" />
              {insight}
            </div>
          ))}
        </div>
      </div>

      {/* Recommended Approach */}
      <div className="mb-5 p-4 rounded-xl bg-gradient-to-r from-primary-500/5 to-cyan-500/5 border border-primary-500/10">
        <h4 className="text-sm font-semibold text-white mb-2">📋 Recommended Approach</h4>
        <p className="text-xs text-surface-200/60 leading-relaxed">{result.recommended_approach}</p>
      </div>

      {/* Outreach Sequence */}
      {result.outreach_sequence && (
        <div>
          <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Send className="w-4 h-4 text-cyan-400" />
            3-Step Outreach Sequence
          </h4>
          <div className="space-y-3">
            {result.outreach_sequence.map((step, idx) => {
              const channelIcon = step.channel === 'LinkedIn'
                ? <Linkedin className="w-3.5 h-3.5" />
                : <Mail className="w-3.5 h-3.5" />;

              return (
                <div key={idx} className="p-4 rounded-xl bg-surface-900/50 border border-white/5">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="flex items-center justify-center w-5 h-5 rounded-full bg-primary-500/20 text-primary-400 text-[10px] font-bold">
                      {step.step}
                    </span>
                    <span className="text-xs font-medium text-white">{step.channel}</span>
                    {channelIcon}
                    <span className="text-xs text-surface-200/40 ml-auto">{step.timing}</span>
                  </div>
                  <p className="text-xs font-medium text-surface-200/80 mb-1">{step.subject}</p>
                  <div>
                    <pre className="text-[11px] text-surface-200/50 whitespace-pre-wrap font-sans leading-relaxed">
                      {step.message}
                    </pre>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
