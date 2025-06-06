from pydantic import BaseModel
from typing import Optional

class SummaryCreate(BaseModel):
    resume_version_id: int
    summary: str    
    summary_generated_by_ai: Optional[bool] = None
    
# class SummaryUpdate(BaseModel):
#     summary: str             
    
class SummaryOut(BaseModel):
    id: int
    resume_version_id: int
    summary: str
    summary_generated_by_ai: Optional[bool] = None
    created_at: str
    updated_at:str
    
    class Config:
        from_attributes = True