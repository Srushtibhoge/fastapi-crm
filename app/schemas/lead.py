
from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    source: str = "website"
    status: str = "New"
    assignedTo: str | None = None
    
