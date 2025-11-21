'use client'

import { Activity, AlertTriangle, Car, TrendingUp } from 'lucide-react'
import VehicleCard from '@/components/dashboard/VehicleCard'
import LiveAlerts from '@/components/dashboard/LiveAlerts'
import AgentStatus from '@/components/dashboard/AgentStatus'
import UEBAIndicator from '@/components/dashboard/UEBAIndicator'

export default function Home() {
  // Mock data - replace with API calls
  const kpis = {
    totalVehicles: 150,
    predictedFailures: 12,
    criticalAlerts: 3,
    activeAgents: 6
  }

  const vehicles = [
    {
      id: 'VIN12345',
      model: 'Tesla Model 3',
      status: 'critical',
      lastAlert: '5 mins ago',
      health: 45,
      issue: 'Battery failure predicted'
    },
    {
      id: 'VIN23456',
      model: 'BMW X5',
      status: 'warning',
      lastAlert: '1 hour ago',
      health: 72,
      issue: 'Brake pad wear detected'
    },
    {
      id: 'VIN34567',
      model: 'Mercedes E-Class',
      status: 'healthy',
      lastAlert: 'None',
      health: 95,
      issue: null
    },
    {
      id: 'VIN45678',
      model: 'Audi A4',
      status: 'warning',
      lastAlert: '2 hours ago',
      health: 68,
      issue: 'Oil pressure low'
    },
    {
      id: 'VIN56789',
      model: 'Toyota Camry',
      status: 'healthy',
      lastAlert: 'None',
      health: 92,
      issue: null
    },
    {
      id: 'VIN67890',
      model: 'Honda Accord',
      status: 'critical',
      lastAlert: '10 mins ago',
      health: 38,
      issue: 'Engine overheating'
    },
  ]

  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Vehicle Health Overview</h1>
        <p className="text-gray-600 mt-1">Real-time monitoring and predictive maintenance</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Total Vehicles</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{kpis.totalVehicles}</p>
            </div>
            <div className="bg-primary-100 p-3 rounded-lg">
              <Car className="w-6 h-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Predicted Failures</p>
              <p className="text-3xl font-bold text-warning-600 mt-2">{kpis.predictedFailures}</p>
            </div>
            <div className="bg-warning-100 p-3 rounded-lg">
              <TrendingUp className="w-6 h-6 text-warning-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Critical Alerts</p>
              <p className="text-3xl font-bold text-danger-600 mt-2">{kpis.criticalAlerts}</p>
            </div>
            <div className="bg-danger-100 p-3 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-danger-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Active AI Agents</p>
              <p className="text-3xl font-bold text-success-600 mt-2">{kpis.activeAgents}</p>
            </div>
            <div className="bg-success-100 p-3 rounded-lg">
              <Activity className="w-6 h-6 text-success-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Vehicle Cards - Takes 2/3 width */}
        <div className="lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Fleet Status</h2>
            <select className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option>All Vehicles</option>
              <option>Critical Only</option>
              <option>Warnings</option>
              <option>Healthy</option>
            </select>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {vehicles.map((vehicle) => (
              <VehicleCard key={vehicle.id} vehicle={vehicle} />
            ))}
          </div>
        </div>

        {/* Right Sidebar - Takes 1/3 width */}
        <div className="space-y-6">
          {/* UEBA Security Indicator */}
          <UEBAIndicator />
          
          {/* Live Alerts Panel */}
          <LiveAlerts />
        </div>
      </div>

      {/* AI Agent Status - Full Width */}
      <AgentStatus />
    </div>
  )
}
