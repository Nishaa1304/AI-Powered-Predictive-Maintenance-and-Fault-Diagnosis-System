"""
Manufacturing Insights Agent - RCA/CAPA for OEMs
Generates Root Cause Analysis and Corrective/Preventive Actions
"""
import os
import sys
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent


class ManufacturingInsightsAgent(BaseAgent):
    """
    AI Agent for manufacturing insights and quality improvements
    - Root Cause Analysis (RCA)
    - Corrective and Preventive Actions (CAPA)
    - Batch-level defect detection
    - Quality trend analysis
    """
    
    def __init__(self):
        super().__init__(
            agent_id="agent-manufacturing-001",
            agent_name="ManufacturingInsightsAgent"
        )
        self.failure_patterns = defaultdict(list)
        self.reports = []
        self.logger.info("Manufacturing Insights Agent created")
    
    async def initialize(self) -> bool:
        """Initialize manufacturing insights agent"""
        self.logger.info("✅ Manufacturing Insights Agent initialized")
        return True
    
    async def shutdown(self) -> bool:
        """Cleanup resources"""
        self.logger.info("Shutting down Manufacturing Insights Agent")
        return True
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process manufacturing insights tasks"""
        self.update_activity()
        
        task_type = task.get("type")
        
        if task_type == "analyze_failure_pattern":
            return await self.analyze_failure_pattern(task)
        elif task_type == "generate_rca_report":
            return await self.generate_rca_report(task)
        elif task_type == "detect_batch_issues":
            return await self.detect_batch_issues(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def analyze_failure_pattern(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze failure patterns across fleet"""
        try:
            component = task.get("component")
            vehicle_data = task.get("vehicle_data", [])
            
            # Track failure pattern
            self.failure_patterns[component].extend(vehicle_data)
            
            # Analyze pattern
            total_failures = len(self.failure_patterns[component])
            affected_vehicles = len(set(v["vehicle_id"] for v in self.failure_patterns[component]))
            
            # Check for batch issues
            batch_analysis = self._analyze_batches(component)
            
            self.logger.info(f"✅ Analyzed {total_failures} failures of {component}")
            
            return {
                "status": "success",
                "component": component,
                "total_failures": total_failures,
                "affected_vehicles": affected_vehicles,
                "batch_analysis": batch_analysis,
                "severity": "high" if total_failures > 10 else "medium"
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def generate_rca_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Root Cause Analysis report"""
        try:
            component = task.get("component")
            failures = self.failure_patterns.get(component, [])
            
            if not failures:
                return {"status": "error", "message": "No failure data available"}
            
            # Perform RCA
            root_causes = self._identify_root_causes(component, failures)
            corrective_actions = self._generate_corrective_actions(component, root_causes)
            preventive_actions = self._generate_preventive_actions(component)
            
            report = {
                "report_id": f"RCA{datetime.now().strftime('%Y%m%d%H%M')}",
                "component": component,
                "total_incidents": len(failures),
                "affected_vehicles": len(set(v["vehicle_id"] for v in failures)),
                "root_causes": root_causes,
                "corrective_actions": corrective_actions,
                "preventive_actions": preventive_actions,
                "estimated_cost_impact": len(failures) * 1500,  # $1500 per incident
                "generated_at": datetime.now().isoformat()
            }
            
            self.reports.append(report)
            
            self.logger.info(f"✅ RCA report generated: {report['report_id']}")
            
            return {
                "status": "success",
                "report": report
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def detect_batch_issues(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Detect batch-level manufacturing defects"""
        try:
            component = task.get("component")
            batch_threshold = task.get("batch_threshold", 0.15)  # 15% failure rate
            
            batch_analysis = self._analyze_batches(component)
            
            # Identify problematic batches
            problematic_batches = [
                batch for batch in batch_analysis
                if batch["failure_rate"] > batch_threshold
            ]
            
            self.logger.info(f"✅ Found {len(problematic_batches)} problematic batches")
            
            return {
                "status": "success",
                "component": component,
                "problematic_batches": problematic_batches,
                "total_batches_analyzed": len(batch_analysis),
                "recommendation": "Immediate quality review required" if problematic_batches else "No action needed"
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    def _analyze_batches(self, component: str) -> List[Dict[str, Any]]:
        """Analyze batches for defect patterns"""
        failures = self.failure_patterns.get(component, [])
        
        batch_data = defaultdict(lambda: {"total": 0, "failures": 0})
        
        for failure in failures:
            batch_id = failure.get("batch_id", "UNKNOWN")
            batch_data[batch_id]["failures"] += 1
        
        # Add total vehicles per batch (simulated)
        for batch_id in batch_data.keys():
            batch_data[batch_id]["total"] = 100  # Assume 100 vehicles per batch
        
        # Calculate failure rates
        result = []
        for batch_id, data in batch_data.items():
            failure_rate = data["failures"] / data["total"] if data["total"] > 0 else 0
            result.append({
                "batch_id": batch_id,
                "total_vehicles": data["total"],
                "failures": data["failures"],
                "failure_rate": round(failure_rate, 3)
            })
        
        return sorted(result, key=lambda x: x["failure_rate"], reverse=True)
    
    def _identify_root_causes(self, component: str, failures: List[Dict]) -> List[Dict[str, str]]:
        """Identify root causes"""
        return [
            {
                "cause": f"Material defect in {component} manufacturing",
                "evidence": f"High failure rate in specific production batches",
                "confidence": "high"
            },
            {
                "cause": "Inadequate quality control during assembly",
                "evidence": "Similar failure patterns across multiple batches",
                "confidence": "medium"
            },
            {
                "cause": "Design vulnerability under high-stress conditions",
                "evidence": "Failures occur at similar mileage/usage patterns",
                "confidence": "medium"
            }
        ]
    
    def _generate_corrective_actions(self, component: str, root_causes: List[Dict]) -> List[Dict[str, Any]]:
        """Generate corrective actions"""
        return [
            {
                "action": f"Immediate recall of affected {component} batches",
                "priority": "critical",
                "timeline": "Immediate",
                "responsible_team": "Quality Assurance"
            },
            {
                "action": "Enhanced inspection protocols for production line",
                "priority": "high",
                "timeline": "1 week",
                "responsible_team": "Manufacturing"
            },
            {
                "action": "Supplier audit and material specification review",
                "priority": "high",
                "timeline": "2 weeks",
                "responsible_team": "Supply Chain"
            }
        ]
    
    def _generate_preventive_actions(self, component: str) -> List[Dict[str, Any]]:
        """Generate preventive actions"""
        return [
            {
                "action": f"Redesign {component} with improved materials",
                "timeline": "3 months",
                "expected_impact": "80% reduction in failures"
            },
            {
                "action": "Implement AI-powered quality inspection",
                "timeline": "2 months",
                "expected_impact": "95% defect detection rate"
            },
            {
                "action": "Enhanced supplier quality requirements",
                "timeline": "1 month",
                "expected_impact": "Improved component reliability"
            }
        ]


async def demo_manufacturing():
    """Demo the manufacturing insights agent"""
    print("\n" + "="*60)
    print("🏭 MANUFACTURING INSIGHTS AGENT DEMO")
    print("="*60 + "\n")
    
    agent = ManufacturingInsightsAgent()
    await agent.start()
    
    # Analyze failure pattern
    pattern_task = {
        "type": "analyze_failure_pattern",
        "component": "Alternator",
        "vehicle_data": [
            {"vehicle_id": "VIN001", "batch_id": "BATCH2024Q1"},
            {"vehicle_id": "VIN002", "batch_id": "BATCH2024Q1"},
            {"vehicle_id": "VIN003", "batch_id": "BATCH2024Q2"}
        ]
    }
    
    result = await agent.process_task(pattern_task)
    print(f"✅ Pattern Analysis: {result['total_failures']} failures detected")
    
    # Generate RCA report
    rca_task = {"type": "generate_rca_report", "component": "Alternator"}
    rca = await agent.process_task(rca_task)
    print(f"✅ RCA Report: {rca['report']['report_id']}")
    print(f"   Cost Impact: ${rca['report']['estimated_cost_impact']:,}")
    
    await agent.stop()
    print("\n✅ DEMO COMPLETE\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(demo_manufacturing())
