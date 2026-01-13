"""
Security utilities for authentication and password hashing
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # Bcrypt has a 72-byte password limit
    password_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(password_bytes.decode('utf-8'), hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storage"""
    # Bcrypt has a 72-byte password limit, truncate if necessary
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes.decode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Dictionary containing claims (typically {"sub": user_id})
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_mock_otp() -> str:
    """
    Generate a mock OTP code for MVP

    In production, this would use Twilio to send a real SMS OTP.
    For MVP, we just return a fixed code and log it.
    """
    mock_code = "123456"
    print(f"[MOCK OTP] Generated code: {mock_code}")
    return mock_code


def verify_mock_otp(code: str) -> bool:
    """
    Verify a mock OTP code for MVP

    In production, this would verify against a stored OTP with expiration.
    For MVP, we just accept "123456".
    """
    is_valid = code == "123456"
    print(f"[MOCK OTP] Verifying code {code}: {'✓ valid' if is_valid else '✗ invalid'}")
    return is_valid
