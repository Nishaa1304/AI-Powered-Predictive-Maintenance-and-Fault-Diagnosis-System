"""
Diagnosis Agent
Predicts vehicle failures and analyzes fault codes
"""
import sys
sys.path.append('../..')

from agents.base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

class DiagnosisAgent(BaseAgent):
    """
    Agent responsible for:
    - Predicting vehicle component failures
    - Analyzing DTC (Diagnostic Trouble Codes)
    - Classifying failure severity
    - Estimating time-to-failure
    """
    
    def __init__(self, agent_id: str = "diagnosis_001"):
        super().__init__(agent_id, "DiagnosisAgent")
        self.prediction_threshold = 0.75
        self.dtc_database = {}
        
    async def initialize(self) -> bool:
        """Initialize diagnosis resources"""
        self.logger.info("Initializing Diagnosis Agent...")
        # Load ML models for failure prediction
        # Load DTC database
        self._load_dtc_database()
        return True
    
    async def shutdown(self) -> bool:
        """Cleanup resources"""
        self.logger.info("Shutting down Diagnosis Agent...")
        return True
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process diagnosis request"""
        try:
            self.update_activity()
            
            vehicle_id = task["data"].get("vehicle_id")
            features = task["data"].get("features", {})
            anomalies = task["data"].get("anomalies", [])
            
            self.logger.info(f"Diagnosing vehicle: {vehicle_id}")
            
            # 1. Predict failures
            predictions = self._predict_failures(features, anomalies)
            
            # 2. Analyze DTC codes if present
            dtc_codes = task["data"].get("dtc_codes", [])
            dtc_analysis = self._analyze_dtc_codes(dtc_codes)
            
            # 3. Determine severity and urgency
            severity = self._classify_severity(predictions, dtc_analysis)
            
            # 4. Estimate time to failure
            ttf = self._estimate_time_to_failure(predictions, severity)
            
            # 5. Generate recommendations
            recommendations = self._generate_recommendations(predictions, severity)
            
            result = {
                "status": "success",
                "vehicle_id": vehicle_id,
                "predictions": predictions,
                "dtc_analysis": dtc_analysis,
                "severity": severity,
                "time_to_failure_days": ttf,
                "recommendations": recommendations,
                "requires_immediate_action": severity in ["critical", "high"],
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"Diagnosis complete for {vehicle_id}. Severity: {severity}")
            
            return result
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "error": str(e)}
    
    def _predict_failures(self, features: Dict[str, float], 
                         anomalies: List[Dict]) -> List[Dict[str, Any]]:
        """Predict component failures using ML models"""
        predictions = []
        
        # Simulate ML model predictions (replace with actual model)
        if anomalies:
            for anomaly in anomalies:
                feature_name = anomaly["feature"]
                
                # Map features to components
                component_mapping = {
                    "engine_temp_norm": "Engine Cooling System",
                    "battery_voltage_norm": "Battery/Alternator",
                    "oil_pressure_norm": "Oil Pump",
                    "coolant_temp_norm": "Cooling System"
                }
                
                component = component_mapping.get(feature_name, "Unknown Component")
                
                # Simulate prediction confidence
                confidence = random.uniform(0.75, 0.95)
                
                predictions.append({
                    "component": component,
                    "failure_type": "degradation" if confidence < 0.85 else "imminent_failure",
                    "confidence": round(confidence, 2),
                    "contributing_factors": [anomaly["feature"]]
                })
        
        return predictions
    
    def _analyze_dtc_codes(self, dtc_codes: List[str]) -> Dict[str, Any]:
        """Analyze DTC codes"""
        if not dtc_codes:
            return {"has_dtc": False}
        
        analysis = {
            "has_dtc": True,
            "codes": []
        }
        
        for code in dtc_codes:
            code_info = self.dtc_database.get(code, {
                "description": "Unknown code",
                "severity": "medium",
                "system": "unknown"
            })
            
            analysis["codes"].append({
                "code": code,
                "description": code_info["description"],
                "severity": code_info["severity"],
                "system": code_info["system"]
            })
        
        return analysis
    
    def _classify_severity(self, predictions: List[Dict], 
                          dtc_analysis: Dict) -> str:
        """Classify overall severity"""
        severity_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        max_severity = 0
        
        # Check predictions
        for pred in predictions:
            if pred["confidence"] > 0.9:
                max_severity = max(max_severity, severity_scores["high"])
            elif pred["confidence"] > 0.8:
                max_severity = max(max_severity, severity_scores["medium"])
        
        # Check DTC codes
        if dtc_analysis.get("has_dtc"):
            for code_info in dtc_analysis.get("codes", []):
                code_severity = severity_scores.get(code_info.get("severity", "low"), 1)
                max_severity = max(max_severity, code_severity)
        
        # Map back to severity label
        severity_map = {1: "low", 2: "medium", 3: "high", 4: "critical"}
        return severity_map.get(max_severity, "low")
    
    def _estimate_time_to_failure(self, predictions: List[Dict], 
                                   severity: str) -> int:
        """Estimate days until failure"""
        severity_ttf = {
            "critical": 1,
            "high": 3,
            "medium": 7,
            "low": 14
        }
        return severity_ttf.get(severity, 30)
    
    def _generate_recommendations(self, predictions: List[Dict], 
                                  severity: str) -> List[str]:
        """Generate maintenance recommendations"""
        recommendations = []
        
        if severity in ["critical", "high"]:
            recommendations.append("Schedule immediate inspection")
            recommendations.append("Avoid long-distance travel")
        
        for pred in predictions:
            component = pred["component"]
            recommendations.append(f"Inspect {component}")
            
            if "Battery" in component:
                recommendations.append("Check alternator and battery terminals")
            elif "Cooling" in component:
                recommendations.append("Check coolant level and radiator")
        
        return recommendations
    
    def _load_dtc_database(self):
        """Load DTC code database"""
        # Sample DTC codes (expand this)
        self.dtc_database = {
            "P0300": {
                "description": "Random/Multiple Cylinder Misfire Detected",
                "severity": "high",
                "system": "engine"
            },
            "P0420": {
                "description": "Catalyst System Efficiency Below Threshold",
                "severity": "medium",
                "system": "emissions"
            },
            "P0171": {
                "description": "System Too Lean (Bank 1)",
                "severity": "medium",
                "system": "fuel"
            }
        }

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = DiagnosisAgent()
        await agent.start()
        
        task = {
            "task_id": "test_diagnosis",
            "data": {
                "vehicle_id": "VIN12345",
                "features": {
                    "engine_temp_norm": 0.95,
                    "battery_voltage_norm": 0.75
                },
                "anomalies": [
                    {"feature": "battery_voltage_norm", "severity": "high"}
                ],
                "dtc_codes": ["P0300"]
            }
        }
        
        result = await agent.process_task(task)
        print("Diagnosis Result:", result)
        
        await agent.stop()
    
    asyncio.run(test_agent())
