from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime
import uuid
from services.crime_database import crime_db

router = APIRouter()

# Mock database for user contacts (in real app, use MongoDB/SQL)
user_contacts_db = {
    "user123": [
        {"name": "Father", "phone": "+919876543210", "relationship": "parent"},
        {"name": "Mother", "phone": "+919876543211", "relationship": "parent"},
        {"name": "Friend", "phone": "+919876543212", "relationship": "friend"}
    ]
}

class SOSRequest(BaseModel):
    user_id: str
    lat: float
    lng: float
    message: Optional[str] = "Emergency! I need help immediately!"
    trigger_call: bool = False  # Whether to also call

class SOSResponse(BaseModel):
    status: str
    sos_id: str
    timestamp: str
    nearest_police: List[dict]
    contacts_notified: List[str]
    police_contacted: bool
    helpline_contacted: bool

def send_sms_to_contact(phone: str, message: str, user_location: str):
    """Mock SMS sending function"""
    print(f"[SMS] To {phone}: {message}")
    print(f"[SMS] Location: {user_location}")
    # In real app: integrate with Twilio, Fast2SMS, etc.
    return True

def call_phone(phone: str):
    """Mock call function"""
    print(f"[CALL] Calling {phone}...")
    # In real app: integrate with telephony API
    return True

def notify_emergency_services(lat: float, lng: float, sos_id: str):
    """Notify police/helpline"""
    print(f"[EMERGENCY] SOS {sos_id} at {lat},{lng}")
    # In real app: integrate with police API
    return True

@router.post("/sos", response_model=SOSResponse)
async def trigger_sos(data: SOSRequest, background_tasks: BackgroundTasks):
    print("🚨 SOS TRIGGERED 🚨")
    
    # Generate SOS ID
    sos_id = str(uuid.uuid4())[:8].upper()
    timestamp = datetime.datetime.now().isoformat()
    
    # Get nearest police stations
    nearest_stations = crime_db.get_nearest_police_stations(data.lat, data.lng, 3)
    
    # Get user's emergency contacts
    user_contacts = user_contacts_db.get(data.user_id, [])
    
    # Prepare message with location
    location_link = f"https://maps.google.com/?q={data.lat},{data.lng}"
    emergency_message = f"""
🚨 EMERGENCY ALERT 🚨
{data.message}

User ID: {data.user_id}
Location: {data.lat}, {data.lng}
Map: {location_link}
Time: {timestamp}
SOS ID: {sos_id}

Nearest Police:
{chr(10).join([f"- {s['name']}: {s['phone']} ({s['distance_km']}km)" for s in nearest_stations[:2]])}
"""
    
    # Notify emergency contacts in background
    contacts_notified = []
    for contact in user_contacts[:3]:  # Limit to 3 contacts
        phone = contact.get("phone")
        if phone:
            background_tasks.add_task(send_sms_to_contact, phone, emergency_message, f"{data.lat},{data.lng}")
            contacts_notified.append(f"{contact['name']} ({phone})")
            
            # Trigger call if requested
            if data.trigger_call:
                background_tasks.add_task(call_phone, phone)
    
    # Notify nearest police station
    police_contacted = False
    helpline_contacted = False
    
    if nearest_stations:
        # Contact the nearest police station
        nearest = nearest_stations[0]
        background_tasks.add_task(notify_emergency_services, data.lat, data.lng, sos_id)
        police_contacted = True
        
        # Also contact women helpline if available
        for station in nearest_stations:
            if station.get("type") == "helpline":
                background_tasks.add_task(
                    send_sms_to_contact, 
                    station["phone"], 
                    f"Women emergency at {data.lat},{data.lng}. SOS: {sos_id}",
                    f"{data.lat},{data.lng}"
                )
                helpline_contacted = True
                break
    
    print(f"SOS {sos_id} handled. Contacts notified: {len(contacts_notified)}")
    
    return {
        "status": "success",
        "sos_id": sos_id,
        "timestamp": timestamp,
        "nearest_police": nearest_stations,
        "contacts_notified": contacts_notified,
        "police_contacted": police_contacted,
        "helpline_contacted": helpline_contacted
    }

# API to manage emergency contacts
@router.get("/contacts/{user_id}")
def get_emergency_contacts(user_id: str):
    return {
        "status": "success",
        "contacts": user_contacts_db.get(user_id, [])
    }

@router.post("/contacts/{user_id}")
def add_emergency_contact(user_id: str, contact: dict):
    if user_id not in user_contacts_db:
        user_contacts_db[user_id] = []
    
    # Limit to 5 contacts
    if len(user_contacts_db[user_id]) < 5:
        user_contacts_db[user_id].append(contact)
        return {"status": "success", "message": "Contact added"}
    else:
        return {"status": "error", "message": "Maximum 5 contacts allowed"}