# app/services/auth.py
import firebase_admin.auth
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status # Required for raising HTTP errors

from app.db.models.user import User # User model for type hinting
from app.crud.user import get_user_by_email, create_user # Now importing create_user as well
from app.schemas.user import UserCreate # Required for creating new user instances

from app.core.security import create_access_token, hash_password # Import hash_password for dummy password
from app.schemas.firebase_schemas import AuthSuccessResponse
from app.schemas.user import UserOut # Assuming your UserOut schema is defined

# It's assumed that firebase_admin.initialize_app() has been called elsewhere in your application startup.
# Example: In app/main.py or a dedicated app/core/firebase_config.py

async def handle_google_signin(db: Session, firebase_id_token: str) -> AuthSuccessResponse:
    """
    Handles Google Sign-In for existing users.
    Verifies the Firebase ID token and authenticates an existing user.
    If the user's email from the Google token is not found in your database,
    it raises a 404 NOT FOUND HTTPException, indicating they need to sign up.
    
    Returns user data and an application-specific access token upon successful login.
    """
    try:
        # 1. Verify the Firebase ID token with Google's servers
        decoded_token = firebase_admin.auth.verify_id_token(firebase_id_token)

        firebase_email = decoded_token.get("email")
        
        if not firebase_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Firebase token does not contain a valid email."
            )

        # 2. Check if the user exists in your database by email
        existing_user = get_user_by_email(db=db, email=firebase_email)

        if not existing_user:
            # If the user is NOT found, this is a sign-in attempt for an unregistered user.
            # Raise 404 to indicate user does not exist in our system.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, # Changed to 404 as user is not found for sign-in
                detail="User not found. Please sign up with Google."
            )

        # If we reach here, the user *does* exist in your database and can sign in.
        user_for_token_and_response: User = existing_user

        # 3. Generate your application-specific access token
        access_token_data = {
            "sub": str(user_for_token_and_response.id), # Use ID for robustness
            "email": user_for_token_and_response.email
        }
        access_token = create_access_token(data=access_token_data)

        # 4. Prepare user data for the response using UserOut schema
        user_response_data = UserOut(
            id=user_for_token_and_response.id,
            email=user_for_token_and_response.email,
            username=user_for_token_and_response.username # Assuming User model has 'username'
        )

        # 5. Return the AuthSuccessResponse object
        return AuthSuccessResponse(user=user_response_data, access_token=access_token)

    except firebase_admin.auth.InvalidIdTokenError as e:
        print(f"DEBUG: Invalid Firebase ID token during sign-in: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase ID token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as e:
        raise e # Re-raise explicit HTTPExceptions (like the 404 for user not found)
    except Exception as e:
        print(f"ERROR: An unexpected error occurred during Google Sign-In: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed due to an unexpected server error: {e}",
        )

async def handle_google_signup(db: Session, firebase_id_token: str) -> AuthSuccessResponse:
    """
    Handles Google Sign-Up for new users.
    Verifies the Firebase ID token and registers a new user if they don't exist in the database.
    If the user already exists, it raises a 409 CONFLICT HTTPException.
    
    Returns user data and an application-specific access token upon successful registration.
    """
    try:
        # 1. Verify the Firebase ID token with Google's servers
        decoded_token = firebase_admin.auth.verify_id_token(firebase_id_token)

        firebase_email = decoded_token.get("email")
        firebase_display_name = decoded_token.get("name")
        
        if not firebase_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Firebase token does not contain a valid email."
            )

        # 2. Check if the user already exists in your database
        existing_user = get_user_by_email(db=db, email=firebase_email)

        if existing_user:
            # If the user already exists, this is a sign-up attempt for an existing user.
            # Raise 409 CONFLICT to indicate the user already has an account.
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, # 409 Conflict indicates resource already exists
                detail="User already exists. Please sign in with Google instead."
            )

        # 3. If user does not exist, proceed with registration
        # Generate a dummy password since Google handles the primary authentication.
        # It's good practice to have a hashed password even if not used for direct login.
        # Using a portion of the UID for uniqueness.
        dummy_raw_password = f"GOOGLE_AUTH_{decoded_token.get('uid')[:10]}" 
        hashed_dummy_password = hash_password(dummy_raw_password)
        
        # Determine username: prefer Firebase display name, fall back to email prefix
        username = firebase_display_name if firebase_display_name else firebase_email.split('@')[0]
        
        # Create a UserCreate schema instance for new user creation
        new_user_data = UserCreate(
            email=firebase_email,
            password=hashed_dummy_password, # Use the hashed dummy password
            username=username
            # Add other fields if required by your UserCreate schema and User model
        )
        
        # 4. Create the new user in your database
        new_user = create_user(db, user=new_user_data)
        
        # 5. Generate your application-specific access token for the new user
        access_token_data = {
            "sub": str(new_user.id),
            "email": new_user.email
        }
        access_token = create_access_token(data=access_token_data)

        # 6. Prepare user data for the response
        user_response_data = UserOut(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username
        )

        # 7. Return the AuthSuccessResponse object
        return AuthSuccessResponse(user=user_response_data, access_token=access_token)

    except firebase_admin.auth.InvalidIdTokenError as e:
        print(f"DEBUG: Invalid Firebase ID token during sign-up: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase ID token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as e:
        raise e # Re-raise explicit HTTPExceptions (like the 409 for user exists)
    except Exception as e:
        print(f"ERROR: An unexpected error occurred during Google Sign-Up: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed due to an unexpected server error: {e}",
        )
