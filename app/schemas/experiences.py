from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExperienceCreate(BaseModel):
    resume_version_id:int
    job_title: str
    company_name: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    description:str
    desc_generated_by_ai: Optional[bool] = None
    
class ExperienceOut(BaseModel):
    id: int
    resume_version_id:int
    job_title: str
    company_name: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    description:str
    desc_generated_by_ai: Optional[bool] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 