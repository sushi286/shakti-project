from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Contact(BaseModel):
    name: str
    phone: str
    relationship: str
    is_primary: bool = False

class UserProfile(BaseModel):
    user_id: str
    name: str
    phone: Optional[str]
    email: Optional[str]
    emergency_contacts: List[Contact] = []

# Mock database
users_db = {
    "user123": {
        "user_id": "user123",
        "name": "Sara Jain",
        "phone": "+919876543210",
        "emergency_contacts": [
            {"name": "Father", "phone": "+919876543211", "relationship": "parent", "is_primary": True},
            {"name": "Mother", "phone": "+919876543212", "relationship": "parent", "is_primary": False},
            {"name": "Friend", "phone": "+919876543213", "relationship": "friend", "is_primary": False}
        ]
    }
}

@router.get("/profile/{user_id}")
def get_user_profile(user_id: str):
    if user_id in users_db:
        return {"status": "success", "profile": users_db[user_id]}
    return {"status": "error", "message": "User not found"}

@router.post("/profile/{user_id}")
def update_user_profile(user_id: str, profile: dict):
    if user_id not in users_db:
        users_db[user_id] = {"user_id": user_id}
    
    users_db[user_id].update(profile)
    return {"status": "success", "message": "Profile updated"}

@router.get("/contacts/{user_id}")
def get_user_contacts(user_id: str):
    if user_id in users_db:
        return {
            "status": "success",
            "contacts": users_db[user_id].get("emergency_contacts", [])
        }
    return {"status": "error", "message": "User not found"}

@router.post("/contacts/{user_id}")
def add_user_contact(user_id: str, contact: Contact):
    if user_id not in users_db:
        return {"status": "error", "message": "User not found"}
    
    contacts = users_db[user_id].get("emergency_contacts", [])
    
    # Check if already exists
    for c in contacts:
        if c["phone"] == contact.phone:
            return {"status": "error", "message": "Contact already exists"}
    
    # Limit to 5 contacts
    if len(contacts) >= 5:
        return {"status": "error", "message": "Maximum 5 contacts allowed"}
    
    contacts.append(contact.dict())
    users_db[user_id]["emergency_contacts"] = contacts
    
    return {"status": "success", "message": "Contact added"}