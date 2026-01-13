"""
Enum types for database models
"""

import enum


class EventType(str, enum.Enum):
    """Type of event"""
    CORPORATE = "corporate"
    WEDDING = "wedding"
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    NETWORKING = "networking"
    CONFERENCE = "conference"
    OTHER = "other"


class FoodBevLevel(str, enum.Enum):
    """Food and beverage service level"""
    NONE = "none"
    LIGHT_BITES = "light_bites"
    FULL_CATERING = "full_catering"


class AlcoholLevel(str, enum.Enum):
    """Alcohol service level"""
    NONE = "none"
    BEER_WINE = "beer_wine"
    FULL_BAR = "full_bar"


class AVNeeds(str, enum.Enum):
    """Audio/visual requirements"""
    NONE = "none"
    BASIC_MIC = "basic_mic"
    FULL_SETUP = "full_setup"


class OfferStatus(str, enum.Enum):
    """Status of a venue offer"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


class BookingStatus(str, enum.Enum):
    """Status of a booking"""
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class BriefStatus(str, enum.Enum):
    """Status of an event brief"""
    DRAFT = "draft"
    ACTIVE = "active"
    MATCHED = "matched"
    BOOKED = "booked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Borough(str, enum.Enum):
    """NYC Boroughs"""
    MANHATTAN = "manhattan"
    BROOKLYN = "brooklyn"
    QUEENS = "queens"
    BRONX = "bronx"
    STATEN_ISLAND = "staten_island"
