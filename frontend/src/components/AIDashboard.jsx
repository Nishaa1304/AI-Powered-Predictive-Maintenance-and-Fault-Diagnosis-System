'use client';

import { useState, useEffect } from 'react';
import api from '../services/api';
import AgentReportModal from './AgentReportModal';

export default function AIDashboard() {
  const [vehicles, setVehicles] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [showVehicleSelector, setShowVehicleSelector] = useState(false);
  const [showReport, setShowReport] = useState(false);

  const agents = [
    {
      id: 'data_analysis',
      name: 'Data Analysis Agent',
      icon: '🔍',
      color: 'bg-blue-500',
      description: 'Analyzes vehicle telemetry and sensor data'
    },
    {
      id: 'diagnosis',
      name: 'Diagnosis Agent',
      icon: '🔧',
      color: 'bg-orange-500',
      description: 'Predicts failures and estimates repair costs'
    },
    {
      id: 'customer_engagement',
      name: 'Customer Engagement Agent',
      icon: '📞',
      color: 'bg-green-500',
      description: 'Generates personalized call scripts'
    },
    {
      id: 'scheduling',
      name: 'Scheduling Agent',
      icon: '📅',
      color: 'bg-purple-500',
      description: 'Manages service appointments'
    },
    {
      id: 'feedback',
      name: 'Feedback Agent',
      icon: '⭐',
      color: 'bg-yellow-500',
      description: 'Collects customer satisfaction data'
    },
    {
      id: 'manufacturing',
      name: 'Manufacturing Insights Agent',
      icon: '🏭',
      color: 'bg-indigo-500',
      description: 'Analyzes recurring defects for OEMs'
    }
  ];

  useEffect(() => {
    loadVehicles();
  }, []);

  const loadVehicles = async () => {
    try {
      const data = await api.getVehicles();
      if (data.vehicles) {
        setVehicles(Object.values(data.vehicles));
      }
    } catch (error) {
      console.error('Error loading vehicles:', error);
    }
  };

  const handleAgentClick = (agent) => {
    setSelectedAgent(agent);
    setShowVehicleSelector(true);
  };

  const handleVehicleSelect = (vehicle) => {
    setSelectedVehicle(vehicle);
    setShowVehicleSelector(false);
    setShowReport(true);
  };

  const closeReport = () => {
    setShowReport(false);
    setSelectedAgent(null);
    setSelectedVehicle(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-blue-900 mb-4">
            🚗 AI Predictive Maintenance System
          </h1>
          <p className="text-xl text-gray-700">
            Click any AI agent → Select vehicle → Get voice-enabled report
          </p>
        </div>

        {/* AI Agent Grid */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
            <span>🤖</span>
            AI Agent Activity Monitor
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div
                key={agent.id}
                onClick={() => handleAgentClick(agent)}
                className="group cursor-pointer bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-blue-500 hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className={`${agent.color} w-16 h-16 rounded-full flex items-center justify-center text-3xl group-hover:animate-bounce`}>
                    {agent.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-lg text-gray-800 group-hover:text-blue-600">
                      {agent.name}
                    </h3>
                    <span className="inline-block px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                      ● Active
                    </span>
                  </div>
                </div>
                <p className="text-gray-600 text-sm mb-4">
                  {agent.description}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-blue-600 font-semibold group-hover:underline">
                    Click to view report →
                  </span>
                  <span className="text-2xl">🎤</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Vehicle Fleet Overview */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            🚙 Your Vehicle Fleet
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {vehicles.map((vehicle) => (
              <div
                key={vehicle.vehicle_id}
                className="border-2 border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:shadow-md transition"
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-lg">{vehicle.model}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                    vehicle.type === 'EV' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {vehicle.type}
                  </span>
                </div>
                <p className="text-sm text-gray-600">Year: {vehicle.year}</p>
                <p className="text-sm text-gray-600">Owner: {vehicle.owner}</p>
                <p className="text-xs text-gray-500 mt-2">{vehicle.vehicle_id}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Vehicle Selector Modal */}
      {showVehicleSelector && selectedAgent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full p-8">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-4">
                <div className={`${selectedAgent.color} w-16 h-16 rounded-full flex items-center justify-center text-3xl`}>
                  {selectedAgent.icon}
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">
                    {selectedAgent.name}
                  </h2>
                  <p className="text-gray-600">Select a vehicle to analyze</p>
                </div>
              </div>
              <button
                onClick={() => setShowVehicleSelector(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {vehicles.map((vehicle) => (
                <div
                  key={vehicle.vehicle_id}
                  onClick={() => handleVehicleSelect(vehicle)}
                  className="border-2 border-gray-200 rounded-xl p-6 cursor-pointer hover:border-blue-500 hover:shadow-lg transition-all hover:scale-105"
                >
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="font-bold text-xl">{vehicle.model}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      vehicle.type === 'EV' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {vehicle.type}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-1">Year: {vehicle.year}</p>
                  <p className="text-gray-600 mb-1">Owner: {vehicle.owner}</p>
                  <p className="text-gray-500 text-sm">{vehicle.vehicle_id}</p>
                  <div className="mt-4 text-blue-600 font-semibold flex items-center gap-2">
                    View Report <span>→</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Agent Report Modal with Voice */}
      {showReport && selectedAgent && selectedVehicle && (
        <AgentReportModal
          agent={selectedAgent}
          vehicle={selectedVehicle}
          onClose={closeReport}
        />
      )}
    </div>
  );
}