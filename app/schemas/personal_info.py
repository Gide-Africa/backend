from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PersonalInfoCreate(BaseModel):
    resume_version_id:int
    full_name:str
    email:EmailStr
    phone_number:str
    location:Optional[str] = None
    linkedin_url:Optional[str] = None
    portfolio_url:Optional[str] = None
    
class PersonalInfoOut(BaseModel):
    id:int
    resume_version_id:int
    full_name:str
    email:EmailStr
    phone_number:str
    location:Optional[str] = None
    linkedin_url:Optional[str] = None
    portfolio_url:Optional[str] = None
    created_at:datetime
    updated_at:datetime
    
    class Config:
        from_attributes:True