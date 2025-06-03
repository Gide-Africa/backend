from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResumeCreate(BaseModel):
    id:int
    name:str
    email:str
    phoneNumber:str
    location:str
    title=str

class ResumeOut(BaseModel):
    id: int
    content: str
    version: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
