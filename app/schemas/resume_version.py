from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from schemas.personal_info import PersonalInfoCreate, PersonalInfoOut
from schemas.summary import SummaryCreate, SummaryOut
from schemas.experiences import ExperienceCreate, ExperienceOut
from schemas.educations import EducationCreate, EducationOut
from schemas.skills import SkillCreate, SkillOut

class ResumeVersionCreate(BaseModel):
    resume_id:int
    version_number:int
    personal_info: PersonalInfoCreate
    summary: SummaryCreate
    experiences: List[ExperienceCreate]
    educations: List[EducationCreate]
    skills: List[SkillCreate]
    
class ResumeVersionOut(BaseModel):
    id:int
    resume_id:int
    version_number:int
    personal_info: PersonalInfoOut
    summary: SummaryOut
    experiences: List[ExperienceOut]
    educations: List[EducationOut]
    skills: List[SkillOut]
    created_at:datetime
    updated_at:datetime
    
    class Config:
        from_attributes: True 
    