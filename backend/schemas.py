from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone: str
    emergency_contact: str
