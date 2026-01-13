"""
Venue schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.enums import Borough


# Venue Photo Schemas
class VenuePhotoCreate(BaseModel):
    """Schema for creating a venue photo"""
    url: str
    is_hero: bool = False
    order: int = 0


class VenuePhotoResponse(BaseModel):
    """Schema for venue photo in responses"""
    id: int
    venue_id: int
    url: str
    is_hero: bool
    order: int
    created_at: datetime

    class Config:
        from_attributes = True


# Venue Amenity Schemas
class VenueAmenityCreate(BaseModel):
    """Schema for creating a venue amenity"""
    amenity_type: str
    details: Optional[str] = None


class VenueAmenityResponse(BaseModel):
    """Schema for venue amenity in responses"""
    id: int
    venue_id: int
    amenity_type: str
    details: Optional[str] = None

    class Config:
        from_attributes = True


# Venue Pricing Schemas
class VenuePricingCreate(BaseModel):
    """Schema for creating a pricing package"""
    package_name: str
    base_price: float = Field(..., gt=0)
    min_spend: Optional[float] = Field(None, gt=0)
    inclusions: Optional[str] = None


class VenuePricingResponse(BaseModel):
    """Schema for pricing package in responses"""
    id: int
    venue_id: int
    package_name: str
    base_price: float
    min_spend: Optional[float] = None
    inclusions: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Venue Availability Schemas
class VenueAvailabilityCreate(BaseModel):
    """Schema for creating venue availability"""
    calendar_url: Optional[str] = None


class VenueAvailabilityResponse(BaseModel):
    """Schema for venue availability in responses"""
    id: int
    venue_id: int
    calendar_url: Optional[str] = None
    sync_status: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Main Venue Schemas
class VenueCreate(BaseModel):
    """Schema for creating a venue"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    borough: Borough
    neighborhood: Optional[str] = None
    address: str = Field(..., min_length=1)

    capacity_min: int = Field(..., gt=0)
    capacity_max: int = Field(..., gt=0)

    base_price: Optional[float] = Field(None, gt=0)
    min_spend: Optional[float] = Field(None, gt=0)

    instant_book_enabled: bool = False

    # Nested creates
    photos: List[VenuePhotoCreate] = []
    amenities: List[VenueAmenityCreate] = []
    pricing_packages: List[VenuePricingCreate] = []
    availability: Optional[VenueAvailabilityCreate] = None


class VenueUpdate(BaseModel):
    """Schema for updating a venue"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    borough: Optional[Borough] = None
    neighborhood: Optional[str] = None
    address: Optional[str] = None

    capacity_min: Optional[int] = Field(None, gt=0)
    capacity_max: Optional[int] = Field(None, gt=0)

    base_price: Optional[float] = Field(None, gt=0)
    min_spend: Optional[float] = Field(None, gt=0)

    instant_book_enabled: Optional[bool] = None
    verification_status: Optional[str] = None


class VenueResponse(BaseModel):
    """Schema for venue data in responses"""
    id: int
    owner_id: int
    name: str
    description: Optional[str] = None
    borough: Borough
    neighborhood: Optional[str] = None
    address: str

    capacity_min: int
    capacity_max: int

    base_price: Optional[float] = None
    min_spend: Optional[float] = None

    instant_book_enabled: bool
    verification_status: str

    created_at: datetime
    updated_at: datetime

    # Nested relationships
    photos: List[VenuePhotoResponse] = []
    amenities: List[VenueAmenityResponse] = []
    pricing_packages: List[VenuePricingResponse] = []
    availability: Optional[VenueAvailabilityResponse] = None

    class Config:
        from_attributes = True


class VenueListResponse(BaseModel):
    """Schema for venue in list views (minimal data)"""
    id: int
    name: str
    borough: Borough
    neighborhood: Optional[str] = None
    capacity_min: int
    capacity_max: int
    base_price: Optional[float] = None
    verification_status: str
    hero_photo: Optional[str] = None  # URL of hero photo

    class Config:
        from_attributes = True
