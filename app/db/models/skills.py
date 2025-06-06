from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    resume_version_id = Column(Integer, ForeignKey("resume_version.id"), nullable=False)
    name = Column(String, nullable=False)
    skill_generated_by_ai = Column(Boolean, nullable=True)
    
    resume_version = relationship("ResumeVersion", back_populates="skills")