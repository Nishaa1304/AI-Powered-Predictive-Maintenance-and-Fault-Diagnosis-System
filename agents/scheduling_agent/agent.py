"""
Scheduling Agent - Autonomous Service Appointment Booking
Handles intelligent scheduling of service appointments
"""
import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, AgentStatus, AgentPriority


class SchedulingAgent(BaseAgent):
    """
    AI Agent for autonomous service appointment scheduling
    - Finds nearby service centers
    - Checks availability
    - Books appointments automatically
    - Sends confirmations
    - Handles rescheduling
    """
    
    def __init__(self):
        super().__init__(
            agent_id="agent-scheduling-001",
            agent_name="SchedulingAgent"
        )
        
        # Service center database (in production, this would be a real DB)
        self.service_centers = []
        self.bookings = []
        
        self.logger.info("Scheduling Agent created")
    
    async def initialize(self) -> bool:
        """Initialize service center data"""
        try:
            # Load mock service centers
            self.service_centers = self._load_service_centers()
            self.logger.info(f"✅ Loaded {len(self.service_centers)} service centers")
            return True
        except Exception as e:
            self.handle_error(e)
            return False
    
    async def shutdown(self) -> bool:
        """Cleanup resources"""
        self.logger.info("Shutting down Scheduling Agent")
        return True
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process scheduling tasks"""
        self.update_activity()
        
        task_type = task.get("type")
        
        if task_type == "find_service_centers":
            return await self.find_service_centers(task)
        elif task_type == "check_availability":
            return await self.check_availability(task)
        elif task_type == "book_appointment":
            return await self.book_appointment(task)
        elif task_type == "reschedule_appointment":
            return await self.reschedule_appointment(task)
        elif task_type == "cancel_appointment":
            return await self.cancel_appointment(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def find_service_centers(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Find service centers near customer location"""
        try:
            customer_location = task.get("customer_location", {})
            service_type = task.get("service_type", "general")
            max_distance_km = task.get("max_distance_km", 50)
            
            self.logger.info(f"🔍 Finding service centers within {max_distance_km}km")
            
            # Filter and sort service centers by distance
            nearby_centers = []
            for center in self.service_centers:
                # Calculate distance (simplified - in production use real geolocation)
                distance = self._calculate_distance(customer_location, center["location"])
                
                if distance <= max_distance_km:
                    center_info = {
                        **center,
                        "distance_km": round(distance, 1)
                    }
                    nearby_centers.append(center_info)
            
            # Sort by distance
            nearby_centers.sort(key=lambda x: x["distance_km"])
            
            self.logger.info(f"✅ Found {len(nearby_centers)} service centers")
            
            return {
                "status": "success",
                "service_centers": nearby_centers,
                "count": len(nearby_centers)
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def check_availability(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check availability at service centers"""
        try:
            service_center_id = task.get("service_center_id")
            preferred_dates = task.get("preferred_dates", [])
            service_duration_minutes = task.get("service_duration_minutes", 120)
            
            self.logger.info(f"📅 Checking availability for center {service_center_id}")
            
            # Get service center
            center = next((c for c in self.service_centers if c["id"] == service_center_id), None)
            if not center:
                return {"status": "error", "message": "Service center not found"}
            
            # Generate available slots (in production, check real calendar)
            available_slots = self._generate_available_slots(
                center,
                preferred_dates,
                service_duration_minutes
            )
            
            self.logger.info(f"✅ Found {len(available_slots)} available slots")
            
            return {
                "status": "success",
                "service_center": center,
                "available_slots": available_slots,
                "count": len(available_slots)
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def book_appointment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Book a service appointment"""
        try:
            booking_details = {
                "booking_id": f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "service_center_id": task.get("service_center_id"),
                "customer_name": task.get("customer_name"),
                "customer_phone": task.get("customer_phone"),
                "vehicle_id": task.get("vehicle_id"),
                "appointment_time": task.get("appointment_time"),
                "service_type": task.get("service_type", "Predictive Maintenance"),
                "estimated_duration": task.get("estimated_duration", 120),
                "status": "confirmed",
                "created_at": datetime.now().isoformat(),
                "notes": task.get("notes", "")
            }
            
            # Save booking
            self.bookings.append(booking_details)
            
            # Send confirmation (simulated)
            confirmation = await self._send_confirmation(booking_details)
            
            self.logger.info(f"✅ Appointment booked: {booking_details['booking_id']}")
            
            return {
                "status": "success",
                "booking": booking_details,
                "confirmation": confirmation,
                "message": "Appointment successfully booked"
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def reschedule_appointment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Reschedule an existing appointment"""
        try:
            booking_id = task.get("booking_id")
            new_time = task.get("new_appointment_time")
            
            # Find booking
            booking = next((b for b in self.bookings if b["booking_id"] == booking_id), None)
            if not booking:
                return {"status": "error", "message": "Booking not found"}
            
            # Update booking
            old_time = booking["appointment_time"]
            booking["appointment_time"] = new_time
            booking["rescheduled_at"] = datetime.now().isoformat()
            booking["rescheduled_from"] = old_time
            
            self.logger.info(f"✅ Appointment rescheduled: {booking_id}")
            
            return {
                "status": "success",
                "booking": booking,
                "message": "Appointment successfully rescheduled"
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    async def cancel_appointment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel an appointment"""
        try:
            booking_id = task.get("booking_id")
            
            # Find and update booking
            booking = next((b for b in self.bookings if b["booking_id"] == booking_id), None)
            if not booking:
                return {"status": "error", "message": "Booking not found"}
            
            booking["status"] = "cancelled"
            booking["cancelled_at"] = datetime.now().isoformat()
            booking["cancellation_reason"] = task.get("reason", "Customer request")
            
            self.logger.info(f"✅ Appointment cancelled: {booking_id}")
            
            return {
                "status": "success",
                "booking": booking,
                "message": "Appointment successfully cancelled"
            }
            
        except Exception as e:
            self.handle_error(e)
            return {"status": "error", "message": str(e)}
    
    def _load_service_centers(self) -> List[Dict[str, Any]]:
        """Load service center data"""
        return [
            {
                "id": "SC001",
                "name": "AutoCare Center Downtown",
                "location": {"lat": 40.7128, "lng": -74.0060},
                "address": "123 Main St, New York, NY 10001",
                "phone": "+1-555-0101",
                "rating": 4.8,
                "services": ["Maintenance", "Diagnostics", "Repair"],
                "working_hours": {
                    "monday": "08:00-18:00",
                    "tuesday": "08:00-18:00",
                    "wednesday": "08:00-18:00",
                    "thursday": "08:00-18:00",
                    "friday": "08:00-18:00",
                    "saturday": "09:00-15:00",
                    "sunday": "Closed"
                }
            },
            {
                "id": "SC002",
                "name": "Premium Auto Service",
                "location": {"lat": 40.7580, "lng": -73.9855},
                "address": "456 Park Ave, New York, NY 10022",
                "phone": "+1-555-0102",
                "rating": 4.9,
                "services": ["Maintenance", "Diagnostics", "Repair", "Detailing"],
                "working_hours": {
                    "monday": "07:00-19:00",
                    "tuesday": "07:00-19:00",
                    "wednesday": "07:00-19:00",
                    "thursday": "07:00-19:00",
                    "friday": "07:00-19:00",
                    "saturday": "08:00-16:00",
                    "sunday": "Closed"
                }
            },
            {
                "id": "SC003",
                "name": "QuickFix Auto Shop",
                "location": {"lat": 40.6782, "lng": -73.9442},
                "address": "789 Brooklyn Ave, Brooklyn, NY 11201",
                "phone": "+1-555-0103",
                "rating": 4.5,
                "services": ["Maintenance", "Quick Service"],
                "working_hours": {
                    "monday": "08:00-17:00",
                    "tuesday": "08:00-17:00",
                    "wednesday": "08:00-17:00",
                    "thursday": "08:00-17:00",
                    "friday": "08:00-17:00",
                    "saturday": "09:00-14:00",
                    "sunday": "Closed"
                }
            }
        ]
    
    def _calculate_distance(
        self, 
        loc1: Dict[str, float], 
        loc2: Dict[str, float]
    ) -> float:
        """Calculate distance between two locations (simplified)"""
        # In production, use proper geolocation library
        import math
        
        if not loc1 or not loc2:
            return 999.9
        
        lat1, lng1 = loc1.get("lat", 0), loc1.get("lng", 0)
        lat2, lng2 = loc2.get("lat", 0), loc2.get("lng", 0)
        
        # Haversine formula (simplified)
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlng/2) * math.sin(dlng/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def _generate_available_slots(
        self,
        center: Dict[str, Any],
        preferred_dates: List[str],
        duration_minutes: int
    ) -> List[Dict[str, Any]]:
        """Generate available time slots"""
        slots = []
        
        # Generate slots for next 7 days if no preferred dates
        if not preferred_dates:
            start_date = datetime.now() + timedelta(days=1)
            preferred_dates = [
                (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range(7)
            ]
        
        for date_str in preferred_dates[:7]:  # Limit to 7 days
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = date.strftime("%A").lower()
                
                # Check if center is open
                working_hours = center["working_hours"].get(day_name)
                if not working_hours or working_hours == "Closed":
                    continue
                
                # Parse working hours
                start_time, end_time = working_hours.split("-")
                start_hour = int(start_time.split(":")[0])
                end_hour = int(end_time.split(":")[0])
                
                # Generate slots (every 2 hours)
                for hour in range(start_hour, end_hour, 2):
                    slot_time = date.replace(hour=hour, minute=0, second=0)
                    
                    # Skip past times
                    if slot_time < datetime.now():
                        continue
                    
                    slots.append({
                        "slot_id": f"SLOT{slot_time.strftime('%Y%m%d%H%M')}",
                        "date": date_str,
                        "time": f"{hour:02d}:00",
                        "datetime": slot_time.isoformat(),
                        "available": True,
                        "duration_minutes": duration_minutes
                    })
            
            except Exception as e:
                continue
        
        return slots[:20]  # Return max 20 slots
    
    async def _send_confirmation(self, booking: Dict[str, Any]) -> Dict[str, Any]:
        """Send booking confirmation (simulated)"""
        await asyncio.sleep(0.5)  # Simulate API call
        
        return {
            "sent": True,
            "method": "sms",
            "phone": booking.get("customer_phone"),
            "message": f"Your appointment is confirmed for {booking['appointment_time']}. "
                      f"Booking ID: {booking['booking_id']}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_bookings(self, vehicle_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all bookings or bookings for a specific vehicle"""
        if vehicle_id:
            return [b for b in self.bookings if b["vehicle_id"] == vehicle_id]
        return self.bookings


# Demo/Test function
async def demo_scheduling():
    """Demo the scheduling agent"""
    print("\n" + "="*60)
    print("📅 SCHEDULING AGENT DEMO")
    print("="*60 + "\n")
    
    # Create agent
    agent = SchedulingAgent()
    await agent.start()
    
    # Test 1: Find service centers
    print("\n🔍 Test 1: Find Service Centers")
    print("-" * 60)
    find_task = {
        "type": "find_service_centers",
        "customer_location": {"lat": 40.7128, "lng": -74.0060},
        "service_type": "maintenance",
        "max_distance_km": 20
    }
    find_result = await agent.process_task(find_task)
    print(f"✅ Found {find_result['count']} service centers:")
    for center in find_result['service_centers'][:3]:
        print(f"   - {center['name']}: {center['distance_km']}km away (Rating: {center['rating']})")
    
    # Test 2: Check availability
    print("\n📅 Test 2: Check Availability")
    print("-" * 60)
    availability_task = {
        "type": "check_availability",
        "service_center_id": "SC001",
        "preferred_dates": [
            (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        ],
        "service_duration_minutes": 120
    }
    availability_result = await agent.process_task(availability_task)
    print(f"✅ Found {availability_result['count']} available slots:")
    for slot in availability_result['available_slots'][:5]:
        print(f"   - {slot['date']} at {slot['time']}")
    
    # Test 3: Book appointment
    print("\n📝 Test 3: Book Appointment")
    print("-" * 60)
    booking_task = {
        "type": "book_appointment",
        "service_center_id": "SC001",
        "customer_name": "John Smith",
        "customer_phone": "+1-555-0123",
        "vehicle_id": "VINDEMO001",
        "appointment_time": availability_result['available_slots'][0]['datetime'],
        "service_type": "Alternator Replacement",
        "estimated_duration": 120,
        "notes": "Predicted failure - proactive maintenance"
    }
    booking_result = await agent.process_task(booking_task)
    print(f"✅ Appointment booked!")
    print(f"   Booking ID: {booking_result['booking']['booking_id']}")
    print(f"   Time: {booking_result['booking']['appointment_time']}")
    print(f"   Service: {booking_result['booking']['service_type']}")
    
    # Test 4: View all bookings
    print("\n📊 Test 4: View All Bookings")
    print("-" * 60)
    all_bookings = agent.get_bookings()
    print(f"Total bookings: {len(all_bookings)}")
    for booking in all_bookings:
        print(f"   - {booking['booking_id']}: {booking['customer_name']} - {booking['status']}")
    
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
    asyncio.run(demo_scheduling())
