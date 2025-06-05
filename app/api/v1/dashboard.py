from fastapi import APIRouter, Depends, HTTPException, status # Added status for clarity
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.user import get_user_by_email # Still needed for get_user_by_email within dependency
from app.crud.resume import get_user_resumes # Assuming this is for fetching resume data
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Import your User model and UserOut schema
from app.db.models.user import User # Assuming User model is defined in app/db/models/user.py
from app.schemas.user import UserOut # Assuming UserOut schema is defined in app/schemas/user.py

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# --- DEPENDENCY: get_current_user ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Dependency function to retrieve the current authenticated user's database object.
    
    It decodes the JWT token from the Authorization header, extracts the user's email
    (from the 'sub' claim), and then fetches the corresponding user from the database.
    
    Raises HTTPException 401 Unauthorized if:
    - The token is missing or invalid.
    - The token's payload does not contain a 'sub' (subject/email) claim.
    - The user associated with the email in the token is not found in the database.
    
    Returns:
        User: The SQLAlchemy User object for the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token using your application's SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub") # The 'sub' claim typically holds the user's identifier (email in this case)
        
        if user_email is None:
            # If 'sub' claim is missing from the token payload, raise an error
            raise credentials_exception
    except JWTError:
        # If JWT decoding fails (e.g., token is expired, malformed, or signature is invalid)
        raise credentials_exception
    
    # Fetch the user from the database using the email extracted from the token
    user = get_user_by_email(db, user_email)
    if user is None:
        # If no user is found with the extracted email, it indicates an invalid user or revoked access
        raise credentials_exception
        
    # Optional: If your User model has an 'is_active' field and you want to enforce it
    # if not user.is_active:
    #    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account.")
        
    return user

# --- ENDPOINT: /me ---
@router.get("/me", response_model=UserOut)
def get_current_user_profile(
    current_user: User = Depends(get_current_user) # Inject the User object directly
):
    """
    Retrieves the profile information of the current authenticated user.
    
    This endpoint is protected and requires a valid JWT token in the
    'Authorization: Bearer <token>' header.
    
    Returns:
        UserOut: A Pydantic model representing the authenticated user's profile.
    """
    # The 'current_user' parameter already holds the SQLAlchemy User object,
    # which Pydantic's response_model will automatically serialize into UserOut.
    return current_user

# --- ENDPOINT: / (User Dashboard) ---
@router.get("/")
def user_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Use the get_current_user dependency
):
    """
    Provides a dashboard view for the current authenticated user.
    
    Includes basic user information, the count of their resumes,
    and a list of their resume versions.
    
    This endpoint is protected and requires a valid JWT token.
    """
    # Use the 'current_user' object directly to get the user's ID and other details.
    resumes = get_user_resumes(db, current_user.id) # Assuming get_user_resumes works with user ID
    total_versions = len(resumes)
    
    # Prepare information for each resume version
    versions_info = [{"id": r.id, "version": r.version, "created_at": r.created_at} for r in resumes]

    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username, # Assuming your User model has 'username'
            "created_at": current_user.created_at
        },
        "resume_count": total_versions,
        "resume_versions": versions_info
    }
