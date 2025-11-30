'use client';

import { useState } from 'react';

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
}

export default function Sidebar({ activeView, onViewChange }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const menuItems = [
    {
      id: 'dashboard',
      icon: '📊',
      label: 'Dashboard',
      color: 'hover:bg-blue-500/20 hover:border-blue-500/50'
    },
    {
      id: 'vehicles',
      icon: '🚗',
      label: 'Vehicles',
      color: 'hover:bg-cyan-500/20 hover:border-cyan-500/50'
    },
    {
      id: 'scheduling',
      icon: '📅',
      label: 'Scheduling',
      color: 'hover:bg-purple-500/20 hover:border-purple-500/50'
    },
    {
      id: 'voice_agent',
      icon: '🎙️',
      label: 'Voice Agent',
      color: 'hover:bg-green-500/20 hover:border-green-500/50'
    },
    {
      id: 'feedback',
      icon: '⭐',
      label: 'Feedback',
      color: 'hover:bg-yellow-500/20 hover:border-yellow-500/50'
    },
    {
      id: 'manufacturing',
      icon: '🏭',
      label: 'Manufacturing',
      color: 'hover:bg-indigo-500/20 hover:border-indigo-500/50'
    },
    {
      id: 'ueba',
      icon: '🔒',
      label: 'UEBA Security',
      color: 'hover:bg-red-500/20 hover:border-red-500/50'
    },
    {
      id: 'analytics',
      icon: '📈',
      label: 'Analytics',
      color: 'hover:bg-orange-500/20 hover:border-orange-500/50'
    }
  ];

  return (
    <div
      className={`fixed left-0 top-0 h-screen bg-gray-900/95 backdrop-blur-sm border-r border-gray-700 transition-all duration-300 z-40 overflow-y-auto ${
        isCollapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Header */}
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-xl shadow-lg">
              🚗
            </div>
            {!isCollapsed && (
              <div>
                <h2 className="font-bold text-white text-sm">AI Vehicle</h2>
                <p className="text-xs text-gray-400">Predictive Maintenance</p>
              </div>
            )}
          </div>
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="text-gray-400 hover:text-white transition-colors"
          >
            {isCollapsed ? '→' : '←'}
          </button>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="p-4 space-y-2 pb-24">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onViewChange(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 border border-transparent ${
              activeView === item.id
                ? 'bg-blue-500/20 border-blue-500/50 shadow-lg shadow-blue-500/20'
                : `bg-gray-800/50 ${item.color}`
            }`}
          >
            <span className="text-2xl">{item.icon}</span>
            {!isCollapsed && (
              <div className="flex-1 text-left">
                <span
                  className={`font-semibold text-sm ${
                    activeView === item.id ? 'text-blue-400' : 'text-gray-300'
                  }`}
                >
                  {item.label}
                </span>
              </div>
            )}
            {activeView === item.id && (
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            )}
          </button>
        ))}
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700 bg-gray-900">
        {!isCollapsed && (
          <div className="bg-gray-800/50 rounded-xl p-3">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-green-400 font-semibold">System Online</span>
            </div>
            <p className="text-xs text-gray-500">v2.0.1 | All systems operational</p>
          </div>
        )}
      </div>
    </div>
  );
}
