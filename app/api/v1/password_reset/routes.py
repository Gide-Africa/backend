from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.password_reset import PasswordResetRequest, PasswordResetVerify, PasswordResetConfirm # Corrected imports
from app.api.deps import get_db
from app.crud import user as crud_user
# send_reset_email is now called from crud_user.generate_and_send_reset_code, so no direct import here
# random and uuid are no longer directly used here as their logic is encapsulated in crud_user

router = APIRouter()

@router.get("/check-email")
def check_email_exists(email: str, db: Session = Depends(get_db)):
    """
    Checks if an email already exists in the database.
    Returns {"exists": True} if found, {"exists": False} otherwise.
    Always returns 200 OK.
    """
    user = crud_user.get_user_by_email(db, email)
    if user:
        return {"exists": True, "message": "Email found."}
    return {"exists": False, "message": "Email not found."}

@router.post("/forgot", status_code=status.HTTP_200_OK)
def forgot_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Initiates the password reset process by sending a 6-digit code to the user's email.
    """
    user = crud_user.get_user_by_email(db, payload.email)
    if not user:
        # For security, return a generic success message even if user not found
        # to prevent email enumeration.
        return {"message": "If a matching email address was found, a password reset code has been sent to your email."}
    
    # Call the CRUD function to generate, store, and send the code
    crud_user.generate_and_send_reset_code(db, user) 
    return {"message": "Password reset code sent to your email."}


@router.post("/verify-code", status_code=status.HTTP_200_OK)
def verify_password_reset_code(payload: PasswordResetVerify, db: Session = Depends(get_db)):
    """
    Verifies the 6-digit password reset code provided by the user.
    This is an intermediate step before allowing password change.
    """
    # Verify the provided code against the stored one
    if not crud_user.verify_reset_code(db, payload.email, payload.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset code.")
    
    return {"message": "Code verified successfully. You can now set your new password."}


@router.post("/reset", status_code=status.HTTP_200_OK)
def reset_password_confirm(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Confirms the password reset with the code and sets the new password.
    The email and code are re-verified for security.
    """
    # Verify the provided code again (important for security, even if frontend pre-verified)
    if not crud_user.verify_reset_code(db, payload.email, payload.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset code.")

    # Update the user's password
    success = crud_user.update_user_password(db, payload.email, payload.new_password)
    if not success:
        # If user was found by verify_reset_code but update failed, it's a server issue
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password update failed.")
    
    # Clear the reset code and its expiry after successful password reset
    # Re-fetch user to ensure latest state before clearing
    user = crud_user.get_user_by_email(db, payload.email) 
    if user:
        crud_user.clear_reset_code(db, user)
        
    return {"message": "Password has been reset successfully."}