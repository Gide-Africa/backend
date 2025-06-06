from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship 
from app.db.base import Base

class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True, index=True)
    resume_version_id = Column(Integer, ForeignKey("resume_version.id"), nullable=False)
    summary_text = Column(Text, nullable=False)   
    summary_generated_by_ai = Column(Boolean, nullable=True)
    
    resume_version = relationship("ResumeVersion", back_populates="summary")