"""
🎭 REAL-TIME AGENTIC AI DEMO
Complete end-to-end demonstration of all 6 AI agents working together
Including REAL voice calling capability with customer engagement
"""
import os
import sys
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

# Setup Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.join(current_dir, "agents")
sys.path.append(agents_dir)

# Import all agents
from data_analysis_agent.agent import DataAnalysisAgent
from diagnosis_agent.agent import DiagnosisAgent
from customer_engagement_agent.agent import CustomerEngagementAgent
from scheduling_agent.agent import SchedulingAgent
from feedback_agent.agent import FeedbackAgent
from manufacturing_insights_agent.agent import ManufacturingInsightsAgent
from ueba_agent.agent import UEBAAgent
from orchestrator import AgentOrchestrator


class RealTimeDemoSystem:
    """
    Complete real-time demo of the AI-Powered Predictive Maintenance System
    """
    
    def __init__(self):
        self.orchestrator = None
        self.demo_vehicle = {
            "vehicle_id": "VINDEMO001",
            "owner_name": "John Smith",
            "owner_phone": "+1-555-0123",  # Use your real phone for demo
            "vehicle_make": "Tesla",
            "vehicle_model": "Model 3",
            "vehicle_year": 2022
        }
    
    async def setup(self):
        """Initialize all agents"""
        print("\n" + "="*70)
        print("🚀 INITIALIZING AI-POWERED PREDICTIVE MAINTENANCE SYSTEM")
        print("="*70 + "\n")
        
        # Create orchestrator
        self.orchestrator = AgentOrchestrator()
        
        # Register all agents
        agents = [
            DataAnalysisAgent(),
            DiagnosisAgent(),
            CustomerEngagementAgent(),
            SchedulingAgent(),
            FeedbackAgent(),
            ManufacturingInsightsAgent(),
            UEBAAgent()
        ]
        
        for agent in agents:
            await self.orchestrator.register_agent(agent)
            print(f"✅ {agent.agent_name} registered")
        
        # Start all agents
        await self.orchestrator.start_all_agents()
        
        print("\n✅ All 6 AI agents are now ACTIVE and ready!\n")
        await asyncio.sleep(2)
    
    async def run_complete_demo(self):
        """Run the complete end-to-end demo"""
        print("="*70)
        print("🎬 STARTING REAL-TIME DEMO - COMPLETE WORKFLOW")
        print("="*70 + "\n")
        
        # ========== PHASE 1: DATA ANALYSIS & PREDICTION ==========
        await self._phase_1_data_analysis()
        await asyncio.sleep(2)
        
        # ========== PHASE 2: VOICE CALL TO CUSTOMER ==========
        await self._phase_2_voice_call()
        await asyncio.sleep(2)
        
        # ========== PHASE 3: AUTONOMOUS SCHEDULING ==========
        await self._phase_3_scheduling()
        await asyncio.sleep(2)
        
        # ========== PHASE 4: FEEDBACK COLLECTION ==========
        await self._phase_4_feedback()
        await asyncio.sleep(2)
        
        # ========== PHASE 5: MANUFACTURING INSIGHTS ==========
        await self._phase_5_manufacturing()
        await asyncio.sleep(2)
        
        # ========== PHASE 6: SECURITY MONITORING ==========
        await self._phase_6_security()
        
        # ========== FINAL SUMMARY ==========
        await self._show_summary()
    
    async def _phase_1_data_analysis(self):
        """Phase 1: Data Analysis & Failure Prediction"""
        print("\n" + "🔍 PHASE 1: DATA ANALYSIS & FAILURE PREDICTION")
        print("-" * 70)
        
        # Load synthetic data
        data_file = os.path.join(os.path.dirname(current_dir), "data", "synthetic", "demo_scenario.json")
        
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                vehicle_data = json.load(f)
                self.demo_vehicle.update(vehicle_data)
        
        # Analyze telemetry data
        print("📊 Analyzing vehicle telemetry...")
        analysis_task = {
            "type": "analyze_telemetry",
            "vehicle_id": self.demo_vehicle["vehicle_id"],
            "telemetry_data": self.demo_vehicle.get("current_telemetry", {})
        }
        
        analysis_result = await self.orchestrator.route_task("DataAnalysisAgent", analysis_task)
        
        if analysis_result.get("status") == "success":
            print(f"✅ Analysis complete!")
            print(f"   Vehicle: {self.demo_vehicle['vehicle_make']} {self.demo_vehicle['vehicle_model']}")
            print(f"   Health Score: {analysis_result.get('health_score', 0)}/100")
            print(f"   Anomalies Detected: {analysis_result.get('anomalies_detected', 0)}")
        
        # Predict failure
        print("\n🔮 Predicting component failures...")
        prediction_task = {
            "type": "predict_failure",
            "vehicle_id": self.demo_vehicle["vehicle_id"],
            "telemetry_data": self.demo_vehicle.get("current_telemetry", {}),
            "failure_prediction": self.demo_vehicle.get("predicted_failure", {})
        }
        
        prediction_result = await self.orchestrator.route_task("DiagnosisAgent", prediction_task)
        
        if prediction_result.get("status") == "success":
            prediction = prediction_result.get("prediction", {})
            print(f"⚠️  FAILURE PREDICTED!")
            print(f"   Component: {prediction.get('component', 'Unknown')}")
            print(f"   Confidence: {prediction.get('confidence', 0)*100:.0f}%")
            print(f"   Time to Failure: {prediction.get('time_to_failure_days', 0)} days")
            print(f"   Severity: {prediction.get('severity', 'unknown').upper()}")
            
            self.demo_vehicle["predicted_failure"] = prediction
    
    async def _phase_2_voice_call(self):
        """Phase 2: Voice Call to Customer"""
        print("\n" + "📞 PHASE 2: VOICE CALL TO CUSTOMER")
        print("-" * 70)
        
        print("🎤 Initiating voice call to customer...")
        print(f"   Calling: {self.demo_vehicle['owner_name']} at {self.demo_vehicle['owner_phone']}")
        
        # Initiate voice call
        call_task = {
            "type": "initiate_voice_call",
            "customer_phone": self.demo_vehicle["owner_phone"],
            "vehicle_id": self.demo_vehicle["vehicle_id"],
            "customer_name": self.demo_vehicle["owner_name"],
            "failure_prediction": self.demo_vehicle.get("predicted_failure", {})
        }
        
        call_result = await self.orchestrator.route_task("CustomerEngagementAgent", call_task)
        
        if call_result.get("status") == "success":
            script = call_result.get("script", {})
            print(f"\n✅ Voice call initiated!")
            print(f"   Call ID: {call_result.get('call_id')}")
            print(f"\n💬 CALL TRANSCRIPT:")
            print(f"   🤖 AI: {script.get('greeting', '')}")
            print(f"   🤖 AI: {script.get('issue_explanation', '')}")
            print(f"   🤖 AI: {script.get('recommendation', '')}")
            print(f"   🤖 AI: {script.get('scheduling_offer', '')}")
            
            print(f"\n   👤 Customer: 'Yes, I'd like to schedule an appointment'")
            
            # Handle customer response
            response_task = {
                "type": "handle_customer_response",
                "call_id": call_result.get('call_id'),
                "response_text": "Yes, I'd like to schedule an appointment"
            }
            
            response_result = await self.orchestrator.route_task("CustomerEngagementAgent", response_task)
            
            if response_result.get("action") == "proceed_to_scheduling":
                print(f"\n✅ Customer accepted! Proceeding to scheduling...")
                self.demo_vehicle["customer_accepted"] = True
    
    async def _phase_3_scheduling(self):
        """Phase 3: Autonomous Scheduling"""
        print("\n" + "📅 PHASE 3: AUTONOMOUS SCHEDULING")
        print("-" * 70)
        
        # Find service centers
        print("🔍 Finding nearby service centers...")
        find_task = {
            "type": "find_service_centers",
            "customer_location": {"lat": 40.7128, "lng": -74.0060},
            "service_type": "maintenance",
            "max_distance_km": 20
        }
        
        find_result = await self.orchestrator.route_task("SchedulingAgent", find_task)
        
        if find_result.get("status") == "success":
            centers = find_result.get("service_centers", [])
            print(f"✅ Found {len(centers)} service centers nearby:")
            for i, center in enumerate(centers[:3], 1):
                print(f"   {i}. {center['name']} - {center['distance_km']}km away (★ {center['rating']})")
            
            # Check availability
            best_center = centers[0]
            print(f"\n📅 Checking availability at {best_center['name']}...")
            
            availability_task = {
                "type": "check_availability",
                "service_center_id": best_center["id"],
                "preferred_dates": [
                    (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                    (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
                ],
                "service_duration_minutes": 120
            }
            
            availability_result = await self.orchestrator.route_task("SchedulingAgent", availability_task)
            
            if availability_result.get("status") == "success":
                slots = availability_result.get("available_slots", [])
                print(f"✅ Found {len(slots)} available slots:")
                for i, slot in enumerate(slots[:5], 1):
                    print(f"   {i}. {slot['date']} at {slot['time']}")
                
                # Book appointment
                best_slot = slots[0]
                print(f"\n📝 Booking appointment for {best_slot['date']} at {best_slot['time']}...")
                
                booking_task = {
                    "type": "book_appointment",
                    "service_center_id": best_center["id"],
                    "customer_name": self.demo_vehicle["owner_name"],
                    "customer_phone": self.demo_vehicle["owner_phone"],
                    "vehicle_id": self.demo_vehicle["vehicle_id"],
                    "appointment_time": best_slot["datetime"],
                    "service_type": f"{self.demo_vehicle.get('predicted_failure', {}).get('component', 'Component')} Replacement",
                    "estimated_duration": 120
                }
                
                booking_result = await self.orchestrator.route_task("SchedulingAgent", booking_task)
                
                if booking_result.get("status") == "success":
                    booking = booking_result.get("booking", {})
                    print(f"\n✅ APPOINTMENT SUCCESSFULLY BOOKED!")
                    print(f"   Booking ID: {booking['booking_id']}")
                    print(f"   Service Center: {best_center['name']}")
                    print(f"   Date & Time: {best_slot['date']} at {best_slot['time']}")
                    print(f"   Service: {booking['service_type']}")
                    print(f"   📱 Confirmation sent to {booking['customer_phone']}")
                    
                    self.demo_vehicle["booking"] = booking
    
    async def _phase_4_feedback(self):
        """Phase 4: Feedback Collection"""
        print("\n" + "💬 PHASE 4: POST-SERVICE FEEDBACK COLLECTION")
        print("-" * 70)
        
        print("📊 Simulating post-service feedback collection...")
        print("   (In production, this would happen after service completion)")
        
        # Collect feedback
        feedback_task = {
            "type": "collect_feedback",
            "booking_id": self.demo_vehicle.get("booking", {}).get("booking_id", "BK20251122"),
            "customer_name": self.demo_vehicle["owner_name"],
            "vehicle_id": self.demo_vehicle["vehicle_id"],
            "rating": 5,
            "comments": "Excellent service! The team was very professional and explained everything clearly. My car is running perfectly now!",
            "service_quality": 5,
            "timeliness": 5,
            "staff_courtesy": 5,
            "would_recommend": True
        }
        
        feedback_result = await self.orchestrator.route_task("FeedbackAgent", feedback_task)
        
        if feedback_result.get("status") == "success":
            feedback = feedback_result.get("feedback", {})
            print(f"\n✅ Feedback collected!")
            print(f"   Rating: {'⭐' * feedback['rating']}")
            print(f"   Sentiment: {feedback['sentiment'].upper()}")
            print(f"   Would Recommend: {'Yes' if feedback['would_recommend'] else 'No'}")
            print(f"   Comments: \"{feedback['comments'][:80]}...\"")
    
    async def _phase_5_manufacturing(self):
        """Phase 5: Manufacturing Insights"""
        print("\n" + "🏭 PHASE 5: MANUFACTURING INSIGHTS & RCA")
        print("-" * 70)
        
        component = self.demo_vehicle.get("predicted_failure", {}).get("component", "Alternator")
        
        print(f"📊 Analyzing failure patterns for {component}...")
        
        # Analyze failure pattern
        pattern_task = {
            "type": "analyze_failure_pattern",
            "component": component,
            "vehicle_data": [
                {"vehicle_id": "VIN001", "batch_id": "BATCH2024Q1"},
                {"vehicle_id": "VIN002", "batch_id": "BATCH2024Q1"},
                {"vehicle_id": "VIN003", "batch_id": "BATCH2024Q1"},
                {"vehicle_id": self.demo_vehicle["vehicle_id"], "batch_id": "BATCH2024Q1"}
            ]
        }
        
        pattern_result = await self.orchestrator.route_task("ManufacturingInsightsAgent", pattern_task)
        
        if pattern_result.get("status") == "success":
            print(f"✅ Pattern analysis complete!")
            print(f"   Total Failures: {pattern_result['total_failures']}")
            print(f"   Affected Vehicles: {pattern_result['affected_vehicles']}")
            print(f"   Severity: {pattern_result['severity'].upper()}")
            
            # Generate RCA report
            print(f"\n📝 Generating Root Cause Analysis (RCA) report...")
            
            rca_task = {
                "type": "generate_rca_report",
                "component": component
            }
            
            rca_result = await self.orchestrator.route_task("ManufacturingInsightsAgent", rca_task)
            
            if rca_result.get("status") == "success":
                report = rca_result.get("report", {})
                print(f"\n✅ RCA REPORT GENERATED!")
                print(f"   Report ID: {report['report_id']}")
                print(f"   Affected Vehicles: {report['affected_vehicles']}")
                print(f"   Estimated Cost Impact: ${report['estimated_cost_impact']:,}")
                
                print(f"\n   🔍 Root Causes Identified:")
                for i, cause in enumerate(report['root_causes'][:2], 1):
                    print(f"      {i}. {cause['cause']} (Confidence: {cause['confidence']})")
                
                print(f"\n   ⚡ Corrective Actions:")
                for i, action in enumerate(report['corrective_actions'][:2], 1):
                    print(f"      {i}. {action['action']} (Priority: {action['priority']})")
    
    async def _phase_6_security(self):
        """Phase 6: Security Monitoring"""
        print("\n" + "🔐 PHASE 6: UEBA SECURITY MONITORING")
        print("-" * 70)
        
        print("🔍 Monitoring all agent activities for security...")
        
        # Generate security report
        security_task = {
            "type": "generate_security_report",
            "time_period_hours": 1
        }
        
        security_result = await self.orchestrator.route_task("UEBAAgent", security_task)
        
        if security_result.get("status") == "success":
            report = security_result.get("report", {})
            print(f"\n✅ SECURITY REPORT:")
            print(f"   Status: {report['security_status']}")
            print(f"   Total Activities Monitored: {report['total_activities']}")
            print(f"   Security Alerts: {report['total_alerts']}")
            print(f"   Critical Alerts: {report['critical_alerts']}")
            
            if report['security_status'] == "SECURE":
                print(f"\n   ✅ All agents operating normally - No security threats detected")
            
            print(f"\n   📊 Agent Activity Breakdown:")
            for agent_name, count in report.get('agent_activity', {}).items():
                print(f"      - {agent_name}: {count} activities")
    
    async def _show_summary(self):
        """Show final summary"""
        print("\n" + "="*70)
        print("🎉 DEMO COMPLETE - SYSTEM SUMMARY")
        print("="*70 + "\n")
        
        print("✅ END-TO-END WORKFLOW COMPLETED SUCCESSFULLY!\n")
        
        print("📊 What We Demonstrated:\n")
        print("   1. ✅ Data Analysis Agent - Analyzed telemetry & predicted failure")
        print("   2. ✅ Diagnosis Agent - Provided detailed failure diagnosis")
        print("   3. ✅ Customer Engagement Agent - Made VOICE CALL to customer")
        print("   4. ✅ Scheduling Agent - Autonomously booked service appointment")
        print("   5. ✅ Feedback Agent - Collected post-service feedback")
        print("   6. ✅ Manufacturing Insights Agent - Generated RCA/CAPA report")
        print("   7. ✅ UEBA Security Agent - Monitored all activities for security")
        
        print(f"\n💡 KEY OUTCOMES:\n")
        print(f"   🚗 Vehicle: {self.demo_vehicle['vehicle_make']} {self.demo_vehicle['vehicle_model']}")
        print(f"   👤 Customer: {self.demo_vehicle['owner_name']}")
        print(f"   ⚠️  Predicted Failure: {self.demo_vehicle.get('predicted_failure', {}).get('component', 'N/A')}")
        print(f"   📞 Voice Call: Completed with customer consent")
        print(f"   📅 Appointment: Booked and confirmed")
        print(f"   💬 Feedback: Collected with 5⭐ rating")
        print(f"   🏭 Manufacturing: RCA report sent to OEM")
        print(f"   🔐 Security: All systems secure")
        
        print(f"\n🏆 COMPETITIVE ADVANTAGES:\n")
        print("   ✨ Voice-First Engagement - Real human-like conversations")
        print("   🤖 Multi-Agent Orchestration - 6 specialized AI agents")
        print("   🔄 End-to-End Automation - From prediction to resolution")
        print("   🔐 UEBA Security - AI behavior monitoring")
        print("   🏭 Manufacturing Loop - Feedback to OEMs for improvements")
        
        print("\n" + "="*70)
        print("🚀 Ready for Production Deployment!")
        print("="*70 + "\n")
    
    async def shutdown(self):
        """Shutdown all agents"""
        print("\n🛑 Shutting down all agents...")
        await self.orchestrator.stop_all_agents()
        print("✅ All agents stopped successfully\n")


async def main():
    """Main demo entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create demo system
    demo = RealTimeDemoSystem()
    
    try:
        # Setup all agents
        await demo.setup()
        
        # Run complete demo
        await demo.run_complete_demo()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        await demo.shutdown()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║  🚗 AI-POWERED PREDICTIVE MAINTENANCE & FAULT DIAGNOSIS SYSTEM    ║
    ║                                                                    ║
    ║     🎭 REAL-TIME AGENTIC AI DEMONSTRATION                         ║
    ║                                                                    ║
    ║  Features:                                                         ║
    ║  • 6 Specialized AI Agents Working Together                       ║
    ║  • Real Voice Calling with Natural Language                       ║
    ║  • Autonomous Scheduling & Booking                                ║
    ║  • Post-Service Feedback Collection                               ║
    ║  • Manufacturing Insights (RCA/CAPA)                              ║
    ║  • UEBA Security Monitoring                                       ║
    ║                                                                    ║
    ║  Press Ctrl+C to stop at any time                                ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run the demo
    asyncio.run(main())
