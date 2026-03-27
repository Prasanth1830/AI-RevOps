import React from 'react';
import { 
  CheckCircle2, Clock, XCircle, Loader2, Bot,
  ChevronDown, ChevronRight, Terminal
} from 'lucide-react';

function getStatusIcon(status) {
  switch (status) {
    case 'completed': return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
    case 'running': return <Loader2 className="w-4 h-4 text-primary-400 animate-spin" />;
    case 'failed': return <XCircle className="w-4 h-4 text-rose-400" />;
    default: return <Clock className="w-4 h-4 text-surface-200/40" />;
  }
}

function getAgentColor(type) {
  const colors = {
    prospect: 'text-primary-400',
    deal_risk: 'text-amber-400',
    churn: 'text-rose-400',
    competitive: 'text-cyan-400',
  };
  return colors[type] || 'text-surface-200/60';
}

function getAgentName(type) {
  const names = {
    prospect: 'Prospecting',
    deal_risk: 'Deal Intelligence',
    churn: 'Revenue Retention',
    competitive: 'Competitive Intel',
  };
  return names[type] || type;
}

export default function AgentLogs({ runs, expandedRun, onToggleExpand }) {
  if (!runs || runs.length === 0) {
    return (
      <div className="glass-card p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-surface-700/50">
            <Terminal className="w-5 h-5 text-surface-200/60" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Agent Execution Logs</h3>
            <p className="text-xs text-surface-200/50">No agent runs yet</p>
          </div>
        </div>
        <div className="py-8 text-center text-sm text-surface-200/30">
          Run an agent to see execution logs here
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2.5 rounded-xl bg-surface-700/50">
          <Terminal className="w-5 h-5 text-surface-200/60" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">Agent Execution Logs</h3>
          <p className="text-xs text-surface-200/50">{runs.length} recent runs</p>
        </div>
      </div>

      <div className="space-y-2 max-h-[400px] overflow-y-auto">
        {runs.map((run) => (
          <div key={run.id} className="rounded-xl border border-white/5 bg-surface-900/30 overflow-hidden">
            <button
              onClick={() => onToggleExpand(run.id)}
              className="w-full flex items-center gap-3 p-3 hover:bg-white/[0.02] transition-colors"
            >
              {getStatusIcon(run.status)}
              <span className={`text-xs font-semibold ${getAgentColor(run.agent_type)}`}>
                {getAgentName(run.agent_type)}
              </span>
              <span className="text-xs text-surface-200/30 flex-1 text-left truncate">
                {run.status === 'completed' && `${run.duration_ms}ms`}
                {run.status === 'failed' && run.error_message}
              </span>
              <span className="text-[10px] text-surface-200/20">
                #{run.id}
              </span>
              {expandedRun === run.id
                ? <ChevronDown className="w-3.5 h-3.5 text-surface-200/30" />
                : <ChevronRight className="w-3.5 h-3.5 text-surface-200/30" />
              }
            </button>

            {expandedRun === run.id && run.execution_log && (
              <div className="border-t border-white/5 p-3 bg-surface-900/50">
                <div className="space-y-1.5 font-mono">
                  {run.execution_log.map((log, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-[11px]">
                      <span className="text-surface-200/20 w-12 flex-shrink-0 text-right">
                        {log.elapsed_ms}ms
                      </span>
                      <span className="text-primary-400/60 w-20 flex-shrink-0 truncate">
                        [{log.step}]
                      </span>
                      <span className="text-surface-200/50 flex-1">
                        {log.details}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
