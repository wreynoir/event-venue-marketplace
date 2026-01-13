"""
Venue and related models
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import Borough


class Venue(Base):
    """Venue model"""

    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic info
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    borough = Column(SQLEnum(Borough), nullable=False, index=True)
    neighborhood = Column(String, nullable=True)
    address = Column(String, nullable=False)

    # Capacity
    capacity_min = Column(Integer, nullable=False)
    capacity_max = Column(Integer, nullable=False)

    # Pricing
    base_price = Column(Float, nullable=True)  # Optional base price
    min_spend = Column(Float, nullable=True)   # Optional minimum spend

    # Features
    instant_book_enabled = Column(Boolean, default=False)
    verification_status = Column(String, default="pending")  # pending, verified, rejected

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    photos = relationship("VenuePhoto", back_populates="venue", cascade="all, delete-orphan")
    amenities = relationship("VenueAmenity", back_populates="venue", cascade="all, delete-orphan")
    pricing_packages = relationship("VenuePricing", back_populates="venue", cascade="all, delete-orphan")
    availability = relationship("VenueAvailability", back_populates="venue", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Venue(id={self.id}, name={self.name}, borough={self.borough})>"


class VenuePhoto(Base):
    """Venue photos"""

    __tablename__ = "venue_photos"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)

    url = Column(String, nullable=False)
    is_hero = Column(Boolean, default=False)  # Hero/cover image
    order = Column(Integer, default=0)  # Display order

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    venue = relationship("Venue", back_populates="photos")

    def __repr__(self):
        return f"<VenuePhoto(id={self.id}, venue_id={self.venue_id}, is_hero={self.is_hero})>"


class VenueAmenity(Base):
    """Venue amenities"""

    __tablename__ = "venue_amenities"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)

    amenity_type = Column(String, nullable=False)  # wifi, parking, av_equipment, kitchen, etc.
    details = Column(Text, nullable=True)  # Additional details about the amenity

    # Relationships
    venue = relationship("Venue", back_populates="amenities")

    def __repr__(self):
        return f"<VenueAmenity(id={self.id}, type={self.amenity_type})>"


class VenuePricing(Base):
    """Venue pricing packages"""

    __tablename__ = "venue_pricing"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)

    package_name = Column(String, nullable=False)  # "Space Only", "Full Package", etc.
    base_price = Column(Float, nullable=False)
    min_spend = Column(Float, nullable=True)
    inclusions = Column(Text, nullable=True)  # What's included (JSON or comma-separated)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    venue = relationship("Venue", back_populates="pricing_packages")

    def __repr__(self):
        return f"<VenuePricing(id={self.id}, package={self.package_name}, price={self.base_price})>"


class VenueAvailability(Base):
    """Venue calendar availability sync"""

    __tablename__ = "venue_availability"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False, unique=True)

    calendar_url = Column(String, nullable=True)  # ICS calendar URL or Google Calendar link
    sync_status = Column(String, default="not_configured")  # not_configured, syncing, synced, error
    last_synced_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    venue = relationship("Venue", back_populates="availability")

    def __repr__(self):
        return f"<VenueAvailability(venue_id={self.venue_id}, status={self.sync_status})>"
