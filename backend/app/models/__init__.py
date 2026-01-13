"""
Database models

Import all models here so Alembic can detect them for migrations.
"""

from app.models.user import User
from app.models.venue import Venue, VenuePhoto, VenueAmenity, VenuePricing, VenueAvailability
from app.models.brief import EventBrief
from app.models.offer import MatchResult, Offer, Booking, Review, MessageRelayLog
from app.models.enums import (
    EventType,
    FoodBevLevel,
    AlcoholLevel,
    AVNeeds,
    OfferStatus,
    BookingStatus,
    BriefStatus,
    Borough,
)

__all__ = [
    # User
    "User",
    # Venue
    "Venue",
    "VenuePhoto",
    "VenueAmenity",
    "VenuePricing",
    "VenueAvailability",
    # Brief
    "EventBrief",
    # Offers and Bookings
    "MatchResult",
    "Offer",
    "Booking",
    "Review",
    "MessageRelayLog",
    # Enums
    "EventType",
    "FoodBevLevel",
    "AlcoholLevel",
    "AVNeeds",
    "OfferStatus",
    "BookingStatus",
    "BriefStatus",
    "Borough",
]
