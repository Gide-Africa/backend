from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError # Imported globally as they are essential for token operations
from passlib.context import CryptContext

from app.core.config import settings # Assuming settings are correctly imported and configured

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token with a configurable expiration.
    
    Args:
        data (dict): The payload to encode in the token (e.g., {"sub": user.email, "user_id": user.id}).
        expires_delta (Optional[timedelta]): The timedelta for token expiration.
                                            If None, uses the default from settings.
    
    Returns:
        str: The encoded JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Fallback to default expiration from settings if expires_delta is not provided
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    # Use settings.SECRET_KEY and settings.ALGORITHM
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Decodes and validates a JWT access token.
    
    Args:
        token (str): The JWT to decode.
        
    Returns:
        Optional[dict]: The decoded payload if valid, otherwise None.
    """
    try:
        # Use settings.SECRET_KEY and settings.ALGORITHM
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
