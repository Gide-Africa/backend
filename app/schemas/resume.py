from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResumeCreate(BaseModel):
    user_id:int
    title:str

class ResumeOut(BaseModel):
    id: int
    user_id:int
    title:str
    created_at: datetime
    updated_at:datetime

    model_config = {
        "from_attributes": True,
    }
