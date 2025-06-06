from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    resume_version_id = Column(Integer, ForeignKey("resume_version.id"), nullable=False)
    degree = Column(String, nullable=False)
    institution_name = Column(String, nullable=False) 
    location = Column(String, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    additional_info = Column(Text, nullable=True)        
    
    
    resume_version = relationship("ResumeVersion", back_populates="educations") 
   
    