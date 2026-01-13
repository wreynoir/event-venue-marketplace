"""
Offer and Booking models
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum as SQLEnum
from app.db.base import Base
from app.models.enums import OfferStatus, BookingStatus


class MatchResult(Base):
    """AI matching results for brief-venue pairs"""

    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    brief_id = Column(Integer, ForeignKey("event_briefs.id"), nullable=False, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False, index=True)

    score = Column(Float, nullable=False)  # Matching score (0-100)
    explanation = Column(Text, nullable=True)  # AI-generated explanation bullets
    rank = Column(Integer, nullable=False)  # Rank in the match results (1, 2, 3...)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f"<MatchResult(brief_id={self.brief_id}, venue_id={self.venue_id}, score={self.score}, rank={self.rank})>"


class Offer(Base):
    """Venue offers to event briefs"""

    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    brief_id = Column(Integer, ForeignKey("event_briefs.id"), nullable=False, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False, index=True)

    # Offer details
    package_name = Column(String, nullable=False)  # Package offered
    price = Column(Float, nullable=False)
    min_spend = Column(Float, nullable=True)
    included_items = Column(Text, nullable=True)  # What's included (JSON or list)
    terms = Column(Text, nullable=True)  # Terms and conditions

    # Expiration
    expires_at = Column(DateTime, nullable=True)

    # Status
    status = Column(SQLEnum(OfferStatus), default=OfferStatus.PENDING, index=True)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Offer(id={self.id}, brief_id={self.brief_id}, venue_id={self.venue_id}, status={self.status})>"


class Booking(Base):
    """Event bookings"""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    brief_id = Column(Integer, ForeignKey("event_briefs.id"), nullable=False, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False, index=True)

    # Payment details
    deposit_amount = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=False)
    stripe_payment_intent_id = Column(String, nullable=True, unique=True)

    # Status
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.REQUESTED, index=True)

    # Timestamps
    confirmed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Booking(id={self.id}, brief_id={self.brief_id}, status={self.status})>"


class Review(Base):
    """Two-way reviews (host <-> venue)"""

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who wrote the review
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who is being reviewed

    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f"<Review(id={self.id}, booking_id={self.booking_id}, rating={self.rating})>"


class MessageRelayLog(Base):
    """Log of email/SMS notifications sent (for MVP mock tracking)"""

    __tablename__ = "message_relay_logs"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    channel = Column(String, nullable=False)  # email, sms
    message_body = Column(Text, nullable=False)

    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f"<MessageRelayLog(id={self.id}, channel={self.channel}, sent_at={self.sent_at})>"
