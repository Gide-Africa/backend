from pydantic import BaseModel, EmailStr, Field

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

class PasswordResetVerify(BaseModel): # New schema for the /verify-code endpoint
    email: EmailStr = Field(..., example="user@example.com", description="User's email for password reset code verification")
    code: str = Field(..., min_length=6, max_length=6, example="123456", description="6-digit password reset code")

class PasswordResetConfirm(BaseModel): # Used for the final /reset endpoint
    email: EmailStr = Field(..., example="user@example.com", description="User's email for password reset confirmation")
    code: str = Field(..., min_length=6, max_length=6, example="123456", description="6-digit password reset code (re-verified)")
    new_password: str = Field(..., min_length=8, example="newStrongPassword123")
