"""
Event Brief model
"""

from datetime import datetime, timezone, date
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Date, DateTime, ForeignKey, Enum as SQLEnum
from app.db.base import Base
from app.models.enums import EventType, FoodBevLevel, AlcoholLevel, AVNeeds, BriefStatus, Borough


class EventBrief(Base):
    """Event brief submitted by hosts"""

    __tablename__ = "event_briefs"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Event details
    event_type = Column(SQLEnum(EventType), nullable=False, index=True)
    headcount = Column(Integer, nullable=False)

    # Date preferences
    date_preferred = Column(Date, nullable=False, index=True)
    date_flexible = Column(Boolean, default=False)

    # Location preferences
    borough_pref = Column(SQLEnum(Borough), nullable=True, index=True)
    neighborhood_pref = Column(String, nullable=True)

    # Budget
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=False)

    # Requirements
    food_bev_level = Column(SQLEnum(FoodBevLevel), default=FoodBevLevel.NONE)
    alcohol_level = Column(SQLEnum(AlcoholLevel), default=AlcoholLevel.NONE)
    av_needs = Column(SQLEnum(AVNeeds), default=AVNeeds.NONE)
    accessibility_needs = Column(Text, nullable=True)
    vibe = Column(String, nullable=True)  # casual, formal, creative, etc.

    # Additional notes
    notes = Column(Text, nullable=True)

    # Status
    status = Column(SQLEnum(BriefStatus), default=BriefStatus.ACTIVE, index=True)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<EventBrief(id={self.id}, type={self.event_type}, headcount={self.headcount}, status={self.status})>"
