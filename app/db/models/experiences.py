from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship 
from app.db.base import Base

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    resume_version_id = Column(Integer, ForeignKey("resume_version.id"), nullable=False)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    description = Column(Text, nullable=True)
    desc_generated_by_ai = Column(Boolean, nullable=True)
    
    resume_version = relationship("ResumeVersion", back_populates="experiences")