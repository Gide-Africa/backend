from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    full_name = Column(String, nullable=False)
    # New fields for password reset code
    reset_code = Column(String, nullable=True)
    reset_code_expiry = Column(DateTime, nullable=True)
    
    resumes = relationship("Resume", back_populates="user")  