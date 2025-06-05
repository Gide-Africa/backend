from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud import user as crud_user
# from app.crud.user import get_user_by_email # Removed: not needed as crud_user is used
from app.core.security import verify_password, create_access_token
from app.api.deps import get_db
from app.services.auth import handle_google_signin, handle_google_signup # --- IMPORTED handle_google_signup ---
from app.schemas.firebase_schemas import FirebaseTokenRequest, AuthSuccessResponse
from datetime import timedelta # Import timedelta for token expiration
from app.core.config import settings # --- IMPORTED SETTINGS for token expiration ---

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user with email and password.
    """
    db_user = crud_user.get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud_user.create_user(db, user=user_data)

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Handles traditional email/password login.
    Supports "Remember Me" for configurable token expiration.
    """
    user = crud_user.get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Determine token expiration based on 'remember_me' flag
    if user_data.remember_me:
        # Longer expiration for "Remember Me" (e.g., 7 days)
        access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS) 
    else:
        # Shorter expiration for standard login (e.g., 30 minutes, from settings)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create the access token with the determined expiration
    token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, # Include user_id if needed in token payload
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()) # Return expiration in seconds
    }

@router.post("/google-signin", response_model=AuthSuccessResponse)
async def google_signin_endpoint( # --- RENAMED to avoid conflict with service function ---
    request: FirebaseTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Handles Google Sign-In for existing users.
    Verifies Firebase ID token and authenticates if user exists.
    Returns 404 if user is not found.
    """
    try:
        # Pass the injected 'db' session to the service function
        result = await handle_google_signin(db, request.id_token)
        return result
    except HTTPException as e:
        # Catch and re-raise HTTPExceptions from the service (e.g., 404 for user not found)
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during Google Sign-In: {e}",
        )

@router.post("/google-signup", response_model=AuthSuccessResponse) # --- NEW ENDPOINT FOR GOOGLE SIGN-UP ---
async def google_signup_endpoint(
    request: FirebaseTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Handles Google Sign-Up for new users.
    Verifies Firebase ID token and registers a new user if they don't exist.
    Returns 409 if user already exists.
    """
    try:
        # Call the service function dedicated to Google Sign-Up
        result = await handle_google_signup(db, request.id_token)
        return result
    except HTTPException as e:
        # Catch and re-raise HTTPExceptions from the service (e.g., 409 for user exists)
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during Google Sign-Up: {e}",
        )

# Delete user endpoint
# from fastapi import FastAPI
from app.api.v1.dashboard import get_current_user
from app.db.models.user import User
# app=FastAPI()
@router.delete("/users/me")
async def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}


# Get current user function
from fastapi.security import OAuth2PasswordBearer
from app.db.models.user import User
oauth2_scheme= OAuth2PasswordBearer
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Implement logic to get the current user based on the token
    # For example:
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

#This is without Authentication
# from app.db.models.user import User

# @router.delete("/users/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted successfully"}