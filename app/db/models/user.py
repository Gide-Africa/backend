from sqlalchemy import Column, Integer, String, DateTime, Boolean # Import Boolean for is_active
from datetime import datetime
from app.db.base import Base # Assuming Base is defined in app/db/base.py

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    Defines the structure of a user record in the database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False, unique=True) # Added unique=True for username
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False) # Common field to enable/disable users
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Fields for the 6-digit password reset code
    reset_code = Column(String, nullable=True) # Stores the 6-digit code
    reset_code_expiry = Column(DateTime, nullable=True) # Stores the expiration timestamp for the code

    # No other temporary token fields are included as per the streamlined flow.
