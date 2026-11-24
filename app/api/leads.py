
from fastapi import APIRouter, HTTPException
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

    try:
        lead_data = lead.model_dump(exclude_unset=True)

        print("Lead ID:", lead_id)
        print("Updated fields:", lead_data)
        if not ObjectId.is_valid(lead_id):
            raise HTTPException(
                status_code=400,
                detail='invalid lead Id'
            )

        db = get_database()
        result = await db["leads"].update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": lead_data}
        )

        if result.matched_count ==0:
            raise HTTPException(
                status_code=404,
                datail="User doesn't exists"
            )

        return {
            "status":201,
            "success":True,
            "message":"lead updated successfully"
        }
    except Exception:
        raise
    except Exception as e:
         print("Error updating lead:", e)

         raise HTTPException(
             status_code=500,
             detail="internal server error"
         )

@router.get("/{lead_id}")
async def get_lead(lead_id:str):
    try:
        if not ObjectId.is_valid(lead_id):
            raise HTTPException(
                        status_code=400,
                        detail="invalid lead id"
                    )

        db = get_database()
        print(lead_id)
        lead = await db["leads"].find_one({"_id": ObjectId(lead_id)})

        if lead is None:
            raise HTTPException(
            status_code=404,
            detail="User doesn't exists"
            )
        print('lead',lead)
 # Convert MongoDB ObjectId to string
        lead["_id"] = str(lead["_id"])
        return({
            "status":200,
            "success": True,
            "message":"fetched!",
            "lead":lead
        })
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail='Internal server error'
        )



@router.get("/")
async def get_leads():
    try:
        db = get_database()

        leads = await db["leads"].find({}).to_list(length=None)

        for lead in leads:
            lead["_id"] = str(lead["_id"])

        return {
            "status": 200,
            "message": "Fetched successfully",
            "leads": leads
        }

    except Exception as e:
        print("Error fetching leads:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
