import React from 'react';
import { Bell, CheckCircle2, XCircle, Loader2, X } from 'lucide-react';

export default function NotificationPanel({ notifications, onClear, isConnected }) {
  return (
    <div className="glass-card p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-surface-200/60" />
          <span className="text-sm font-semibold text-white">Notifications</span>
          <div className={`pulse-dot ${isConnected ? '' : 'opacity-30'}`} />
        </div>
        <span className="text-[10px] text-surface-200/30">
          {isConnected ? 'Live' : 'Disconnected'}
        </span>
      </div>

      <div className="space-y-2 max-h-[250px] overflow-y-auto">
        {notifications.length === 0 ? (
          <p className="text-xs text-surface-200/30 text-center py-4">
            No notifications yet
          </p>
        ) : (
          notifications.map((notif) => (
            <div
              key={notif.id}
              className="flex items-start gap-2 p-2.5 rounded-lg bg-surface-900/30 border border-white/3 animate-slide-in"
            >
              {notif.status === 'completed' ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              ) : notif.status === 'failed' ? (
                <XCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
              ) : (
                <Loader2 className="w-4 h-4 text-primary-400 animate-spin flex-shrink-0 mt-0.5" />
              )}
              <div className="flex-1 min-w-0">
                <p className="text-xs text-white truncate">{notif.message}</p>
                <p className="text-[10px] text-surface-200/30 mt-0.5">
                  {new Date(notif.timestamp).toLocaleTimeString()}
                </p>
              </div>
              <button
                onClick={() => onClear(notif.id)}
                className="text-surface-200/20 hover:text-surface-200/60 transition-colors"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
