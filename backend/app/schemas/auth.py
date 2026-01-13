"""
Authentication schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    """Schema for user registration"""

    email: EmailStr
    phone: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    is_host: bool = True
    is_venue_owner: bool = False


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user data in responses"""

    id: int
    email: str
    phone: Optional[str] = None
    name: str
    is_host: bool
    is_venue_owner: bool
    email_verified: bool
    phone_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data"""

    user_id: Optional[int] = None


class OTPRequest(BaseModel):
    """Schema for requesting an OTP"""

    phone: str = Field(..., pattern=r"^\+?1?\d{10,15}$")


class OTPVerify(BaseModel):
    """Schema for verifying an OTP"""

    phone: str = Field(..., pattern=r"^\+?1?\d{10,15}$")
    code: str = Field(..., min_length=6, max_length=6)
