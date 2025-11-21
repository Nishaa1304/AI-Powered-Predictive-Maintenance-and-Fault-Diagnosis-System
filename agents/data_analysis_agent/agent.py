"""
Data Analysis Agent
Processes vehicle telemetry data and detects anomalies
"""
import sys
sys.path.append('..')

from base_agent import BaseAgent, AgentPriority
from typing import Dict, Any
import numpy as np
from datetime import datetime

class DataAnalysisAgent(BaseAgent):
    """
    Agent responsible for:
    - Processing real-time vehicle telemetry
    - Feature extraction for ML models
    - Real-time anomaly detection
    - Data quality validation
    """
    
    def __init__(self, agent_id: str = "data_analysis_001"):
        super().__init__(agent_id, "DataAnalysisAgent")
        self.baseline_metrics = {}
        self.anomaly_threshold = 0.85
    
    async def initialize(self) -> bool:
        """Initialize data analysis resources"""
        self.logger.info("Initializing Data Analysis Agent...")
        # Load baseline metrics
        # Initialize anomaly detection model
        # Connect to data sources
        return True
    
    async def shutdown(self) -> bool:
        """Cleanup resources"""
        self.logger.info("Shutting down Data Analysis Agent...")
        return True
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming telemetry data"""
        try:
            self.update_activity()
            
            vehicle_id = task["data"].get("vehicle_id")
            telemetry = task["data"].get("telemetry", {})
            
            self.logger.info(f"Processing telemetry for vehicle: {vehicle_id}")
            
            # 1. Validate data quality
            is_valid = self._validate_telemetry(telemetry)
            
            if not is_valid:
                return {"status": "invalid_data", "vehicle_id": vehicle_id}
            
            # 2. Extract features
            features = self._extract_features(telemetry)
            
            # 3. Detect anomalies
            anomalies = self._detect_anomalies(features)
            
            # 4. Calculate risk score
            risk_score = self._calculate_risk_score(features, anomalies)
            
            result = {
                "status": "success",
                "vehicle_id": vehicle_id,
                "features": features,
                "anomalies": anomalies,
                "risk_score": risk_score,
                "timestamp": datetime.now().isoformat(),
                "requires_diagnosis": risk_score > 0.7
            }
            
            self.logger.info(f"Analysis complete for {vehicle_id}. Risk score: {risk_score}")
            
            return result
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "error": str(e)}
    
    def _validate_telemetry(self, telemetry: Dict[str, Any]) -> bool:
        """Validate telemetry data quality"""
        required_fields = [
            "engine_temperature", "battery_voltage", "oil_pressure",
            "coolant_temperature", "rpm", "speed"
        ]
        
        for field in required_fields:
            if field not in telemetry:
                self.logger.warning(f"Missing required field: {field}")
                return False
            
            # Check for valid ranges
            value = telemetry[field]
            if not isinstance(value, (int, float)) or np.isnan(value):
                return False
        
        return True
    
    def _extract_features(self, telemetry: Dict[str, Any]) -> Dict[str, float]:
        """Extract relevant features from telemetry"""
        features = {
            "engine_temp_norm": telemetry.get("engine_temperature", 0) / 120.0,
            "battery_voltage_norm": telemetry.get("battery_voltage", 0) / 14.4,
            "oil_pressure_norm": telemetry.get("oil_pressure", 0) / 80.0,
            "coolant_temp_norm": telemetry.get("coolant_temperature", 0) / 100.0,
            "rpm_norm": telemetry.get("rpm", 0) / 6000.0,
            "speed_norm": telemetry.get("speed", 0) / 200.0,
        }
        
        # Add derived features
        features["engine_load"] = features["rpm_norm"] * features["engine_temp_norm"]
        features["power_demand"] = features["rpm_norm"] * features["speed_norm"]
        
        return features
    
    def _detect_anomalies(self, features: Dict[str, float]) -> list:
        """Detect anomalies in features"""
        anomalies = []
        
        # Simple threshold-based detection (replace with ML model)
        thresholds = {
            "engine_temp_norm": 0.9,
            "battery_voltage_norm": (0.7, 1.1),
            "oil_pressure_norm": 0.3,
            "coolant_temp_norm": 0.9
        }
        
        for feature, value in features.items():
            if feature in thresholds:
                threshold = thresholds[feature]
                
                if isinstance(threshold, tuple):
                    if value < threshold[0] or value > threshold[1]:
                        anomalies.append({
                            "feature": feature,
                            "value": value,
                            "severity": "high" if value < 0.5 else "medium"
                        })
                else:
                    if value > threshold:
                        anomalies.append({
                            "feature": feature,
                            "value": value,
                            "severity": "high"
                        })
        
        return anomalies
    
    def _calculate_risk_score(self, features: Dict[str, float], 
                            anomalies: list) -> float:
        """Calculate overall risk score"""
        if not anomalies:
            return 0.0
        
        # Weight anomalies by severity
        severity_weights = {"low": 0.3, "medium": 0.6, "high": 0.9, "critical": 1.0}
        
        total_risk = sum(severity_weights.get(a["severity"], 0.5) for a in anomalies)
        risk_score = min(total_risk / len(features), 1.0)
        
        return round(risk_score, 2)

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = DataAnalysisAgent()
        await agent.start()
        
        # Test with sample telemetry
        task = {
            "task_id": "test_001",
            "data": {
                "vehicle_id": "VIN12345",
                "telemetry": {
                    "engine_temperature": 105,
                    "battery_voltage": 12.2,
                    "oil_pressure": 45,
                    "coolant_temperature": 92,
                    "rpm": 3500,
                    "speed": 80
                }
            }
        }
        
        result = await agent.process_task(task)
        print("Analysis Result:", result)
        
        await agent.stop()
    
    asyncio.run(test_agent())
