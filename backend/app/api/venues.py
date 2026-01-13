"""
Venue API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.models.user import User
from app.models.venue import Venue, VenuePhoto, VenueAmenity, VenuePricing, VenueAvailability
from app.schemas.venue import (
    VenueCreate,
    VenueUpdate,
    VenueResponse,
    VenueListResponse,
)
from app.api.auth import get_current_user

router = APIRouter(prefix="/venues", tags=["Venues"])


@router.post("", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
async def create_venue(
    venue_data: VenueCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new venue (venue owners only)

    Args:
        venue_data: Venue creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created venue data with all relationships

    Raises:
        HTTPException: If user is not a venue owner
    """
    # Check if user is a venue owner
    if not current_user.is_venue_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only venue owners can create venues",
        )

    # Validate capacity
    if venue_data.capacity_max < venue_data.capacity_min:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum capacity must be greater than or equal to minimum capacity",
        )

    # Create venue
    new_venue = Venue(
        owner_id=current_user.id,
        name=venue_data.name,
        description=venue_data.description,
        borough=venue_data.borough,
        neighborhood=venue_data.neighborhood,
        address=venue_data.address,
        capacity_min=venue_data.capacity_min,
        capacity_max=venue_data.capacity_max,
        base_price=venue_data.base_price,
        min_spend=venue_data.min_spend,
        instant_book_enabled=venue_data.instant_book_enabled,
        verification_status="pending",
    )

    db.add(new_venue)
    db.flush()  # Get venue ID before adding related records

    # Add photos
    for photo_data in venue_data.photos:
        photo = VenuePhoto(
            venue_id=new_venue.id,
            url=photo_data.url,
            is_hero=photo_data.is_hero,
            order=photo_data.order,
        )
        db.add(photo)

    # Add amenities
    for amenity_data in venue_data.amenities:
        amenity = VenueAmenity(
            venue_id=new_venue.id,
            amenity_type=amenity_data.amenity_type,
            details=amenity_data.details,
        )
        db.add(amenity)

    # Add pricing packages
    for pricing_data in venue_data.pricing_packages:
        pricing = VenuePricing(
            venue_id=new_venue.id,
            package_name=pricing_data.package_name,
            base_price=pricing_data.base_price,
            min_spend=pricing_data.min_spend,
            inclusions=pricing_data.inclusions,
        )
        db.add(pricing)

    # Add availability
    if venue_data.availability:
        availability = VenueAvailability(
            venue_id=new_venue.id,
            calendar_url=venue_data.availability.calendar_url,
            sync_status="not_synced",
        )
        db.add(availability)

    db.commit()
    db.refresh(new_venue)

    return new_venue


@router.get("", response_model=List[VenueListResponse])
async def list_venues(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List all venues (paginated)

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of venues with minimal data
    """
    venues = db.query(Venue).offset(skip).limit(limit).all()

    # Convert to list response format with hero photo
    result = []
    for venue in venues:
        hero_photo = next((p.url for p in venue.photos if p.is_hero), None)
        if not hero_photo and venue.photos:
            hero_photo = venue.photos[0].url

        result.append(
            VenueListResponse(
                id=venue.id,
                name=venue.name,
                borough=venue.borough,
                neighborhood=venue.neighborhood,
                capacity_min=venue.capacity_min,
                capacity_max=venue.capacity_max,
                base_price=venue.base_price,
                verification_status=venue.verification_status,
                hero_photo=hero_photo,
            )
        )

    return result


@router.get("/my-venues", response_model=List[VenueResponse])
async def get_my_venues(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all venues owned by the current user

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of user's venues with full details
    """
    venues = db.query(Venue).filter(Venue.owner_id == current_user.id).all()
    return venues


@router.get("/{venue_id}", response_model=VenueResponse)
async def get_venue(
    venue_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a single venue by ID with all details

    Args:
        venue_id: Venue ID
        db: Database session

    Returns:
        Venue data with all relationships

    Raises:
        HTTPException: If venue not found
    """
    venue = db.query(Venue).filter(Venue.id == venue_id).first()

    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found",
        )

    return venue


@router.put("/{venue_id}", response_model=VenueResponse)
async def update_venue(
    venue_id: int,
    venue_data: VenueUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a venue (owner only)

    Args:
        venue_id: Venue ID
        venue_data: Venue update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated venue data

    Raises:
        HTTPException: If venue not found or user is not the owner
    """
    venue = db.query(Venue).filter(Venue.id == venue_id).first()

    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found",
        )

    # Check ownership
    if venue.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own venues",
        )

    # Update fields
    update_data = venue_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(venue, field, value)

    # Validate capacity if both are being updated
    if venue_data.capacity_min and venue_data.capacity_max:
        if venue.capacity_max < venue.capacity_min:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum capacity must be greater than or equal to minimum capacity",
            )

    db.commit()
    db.refresh(venue)

    return venue


@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venue(
    venue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a venue (owner only)

    Args:
        venue_id: Venue ID
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If venue not found or user is not the owner
    """
    venue = db.query(Venue).filter(Venue.id == venue_id).first()

    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found",
        )

    # Check ownership
    if venue.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own venues",
        )

    db.delete(venue)
    db.commit()

    return None
