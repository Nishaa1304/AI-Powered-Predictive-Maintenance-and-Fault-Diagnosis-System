"""
Feedback Agent - Post-Service Experience Collection
Collects and analyzes customer feedback with sentiment analysis
"""
import os
import sys
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, AgentStatus


class FeedbackAgent(BaseAgent):
    """
    AI Agent for collecting and analyzing post-service feedback
    - Automated feedback collection via SMS/Email/Voice
    - Sentiment analysis
    - Issue detection
    - Quality metrics tracking
    """
    
    def __init__(self):
        super().__init__(
            agent_id="agent-feedback-001",
            agent_name="FeedbackAgent"
        )
        self.feedback_records = []
        self.logger.info("Feedback Agent created")
    
    async def initialize(self) -> bool:
        """Initialize feedback agent"""
        self.logger.info("✅ Feedback Agent initialized")
        return True
    
    async def shutdown(self) -> bool:
        """Cleanup resources"""
        self.logger.info("Shutting down Feedback Agent")
        return True
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process feedback tasks"""
        self.update_activity()
        
        task_type = task.get("type")
        
        if task_type == "collect_feedback":
            return await self.collect_feedback(task)
        elif task_type == "analyze_sentiment":
            return await self.analyze_sentiment(task)
        elif task_type == "generate_report":
            return await self.generate_report(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def collect_feedback(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Collect customer feedback"""
        try:
            feedback = {
                "feedback_id": f"FB{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "booking_id": task.get("booking_id"),
                "customer_name": task.get("customer_name"),
                "vehicle_id": task.get("vehicle_id"),
                "rating": task.get("rating", 0),
                "comments": task.get("comments", ""),
                "service_quality": task.get("service_quality", 0),
                "timeliness": task.get("timeliness", 0),
                "staff_courtesy": task.get("staff_courtesy", 0),
                "would_recommend": task.get("would_recommend", True),
                "collected_at": datetime.now().isoformat()
            }
            
            # Analyze sentiment
            sentiment = await self._analyze_sentiment(feedback["comments"])
            feedback["sentiment"] = sentiment
            
            self.feedback_records.append(feedback)
            
            self.logger.info(f"✅ Feedback collected: {feedback['feedback_id']}")
            
            return {
                "status": "success",
                "feedback": feedback,
                "message": "Feedback successfully recorded"
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def analyze_sentiment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment of feedback text"""
        try:
            text = task.get("text", "")
            sentiment = await self._analyze_sentiment(text)
            
            return {
                "status": "success",
                "text": text,
                "sentiment": sentiment
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def generate_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate feedback analytics report"""
        try:
            if not self.feedback_records:
                return {"status": "success", "message": "No feedback data available"}
            
            # Calculate metrics
            total = len(self.feedback_records)
            avg_rating = sum(f["rating"] for f in self.feedback_records) / total
            positive = sum(1 for f in self.feedback_records if f["sentiment"] == "positive")
            negative = sum(1 for f in self.feedback_records if f["sentiment"] == "negative")
            
            report = {
                "total_responses": total,
                "average_rating": round(avg_rating, 2),
                "positive_sentiment": round((positive / total) * 100, 1),
                "negative_sentiment": round((negative / total) * 100, 1),
                "recommendation_rate": round(
                    sum(1 for f in self.feedback_records if f["would_recommend"]) / total * 100, 1
                ),
                "generated_at": datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Feedback report generated")
            
            return {
                "status": "success",
                "report": report
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        if not text:
            return "neutral"
        
        text_lower = text.lower()
        positive_words = ["great", "excellent", "good", "happy", "satisfied", "amazing", "wonderful"]
        negative_words = ["bad", "poor", "terrible", "awful", "disappointed", "unhappy"]
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"


async def demo_feedback():
    """Demo the feedback agent"""
    print("\n" + "="*60)
    print("💬 FEEDBACK AGENT DEMO")
    print("="*60 + "\n")
    
    agent = FeedbackAgent()
    await agent.start()
    
    # Collect feedback
    feedback_task = {
        "type": "collect_feedback",
        "booking_id": "BK20251122",
        "customer_name": "John Smith",
        "vehicle_id": "VINDEMO001",
        "rating": 5,
        "comments": "Excellent service! The team was professional and the repair was done quickly.",
        "service_quality": 5,
        "timeliness": 5,
        "staff_courtesy": 5,
        "would_recommend": True
    }
    
    result = await agent.process_task(feedback_task)
    print(f"✅ Feedback collected: {result['feedback']['sentiment']} sentiment")
    
    # Generate report
    report_task = {"type": "generate_report"}
    report = await agent.process_task(report_task)
    print(f"\n📊 Report: Avg Rating {report['report']['average_rating']}/5")
    
    await agent.stop()
    print("\n✅ DEMO COMPLETE\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(demo_feedback())
