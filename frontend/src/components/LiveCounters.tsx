'use client';

interface LiveCountersProps {
  counters: {
    vehiclesMonitored: number;
    activeAlerts: number;
    callsInProgress: number;
    todaysPredictions: number;
  };
}

export default function LiveCounters({ counters }: LiveCountersProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 rounded-xl p-4 hover:shadow-lg hover:shadow-blue-500/20 transition-all duration-300">
        <div className="text-gray-400 text-xs mb-1">Vehicles Monitored</div>
        <div className="text-3xl font-bold text-white counter-animate">{counters.vehiclesMonitored}</div>
        <div className="flex items-center gap-1 mt-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-green-400">Live</span>
        </div>
      </div>

      <div className="bg-gradient-to-br from-red-500/20 to-orange-500/20 border border-red-500/30 rounded-xl p-4 hover:shadow-lg hover:shadow-red-500/20 transition-all duration-300">
        <div className="text-gray-400 text-xs mb-1">Active Alerts</div>
        <div className="text-3xl font-bold text-white counter-animate">{counters.activeAlerts}</div>
        <div className="flex items-center gap-1 mt-2">
          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-red-400">Monitoring</span>
        </div>
      </div>

      <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-xl p-4 hover:shadow-lg hover:shadow-purple-500/20 transition-all duration-300">
        <div className="text-gray-400 text-xs mb-1">Calls In Progress</div>
        <div className="text-3xl font-bold text-white counter-animate">{counters.callsInProgress}</div>
        <div className="flex items-center gap-1 mt-2">
          <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-purple-400">Active</span>
        </div>
      </div>

      <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-500/30 rounded-xl p-4 hover:shadow-lg hover:shadow-green-500/20 transition-all duration-300">
        <div className="text-gray-400 text-xs mb-1">Today's Predictions</div>
        <div className="text-3xl font-bold text-white counter-animate">{counters.todaysPredictions}</div>
        <div className="flex items-center gap-1 mt-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-green-400">Real-time</span>
        </div>
      </div>
    </div>
  );
}
