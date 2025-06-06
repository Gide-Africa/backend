from pydantic import BaseModel
from typing import Optional

class SkillCreate(BaseModel):
    resume_version_id: int
    name: str
    skill_generated_by_ai: Optional[bool] = None
    
class SkillOut(BaseModel):
    id: int
    resume_version_id: int
    name: str
    skill_generated_by_ai: Optional[bool] = None
    
    class Config:
        from_attributes = True  
    
    