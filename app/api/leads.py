
from fastapi import APIRouter
from datetime import datetime

from app.schemas.lead import LeadCreate
from app.database.connection import get_database
from pydantic import BaseModel, EmailStr
from bson import ObjectId

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/")
async def create_lead(lead: LeadCreate):
    print('callled api leads')
    db = get_database()

    lead_data = lead.model_dump()

    lead_data["createdAt"] = datetime.now()

    result = await db["LeadCreate"].insert_one(lead_data)

    return {"status":200, "success" : True,
            "message": "lead created", 
            "lead_id": str(result.inserted_id)}

class LeadUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None

@router.put("/{lead_id}")
async def edit_lead(lead_id: str,lead:LeadUpdate):
    lead_data = lead.model_dump(exclude_unset=True)

    db = get_database()
    result = await db["LeadCreate"].update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": lead_data}
    )

    print("Lead ID:", lead_id)
    print("Updated fields:", lead_data)
    return {
        "status":201,
        "success":True,
        "message":"lead updated successfully"
    }

