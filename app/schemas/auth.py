from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """
    Schema for user login requests.
    Includes an optional 'remember_me' flag.
    """
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="yourStrongPassword")
    remember_me: bool = Field(False, description="Set to true to keep the user logged in for a longer period.")

class TokenResponse(BaseModel):
    """
    Schema for the token response after successful login.
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int # Time in seconds until the token expires

#Remember Me