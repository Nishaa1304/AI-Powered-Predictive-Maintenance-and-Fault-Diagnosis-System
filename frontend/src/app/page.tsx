'use client';

import { useState, useEffect } from 'react';
import AgentReportModal from '../components/AgentReportModal';

interface Vehicle {
  vehicle_id: string;
  model: string;
  year: number;
  owner: string;
  type: string;
  phone: string;
}

interface Agent {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
}

export default function Home() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);
  const [showVehicleSelector, setShowVehicleSelector] = useState(false);
  const [showReport, setShowReport] = useState(false);

  const agents: Agent[] = [
    {
      id: 'data_analysis',
      name: 'Data Analysis Agent',
      icon: '🔍',
      color: 'bg-blue-500',
      description: 'Analyzes vehicle telemetry and sensor data in real-time'
    },
    {
      id: 'diagnosis',
      name: 'Diagnosis Agent',
      icon: '🔧',
      color: 'bg-orange-500',
      description: 'Predicts component failures and estimates repair costs'
    },
    {
      id: 'customer_engagement',
      name: 'Customer Engagement Agent',
      icon: '📞',
      color: 'bg-green-500',
      description: 'Generates personalized customer call scripts with AI'
    },
    {
      id: 'scheduling',
      name: 'Scheduling Agent',
      icon: '📅',
      color: 'bg-purple-500',
      description: 'Manages service appointments and workshop allocation'
    },
    {
      id: 'feedback',
      name: 'Feedback Agent',
      icon: '⭐',
      color: 'bg-yellow-500',
      description: 'Collects and analyzes customer satisfaction data'
    },
    {
      id: 'manufacturing',
      name: 'Manufacturing Insights',
      icon: '🏭',
      color: 'bg-indigo-500',
      description: 'Identifies recurring defects and sends insights to OEMs'
    }
  ];

  useEffect(() => {
    // Mock vehicle data
    setVehicles([
      {
        vehicle_id: 'VEH001',
        model: '2020 Maruti Swift',
        year: 2020,
        owner: 'Mr. Rajesh Sharma',
        type: 'ICE',
        phone: '+91-9876543210'
      },
      {
        vehicle_id: 'VEH002',
        model: '2022 Tata Nexon EV',
        year: 2022,
        owner: 'Ms. Priya Patel',
        type: 'EV',
        phone: '+91-9876543211'
      },
      {
        vehicle_id: 'VEH003',
        model: '2021 Hyundai Creta',
        year: 2021,
        owner: 'Mr. Amit Kumar',
        type: 'ICE',
        phone: '+91-9876543212'
      }
    ]);
  }, []);

  const handleAgentClick = (agent: Agent) => {
    setSelectedAgent(agent);
    setShowVehicleSelector(true);
  };

  const handleVehicleSelect = (vehicle: Vehicle) => {
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
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-8">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            🚗 AI Predictive Maintenance System
          </h1>
          <p className="text-2xl text-gray-700 mb-2">
            Click any AI agent → Select vehicle → Get voice-enabled report
          </p>
          <p className="text-lg text-gray-600">
            🎤 Each agent has voice interaction capabilities
          </p>
        </div>

        {/* AI Agent Grid - CLICKABLE CARDS */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 mb-8">
          <h2 className="text-4xl font-bold text-gray-800 mb-8 flex items-center gap-3">
            <span className="text-5xl">🤖</span>
            AI Agent Activity Monitor
            <span className="ml-auto text-sm font-normal bg-green-100 text-green-800 px-4 py-2 rounded-full">
              ● 6 Agents Active
            </span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div
                key={agent.id}
                onClick={() => handleAgentClick(agent)}
                className="group cursor-pointer bg-gradient-to-br from-white to-gray-50 border-2 border-gray-200 rounded-2xl p-6 hover:border-blue-500 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 hover:-translate-y-1"
              >
                <div className="flex items-start gap-4 mb-4">
                  <div className={`${agent.color} w-16 h-16 rounded-2xl flex items-center justify-center text-3xl group-hover:animate-bounce shadow-lg`}>
                    {agent.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-xl text-gray-800 group-hover:text-blue-600 mb-2">
                      {agent.name}
                    </h3>
                    <span className="inline-block px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full animate-pulse">
                      ● ACTIVE
                    </span>
                  </div>
                </div>
                
                <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                  {agent.description}
                </p>
                
                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <span className="text-blue-600 font-bold group-hover:underline flex items-center gap-2">
                    Click to view report
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </span>
                  <span className="text-3xl">🎤</span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 p-6 bg-blue-50 rounded-2xl border-2 border-blue-200">
            <p className="text-center text-gray-700">
              <strong className="text-blue-600">💡 Pro Tip:</strong> After viewing any report, use the 🎤 voice button to ask questions like:
              <span className="block mt-2 text-sm text-gray-600">
                "Give me a summary" • "What are the problems?" • "How much will it cost?" • "Is it urgent?"
              </span>
            </p>
          </div>
        </div>

        {/* Vehicle Fleet Overview */}
        <div className="bg-white rounded-3xl shadow-2xl p-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
            <span>🚙</span>
            Your Vehicle Fleet
            <span className="ml-auto text-sm font-normal bg-blue-100 text-blue-800 px-4 py-2 rounded-full">
              {vehicles.length} Vehicles
            </span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {vehicles.map((vehicle) => (
              <div
                key={vehicle.vehicle_id}
                className="border-2 border-gray-200 rounded-2xl p-6 hover:border-blue-300 hover:shadow-xl transition-all"
              >
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-bold text-xl text-gray-800">{vehicle.model}</h3>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    vehicle.type === 'EV' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {vehicle.type}
                  </span>
                </div>
                <div className="space-y-1 text-gray-600">
                  <p className="text-sm">📅 Year: {vehicle.year}</p>
                  <p className="text-sm">👤 Owner: {vehicle.owner}</p>
                  <p className="text-xs text-gray-500 mt-3 font-mono">{vehicle.vehicle_id}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Vehicle Selector Modal */}
      {showVehicleSelector && selectedAgent && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-3xl shadow-2xl max-w-4xl w-full p-8 transform animate-scale-in">
            <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-4">
                <div className={`${selectedAgent.color} w-20 h-20 rounded-2xl flex items-center justify-center text-4xl shadow-lg`}>
                  {selectedAgent.icon}
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-gray-800">
                    {selectedAgent.name}
                  </h2>
                  <p className="text-gray-600 text-lg">Select a vehicle to analyze</p>
                </div>
              </div>
              <button
                onClick={() => setShowVehicleSelector(false)}
                className="text-gray-400 hover:text-gray-600 text-3xl font-bold hover:rotate-90 transition-transform"
              >
                ×
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {vehicles.map((vehicle) => (
                <div
                  key={vehicle.vehicle_id}
                  onClick={() => handleVehicleSelect(vehicle)}
                  className="border-2 border-gray-200 rounded-2xl p-6 cursor-pointer hover:border-blue-500 hover:shadow-2xl transition-all transform hover:scale-105"
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-bold text-2xl text-gray-800">{vehicle.model}</h3>
                    <span className={`px-4 py-2 rounded-full text-sm font-bold ${
                      vehicle.type === 'EV' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {vehicle.type}
                    </span>
                  </div>
                  <div className="space-y-2 mb-4">
                    <p className="text-gray-600">📅 Year: {vehicle.year}</p>
                    <p className="text-gray-600">👤 Owner: {vehicle.owner}</p>
                    <p className="text-gray-500 text-sm font-mono">{vehicle.vehicle_id}</p>
                  </div>
                  <div className="pt-4 border-t border-gray-200 text-blue-600 font-bold flex items-center gap-2">
                    View {selectedAgent.name} Report
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
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

      <style jsx>{`
        @keyframes scale-in {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }
        .animate-scale-in {
          animation: scale-in 0.3s ease-out;
        }
      `}</style>
    </main>
  );
}