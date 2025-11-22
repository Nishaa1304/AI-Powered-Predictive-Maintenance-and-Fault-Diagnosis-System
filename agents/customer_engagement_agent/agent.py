"""
Customer Engagement Agent with Real-Time Voice Calling
Handles voice-first customer engagement using Twilio and OpenAI
"""
import os
import sys
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, AgentStatus, AgentPriority

# For voice capabilities
try:
    from twilio.rest import Client as TwilioClient
    from twilio.twiml.voice_response import VoiceResponse, Gather
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️ Twilio not installed. Install with: pip install twilio")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not installed. Install with: pip install openai")


class CustomerEngagementAgent(BaseAgent):
    """
    AI Agent for voice-first customer engagement
    - Makes proactive voice calls to vehicle owners
    - Uses natural language to explain predicted failures
    - Empathetic and human-like communication
    - Handles real-time conversations
    """
    
    def __init__(self):
        super().__init__(
            agent_id="agent-customer-engagement-001",
            agent_name="CustomerEngagementAgent"
        )
        
        # Twilio configuration
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER", "")
        self.twilio_client = None
        
        # OpenAI configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_client = None
        
        # Call tracking
        self.active_calls = {}
        self.call_history = []
        
        self.logger.info("Customer Engagement Agent created")
    
    async def initialize(self) -> bool:
        """Initialize Twilio and OpenAI clients"""
        try:
            # Initialize Twilio
            if TWILIO_AVAILABLE and self.twilio_account_sid and self.twilio_auth_token:
                self.twilio_client = TwilioClient(
                    self.twilio_account_sid,
                    self.twilio_auth_token
                )
                self.logger.info("✅ Twilio client initialized")
            else:
                self.logger.warning("⚠️ Twilio credentials not configured - using simulation mode")
            
            # Initialize OpenAI
            if OPENAI_AVAILABLE and self.openai_api_key:
                self.openai_client = OpenAI(api_key=self.openai_api_key)
                self.logger.info("✅ OpenAI client initialized")
            else:
                self.logger.warning("⚠️ OpenAI API key not configured - using simulation mode")
            
            return True
        except Exception as e:
            self.handle_error(e)
            return False
    
    async def shutdown(self) -> bool:
        """Cleanup resources"""
        self.logger.info("Shutting down Customer Engagement Agent")
        return True
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer engagement tasks"""
        self.update_activity()
        
        task_type = task.get("type")
        
        if task_type == "initiate_voice_call":
            return await self.initiate_voice_call(task)
        elif task_type == "generate_voice_script":
            return await self.generate_voice_script(task)
        elif task_type == "handle_customer_response":
            return await self.handle_customer_response(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def initiate_voice_call(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate a real voice call to customer
        """
        try:
            customer_phone = task.get("customer_phone")
            vehicle_id = task.get("vehicle_id")
            failure_prediction = task.get("failure_prediction", {})
            
            self.logger.info(f"📞 Initiating voice call to {customer_phone} for vehicle {vehicle_id}")
            
            # Generate conversation script using AI
            script = await self.generate_voice_script({
                "vehicle_id": vehicle_id,
                "failure_prediction": failure_prediction,
                "customer_name": task.get("customer_name", "valued customer")
            })
            
            # Make real call if Twilio is configured
            if self.twilio_client and customer_phone:
                call_result = await self._make_real_call(customer_phone, script)
            else:
                # Simulation mode
                call_result = await self._simulate_call(customer_phone, script)
            
            # Record call in history
            call_record = {
                "call_id": call_result.get("call_id"),
                "timestamp": datetime.now().isoformat(),
                "customer_phone": customer_phone,
                "vehicle_id": vehicle_id,
                "script": script,
                "status": call_result.get("status"),
                "duration": call_result.get("duration", 0)
            }
            self.call_history.append(call_record)
            
            return {
                "status": "success",
                "call_id": call_result.get("call_id"),
                "message": "Voice call initiated successfully",
                "script": script,
                "call_details": call_result
            }
            
        except Exception as e:
            self.handle_error(e)
            return {
                "status": "error",
                "message": f"Failed to initiate call: {str(e)}"
            }
    
    async def _make_real_call(self, phone_number: str, script: Dict[str, Any]) -> Dict[str, Any]:
        """Make a real phone call using Twilio"""
        try:
            # Create TwiML for the call
            twiml_url = f"http://your-server.com/twiml/{script['call_id']}"
            
            call = self.twilio_client.calls.create(
                to=phone_number,
                from_=self.twilio_phone_number,
                url=twiml_url,
                method="POST"
            )
            
            self.logger.info(f"✅ Real call initiated: {call.sid}")
            
            return {
                "call_id": call.sid,
                "status": "initiated",
                "mode": "real",
                "phone_number": phone_number
            }
            
        except Exception as e:
            self.logger.error(f"Failed to make real call: {e}")
            # Fallback to simulation
            return await self._simulate_call(phone_number, script)
    
    async def _simulate_call(self, phone_number: str, script: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a phone call for demo purposes"""
        import uuid
        
        call_id = f"sim-{uuid.uuid4().hex[:8]}"
        
        self.logger.info(f"📞 SIMULATED CALL to {phone_number}")
        self.logger.info(f"🎭 Script: {script['greeting']}")
        
        # Simulate call duration
        await asyncio.sleep(2)
        
        return {
            "call_id": call_id,
            "status": "completed",
            "mode": "simulation",
            "phone_number": phone_number,
            "duration": 45,
            "transcript": script
        }
    
    async def generate_voice_script(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate natural, empathetic voice script using AI
        """
        try:
            vehicle_id = task.get("vehicle_id")
            failure_prediction = task.get("failure_prediction", {})
            customer_name = task.get("customer_name", "valued customer")
            
            component = failure_prediction.get("component", "a critical component")
            confidence = failure_prediction.get("confidence", 0.85) * 100
            days_until_failure = failure_prediction.get("time_to_failure_days", 3)
            
            # Use OpenAI to generate natural script if available
            if self.openai_client:
                script = await self._generate_ai_script(
                    customer_name, component, confidence, days_until_failure
                )
            else:
                # Fallback template
                script = self._generate_template_script(
                    customer_name, component, confidence, days_until_failure
                )
            
            return script
            
        except Exception as e:
            self.handle_error(e)
            return self._generate_template_script(
                "valued customer", "a component", 85, 3
            )
    
    async def _generate_ai_script(
        self, 
        customer_name: str, 
        component: str, 
        confidence: float, 
        days: int
    ) -> Dict[str, Any]:
        """Generate script using OpenAI"""
        try:
            prompt = f"""
            Generate a natural, empathetic phone call script for a predictive maintenance AI calling a customer.
            
            Context:
            - Customer name: {customer_name}
            - Component predicted to fail: {component}
            - Prediction confidence: {confidence:.0f}%
            - Estimated days until failure: {days}
            
            The script should:
            1. Be warm and empathetic
            2. Not cause panic
            3. Explain the issue clearly
            4. Offer to schedule service
            5. Sound natural and human-like
            
            Format as JSON with: greeting, issue_explanation, recommendation, scheduling_offer, closing
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an empathetic AI assistant helping vehicle owners."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            script_text = response.choices[0].message.content
            # Parse JSON from response
            import re
            json_match = re.search(r'\{.*\}', script_text, re.DOTALL)
            if json_match:
                script = json.loads(json_match.group())
            else:
                script = self._generate_template_script(customer_name, component, confidence, days)
            
            return script
            
        except Exception as e:
            self.logger.warning(f"AI script generation failed: {e}, using template")
            return self._generate_template_script(customer_name, component, confidence, days)
    
    def _generate_template_script(
        self, 
        customer_name: str, 
        component: str, 
        confidence: float, 
        days: int
    ) -> Dict[str, Any]:
        """Generate script from template"""
        return {
            "call_id": f"script-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "greeting": f"Hello {customer_name}, this is your vehicle's AI assistant calling. I hope you're having a great day!",
            "issue_explanation": f"I'm reaching out because our advanced diagnostic system has detected that your {component} might need attention soon. Based on our analysis with {confidence:.0f}% confidence, we predict it could fail within the next {days} days.",
            "recommendation": "While your vehicle is still safe to drive, we recommend scheduling a service appointment to prevent any inconvenience or potential breakdown.",
            "scheduling_offer": "I can help you schedule an appointment right now at a service center near you. Would you like me to check available times?",
            "closing": "Your safety and peace of mind are our top priorities. Thank you for trusting us with your vehicle's care!",
            "tone": "warm, empathetic, reassuring"
        }
    
    async def handle_customer_response(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer's response during call"""
        try:
            response_text = task.get("response_text", "")
            call_id = task.get("call_id")
            
            # Use NLP to understand customer intent
            intent = await self._analyze_customer_intent(response_text)
            
            if intent == "accept_scheduling":
                return {
                    "status": "success",
                    "action": "proceed_to_scheduling",
                    "message": "Customer wants to schedule appointment"
                }
            elif intent == "need_more_info":
                return {
                    "status": "success",
                    "action": "provide_details",
                    "message": "Customer needs more information"
                }
            elif intent == "decline":
                return {
                    "status": "success",
                    "action": "end_call_politely",
                    "message": "Customer declined service"
                }
            else:
                return {
                    "status": "success",
                    "action": "clarify",
                    "message": "Need clarification from customer"
                }
                
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def _analyze_customer_intent(self, text: str) -> str:
        """Analyze customer intent from their response"""
        text_lower = text.lower()
        
        # Simple intent detection (can be enhanced with NLP models)
        if any(word in text_lower for word in ["yes", "sure", "okay", "schedule", "book"]):
            return "accept_scheduling"
        elif any(word in text_lower for word in ["no", "not now", "later", "decline"]):
            return "decline"
        elif any(word in text_lower for word in ["why", "how", "what", "explain", "tell me more"]):
            return "need_more_info"
        else:
            return "unknown"
    
    def get_call_history(self) -> list:
        """Get history of all calls made"""
        return self.call_history
    
    def generate_twiml_response(self, script: Dict[str, Any]) -> str:
        """Generate TwiML for Twilio call"""
        if not TWILIO_AVAILABLE:
            return ""
        
        response = VoiceResponse()
        
        # Greeting
        response.say(script.get("greeting", ""), voice="alice", language="en-US")
        response.pause(length=1)
        
        # Issue explanation
        response.say(script.get("issue_explanation", ""), voice="alice", language="en-US")
        response.pause(length=1)
        
        # Recommendation
        response.say(script.get("recommendation", ""), voice="alice", language="en-US")
        response.pause(length=1)
        
        # Gather response
        gather = Gather(
            input="speech",
            action="/handle-response",
            method="POST",
            timeout=5,
            speechTimeout="auto"
        )
        gather.say(script.get("scheduling_offer", ""), voice="alice", language="en-US")
        response.append(gather)
        
        # If no response
        response.say("I didn't hear a response. Please call us back when you're ready. Have a great day!")
        
        return str(response)


# Demo/Test function
async def demo_customer_engagement():
    """Demo the customer engagement agent"""
    print("\n" + "="*60)
    print("🎭 CUSTOMER ENGAGEMENT AGENT DEMO")
    print("="*60 + "\n")
    
    # Create agent
    agent = CustomerEngagementAgent()
    await agent.start()
    
    # Test 1: Generate voice script
    print("\n📝 Test 1: Generate Voice Script")
    print("-" * 60)
    script_task = {
        "type": "generate_voice_script",
        "vehicle_id": "VINDEMO001",
        "customer_name": "John Smith",
        "failure_prediction": {
            "component": "Alternator",
            "confidence": 0.87,
            "time_to_failure_days": 3,
            "severity": "high"
        }
    }
    script_result = await agent.process_task(script_task)
    print(f"✅ Script generated:")
    for key, value in script_result.items():
        if key != "call_id":
            print(f"   {key}: {value}")
    
    # Test 2: Initiate voice call (simulation)
    print("\n📞 Test 2: Initiate Voice Call")
    print("-" * 60)
    call_task = {
        "type": "initiate_voice_call",
        "customer_phone": "+1-555-0123",
        "vehicle_id": "VINDEMO001",
        "customer_name": "John Smith",
        "failure_prediction": {
            "component": "Alternator",
            "confidence": 0.87,
            "time_to_failure_days": 3
        }
    }
    call_result = await agent.process_task(call_task)
    print(f"✅ Call Result: {call_result['status']}")
    print(f"   Call ID: {call_result.get('call_id')}")
    print(f"   Message: {call_result.get('message')}")
    
    # Test 3: Handle customer response
    print("\n💬 Test 3: Handle Customer Response")
    print("-" * 60)
    response_task = {
        "type": "handle_customer_response",
        "call_id": call_result.get('call_id'),
        "response_text": "Yes, I'd like to schedule an appointment"
    }
    response_result = await agent.process_task(response_task)
    print(f"✅ Intent detected: {response_result.get('action')}")
    print(f"   Message: {response_result.get('message')}")
    
    # Show call history
    print("\n📊 Call History")
    print("-" * 60)
    history = agent.get_call_history()
    print(f"Total calls made: {len(history)}")
    for call in history:
        print(f"   - {call['timestamp']}: {call['vehicle_id']} ({call['status']})")
    
    # Agent status
    print("\n📈 Agent Status")
    print("-" * 60)
    status = agent.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    await agent.stop()
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run demo
    asyncio.run(demo_customer_engagement())
