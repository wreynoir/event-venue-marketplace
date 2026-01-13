"""
Authentication API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.db.base import get_db
from app.models.user import User
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    OTPRequest,
    OTPVerify,
)
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    generate_mock_otp,
    verify_mock_otp,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


# Dependency to get current user from JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency to extract and validate current user from JWT token

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user data

    Raises:
        HTTPException: If email already exists
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check if phone already exists (if provided)
    if user_data.phone:
        existing_phone = db.query(User).filter(User.phone == user_data.phone).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered",
            )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        phone=user_data.phone,
        name=user_data.name,
        hashed_password=hashed_password,
        is_host=user_data.is_host,
        is_venue_owner=user_data.is_venue_owner,
        email_verified=False,
        phone_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password

    Args:
        credentials: User login credentials
        db: Database session

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    # Verify password
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information

    Args:
        current_user: Current authenticated user (from JWT)

    Returns:
        Current user data
    """
    return current_user


@router.post("/otp/request", status_code=status.HTTP_200_OK)
async def request_otp(otp_request: OTPRequest):
    """
    Request an OTP code (MOCK for MVP)

    In production, this would:
    1. Generate a random 6-digit code
    2. Store it in Redis with 5-minute expiration
    3. Send it via Twilio SMS

    For MVP, we just return a mock success response and log the code.

    Args:
        otp_request: Phone number to send OTP to

    Returns:
        Success message
    """
    mock_code = generate_mock_otp()

    return {
        "success": True,
        "message": f"OTP sent to {otp_request.phone}",
        "mock_code": mock_code,  # Only for MVP - remove in production!
    }


@router.post("/otp/verify", response_model=Token)
async def verify_otp(otp_verify: OTPVerify, db: Session = Depends(get_db)):
    """
    Verify OTP code and return JWT token (MOCK for MVP)

    In production, this would:
    1. Check Redis for stored OTP
    2. Verify code matches and hasn't expired
    3. Mark phone as verified
    4. Return JWT token

    For MVP, we accept "123456" as valid code.

    Args:
        otp_verify: Phone number and OTP code
        db: Database session

    Returns:
        JWT access token

    Raises:
        HTTPException: If OTP is invalid or user not found
    """
    # Verify mock OTP
    if not verify_mock_otp(otp_verify.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP code",
        )

    # Find user by phone
    user = db.query(User).filter(User.phone == otp_verify.phone).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this phone number",
        )

    # Mark phone as verified
    user.phone_verified = True
    db.commit()

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return Token(access_token=access_token)
