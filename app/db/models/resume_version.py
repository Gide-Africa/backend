from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ResumeVersion(Base):
    __tablename__ = "resume_version"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resume.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    resume = relationship("Resume", back_populates="versions")
    experiences = relationship("Experience", back_populates="resume_version")
    personal_info = relationship("PersonalInfo", back_populates="resume_version")
    summary = relationship("Summary", back_populates="resume_version")
    educations = relationship("Education", back_populates="resume_version")
    skills = relationship("Skill", back_populates="resume_version")