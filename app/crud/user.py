from sqlalchemy.orm import Session
from app.db.models import user as models # Assuming this is where your User model is defined
from app.db.models.user import User # Direct import for type hinting clarity
from app.schemas import user as schemas # Assuming your user creation schemas are here
from app.core.security import hash_password # Assuming your password hashing utility is here
from app.services.email import send_reset_email # Import send_reset_email for sending the code
from datetime import datetime, timedelta
import random # For generating the 6-digit code


def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Retrieves a user from the database by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user in the database.
    """
    hashed_pw = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, email: str, new_password: str) -> bool:
    """
    Updates the password for a user.
    """
    user = get_user_by_email(db, email)
    if user:
        user.hashed_password = hash_password(new_password)
        db.commit()
        return True
    return False

def set_password_reset_code(db: Session, user: models.User, code: str):
    """
    Sets a password reset code for a user with an expiry time.
    """
    user.reset_code = code
    # Set code expiry to 20 minutes from now
    user.reset_code_expiry = datetime.utcnow() + timedelta(minutes=20)
    db.add(user)
    db.commit()
    db.refresh(user)

def verify_reset_code(db: Session, email: str, code: str) -> bool:
    """
    Verifies if a given reset code for an email is valid and not expired.
    """
    user = get_user_by_email(db, email)
    # Check if user exists, code matches, and code has not expired
    if not user or user.reset_code != code:
        return False
    if not user.reset_code_expiry or user.reset_code_expiry < datetime.utcnow():
        return False
    return True

def clear_reset_code(db: Session, user: models.User):
    """
    Clears the password reset code and its expiry for a user.
    """
    user.reset_code = None
    user.reset_code_expiry = None
    db.add(user)
    db.commit()
    db.refresh(user)

def generate_and_send_reset_code(db: Session, user: models.User):
    """
    Generates a 6-digit reset code, stores it in the database,
    and sends it to the user's email.
    """
    reset_code = str(random.randint(100000, 999999))
    set_password_reset_code(db, user, reset_code)
    # Assuming send_reset_email takes 'to_email' and 'code' arguments
    send_reset_email(to_email=user.email, code=reset_code)
