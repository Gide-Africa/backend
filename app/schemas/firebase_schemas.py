# app/schemas/firebase_schemas.py
from pydantic import BaseModel
from app.schemas.user import UserOut # --- ADD THIS IMPORT! ---

class FirebaseTokenRequest(BaseModel):
    """
    Schema for requests containing a Firebase ID token.
    """
    id_token: str

class AuthSuccessResponse(BaseModel):
    """
    Schema for a successful authentication response.
    Includes the authenticated user's data and an access token.
    """
    user: UserOut # --- CHANGED FROM 'dict' TO 'UserOut' ---
    access_token: str
    token_type: str = "bearer" # Added token_type for consistency
    expires_in: int = 3600 # Added expires_in for consistency (example default)
