from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EducationCreate(BaseModel):
    resume_version_id: int
    degree: str
    institution: str
    location:Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    additional_info: Optional[str] = None
    
class EducationOut(BaseModel):
    id: int
    resume_version_id: int
    degree: str
    institution: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    additional_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True