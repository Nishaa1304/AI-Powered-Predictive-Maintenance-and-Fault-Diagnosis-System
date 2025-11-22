"""
UEBA Agent - User and Entity Behavior Analytics for AI Security
Monitors and secures AI agent behavior
"""
import os
import sys
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent


class UEBAAgent(BaseAgent):
    """
    AI Agent for security monitoring and behavior analytics
    - Monitors all agent activities
    - Detects anomalous behavior
    - Prevents malicious actions
    - Generates security alerts
    """
    
    def __init__(self):
        super().__init__(
            agent_id="agent-ueba-001",
            agent_name="UEBASecurityAgent"
        )
        self.activity_log = []
        self.security_alerts = []
        self.baseline_behavior = defaultdict(lambda: {"call_count": 0, "error_rate": 0.0})
        self.logger.info("UEBA Security Agent created")
    
    async def initialize(self) -> bool:
        """Initialize UEBA agent"""
        self.logger.info("✅ UEBA Security Agent initialized")
        return True
    
    async def shutdown(self) -> bool:
        """Cleanup resources"""
        self.logger.info("Shutting down UEBA Security Agent")
        return True
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process security monitoring tasks"""
        self.update_activity()
        
        task_type = task.get("type")
        
        if task_type == "monitor_activity":
            return await self.monitor_activity(task)
        elif task_type == "detect_anomaly":
            return await self.detect_anomaly(task)
        elif task_type == "generate_security_report":
            return await self.generate_security_report(task)
        elif task_type == "block_action":
            return await self.block_action(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def monitor_activity(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor agent activity"""
        try:
            activity = {
                "activity_id": f"ACT{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
                "agent_id": task.get("agent_id"),
                "agent_name": task.get("agent_name"),
                "action": task.get("action"),
                "target": task.get("target"),
                "timestamp": datetime.now().isoformat(),
                "metadata": task.get("metadata", {})
            }
            
            # Log activity
            self.activity_log.append(activity)
            
            # Check for anomalies
            anomaly_result = await self._check_for_anomalies(activity)
            
            if anomaly_result["is_anomalous"]:
                alert = await self._create_security_alert(activity, anomaly_result)
                activity["security_alert"] = alert
            
            self.logger.info(f"✅ Activity monitored: {activity['agent_name']} - {activity['action']}")
            
            return {
                "status": "success",
                "activity": activity,
                "anomaly_detected": anomaly_result["is_anomalous"]
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def detect_anomaly(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalous behavior patterns"""
        try:
            agent_id = task.get("agent_id")
            time_window_hours = task.get("time_window_hours", 24)
            
            # Get recent activities
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            recent_activities = [
                a for a in self.activity_log
                if a["agent_id"] == agent_id and
                datetime.fromisoformat(a["timestamp"]) > cutoff_time
            ]
            
            # Analyze patterns
            anomalies = []
            
            # Check for excessive API calls
            if len(recent_activities) > 100:
                anomalies.append({
                    "type": "excessive_calls",
                    "severity": "medium",
                    "description": f"Agent made {len(recent_activities)} calls in {time_window_hours}h"
                })
            
            # Check for unusual times
            night_calls = [
                a for a in recent_activities
                if 0 <= datetime.fromisoformat(a["timestamp"]).hour < 6
            ]
            if len(night_calls) > 10:
                anomalies.append({
                    "type": "unusual_timing",
                    "severity": "low",
                    "description": f"{len(night_calls)} activities during night hours"
                })
            
            # Check for failed actions
            failed_actions = [a for a in recent_activities if a.get("metadata", {}).get("status") == "failed"]
            failure_rate = len(failed_actions) / len(recent_activities) if recent_activities else 0
            if failure_rate > 0.3:
                anomalies.append({
                    "type": "high_failure_rate",
                    "severity": "high",
                    "description": f"Failure rate: {failure_rate*100:.1f}%"
                })
            
            self.logger.info(f"✅ Detected {len(anomalies)} anomalies")
            
            return {
                "status": "success",
                "agent_id": agent_id,
                "anomalies": anomalies,
                "total_activities": len(recent_activities),
                "is_anomalous": len(anomalies) > 0
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def generate_security_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security report"""
        try:
            time_period_hours = task.get("time_period_hours", 24)
            cutoff_time = datetime.now() - timedelta(hours=time_period_hours)
            
            recent_activities = [
                a for a in self.activity_log
                if datetime.fromisoformat(a["timestamp"]) > cutoff_time
            ]
            
            recent_alerts = [
                a for a in self.security_alerts
                if datetime.fromisoformat(a["timestamp"]) > cutoff_time
            ]
            
            # Calculate metrics
            agent_activity = defaultdict(int)
            for activity in recent_activities:
                agent_activity[activity["agent_name"]] += 1
            
            report = {
                "report_id": f"SEC{datetime.now().strftime('%Y%m%d%H%M')}",
                "time_period_hours": time_period_hours,
                "total_activities": len(recent_activities),
                "total_alerts": len(recent_alerts),
                "critical_alerts": len([a for a in recent_alerts if a["severity"] == "critical"]),
                "high_alerts": len([a for a in recent_alerts if a["severity"] == "high"]),
                "agent_activity": dict(agent_activity),
                "security_status": "SECURE" if len(recent_alerts) == 0 else "MONITORING",
                "generated_at": datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Security report generated: {report['report_id']}")
            
            return {
                "status": "success",
                "report": report
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def block_action(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Block a potentially malicious action"""
        try:
            agent_id = task.get("agent_id")
            action = task.get("action")
            reason = task.get("reason")
            
            block_record = {
                "block_id": f"BLK{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "agent_id": agent_id,
                "action": action,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.warning(f"🚫 BLOCKED: {agent_id} - {action} - Reason: {reason}")
            
            return {
                "status": "success",
                "blocked": True,
                "block_record": block_record
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def _check_for_anomalies(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """Check if activity is anomalous"""
        # Simple rule-based detection (can be enhanced with ML)
        is_anomalous = False
        reasons = []
        severity = "low"
        
        # Check for sensitive actions
        sensitive_actions = ["delete_data", "modify_pricing", "access_credentials"]
        if activity["action"] in sensitive_actions:
            is_anomalous = True
            reasons.append(f"Sensitive action: {activity['action']}")
            severity = "high"
        
        # Check for unusual targets
        if activity.get("target", "").startswith("admin"):
            is_anomalous = True
            reasons.append("Attempted access to admin resources")
            severity = "critical"
        
        return {
            "is_anomalous": is_anomalous,
            "reasons": reasons,
            "severity": severity
        }
    
    async def _create_security_alert(
        self, 
        activity: Dict[str, Any], 
        anomaly: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a security alert"""
        alert = {
            "alert_id": f"ALT{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "severity": anomaly["severity"],
            "agent_id": activity["agent_id"],
            "agent_name": activity["agent_name"],
            "action": activity["action"],
            "reasons": anomaly["reasons"],
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.security_alerts.append(alert)
        
        self.logger.warning(f"🚨 SECURITY ALERT: {alert['severity']} - {alert['agent_name']}")
        
        return alert
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status"""
        active_alerts = [a for a in self.security_alerts if a["status"] == "active"]
        
        return {
            "status": "SECURE" if len(active_alerts) == 0 else "ALERT",
            "total_activities_monitored": len(self.activity_log),
            "active_alerts": len(active_alerts),
            "critical_alerts": len([a for a in active_alerts if a["severity"] == "critical"]),
            "last_check": datetime.now().isoformat()
        }


async def demo_ueba():
    """Demo the UEBA security agent"""
    print("\n" + "="*60)
    print("🔐 UEBA SECURITY AGENT DEMO")
    print("="*60 + "\n")
    
    agent = UEBAAgent()
    await agent.start()
    
    # Monitor normal activity
    normal_activity = {
        "type": "monitor_activity",
        "agent_id": "agent-customer-001",
        "agent_name": "CustomerEngagementAgent",
        "action": "initiate_voice_call",
        "target": "customer_phone",
        "metadata": {"status": "success"}
    }
    
    result = await agent.process_task(normal_activity)
    print(f"✅ Activity monitored: {'🚨 Anomaly' if result['anomaly_detected'] else '✓ Normal'}")
    
    # Monitor suspicious activity
    suspicious_activity = {
        "type": "monitor_activity",
        "agent_id": "agent-unknown-999",
        "agent_name": "UnknownAgent",
        "action": "access_credentials",
        "target": "admin_database",
        "metadata": {"status": "attempted"}
    }
    
    result = await agent.process_task(suspicious_activity)
    print(f"✅ Suspicious activity: {'🚨 ALERT TRIGGERED' if result['anomaly_detected'] else '✓ Normal'}")
    
    # Generate security report
    report_task = {"type": "generate_security_report", "time_period_hours": 1}
    report = await agent.process_task(report_task)
    print(f"\n📊 Security Report: {report['report']['security_status']}")
    print(f"   Total Activities: {report['report']['total_activities']}")
    print(f"   Total Alerts: {report['report']['total_alerts']}")
    
    # Show security status
    status = agent.get_security_status()
    print(f"\n🔐 Security Status: {status['status']}")
    
    await agent.stop()
    print("\n✅ DEMO COMPLETE\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(demo_ueba())
