from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class PersonalInfo(Base):
    __tablename__ = "personal_information"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_version_id = Column(Integer, ForeignKey("resume_version.id"))
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    location = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)    
    
    resume_version = relationship("ResumeVersion", back_populates="personal_info")