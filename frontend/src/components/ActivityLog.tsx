'use client';

import { ActivityLogEntry } from './AlertSystem';
import { formatTimestamp } from '../utils/mockAlertGenerator';

interface ActivityLogProps {
  logs: ActivityLogEntry[];
}

export default function ActivityLog({ logs }: ActivityLogProps) {
  const typeIcons = {
    data: '📊',
    diagnosis: '🔧',
    customer: '💬',
    appointment: '📅',
    security: '🔒'
  };

  const typeColors = {
    data: 'text-blue-400',
    diagnosis: 'text-orange-400',
    customer: 'text-green-400',
    appointment: 'text-purple-400',
    security: 'text-red-400'
  };

  return (
    <div className="bg-gray-900/80 border border-gray-700 rounded-xl p-4 h-full">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <h3 className="text-sm font-bold text-white">Live Activity Log</h3>
      </div>
      <div className="space-y-1 overflow-y-auto custom-scrollbar font-mono text-xs" style={{ maxHeight: '600px' }}>
        {logs.map((log, index) => (
          <div
            key={log.id}
            className="log-fade-in flex items-start gap-2 text-gray-400 hover:text-gray-300 transition-colors"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            <span className="text-gray-600">[{formatTimestamp(log.timestamp)}]</span>
            <span className="text-lg">{typeIcons[log.type]}</span>
            <span className={typeColors[log.type]}>{log.action}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
