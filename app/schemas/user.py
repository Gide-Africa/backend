from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Assuming UserCreate and UserOut are already defined in this file
class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="StrongPassword123")

class UserLogin(BaseModel):
    """
    Schema for user login requests, including the 'remember_me' option.
    """
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="yourStrongPassword")
    remember_me: bool = Field(False, description="Set to true to keep the user logged in for a longer period.")

class UserOut(BaseModel):
    """
    Schema for user data returned in responses (e.g., after registration).
    """
    id: int
    username: str
    email: EmailStr
    is_active: bool = True # Assuming this field exists in your User model

    class Config:
        from_attributes = True # Or orm_mode = True for Pydantic v1
