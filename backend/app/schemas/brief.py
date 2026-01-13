"""
Pydantic schemas for event briefs
"""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.enums import EventType, FoodBevLevel, AlcoholLevel, AVNeeds, BriefStatus, Borough


# Request schemas
class EventBriefCreate(BaseModel):
    """Schema for creating a new event brief"""
    event_type: EventType
    headcount: int = Field(..., ge=1, description="Number of guests")
    date_preferred: date
    date_flexible: bool = False
    borough_pref: Optional[Borough] = None
    neighborhood_pref: Optional[str] = None
    budget_min: Optional[float] = Field(None, ge=0)
    budget_max: float = Field(..., ge=0)
    food_bev_level: FoodBevLevel = FoodBevLevel.NONE
    alcohol_level: AlcoholLevel = AlcoholLevel.NONE
    av_needs: AVNeeds = AVNeeds.NONE
    accessibility_needs: Optional[str] = None
    vibe: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        use_enum_values = True


class EventBriefUpdate(BaseModel):
    """Schema for updating an existing event brief"""
    event_type: Optional[EventType] = None
    headcount: Optional[int] = Field(None, ge=1)
    date_preferred: Optional[date] = None
    date_flexible: Optional[bool] = None
    borough_pref: Optional[Borough] = None
    neighborhood_pref: Optional[str] = None
    budget_min: Optional[float] = Field(None, ge=0)
    budget_max: Optional[float] = Field(None, ge=0)
    food_bev_level: Optional[FoodBevLevel] = None
    alcohol_level: Optional[AlcoholLevel] = None
    av_needs: Optional[AVNeeds] = None
    accessibility_needs: Optional[str] = None
    vibe: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[BriefStatus] = None

    class Config:
        use_enum_values = True


# Response schemas
class EventBriefResponse(BaseModel):
    """Schema for event brief response"""
    id: int
    host_id: int
    event_type: EventType
    headcount: int
    date_preferred: date
    date_flexible: bool
    borough_pref: Optional[Borough]
    neighborhood_pref: Optional[str]
    budget_min: Optional[float]
    budget_max: float
    food_bev_level: FoodBevLevel
    alcohol_level: AlcoholLevel
    av_needs: AVNeeds
    accessibility_needs: Optional[str]
    vibe: Optional[str]
    notes: Optional[str]
    status: BriefStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


class EventBriefListResponse(BaseModel):
    """Schema for list of event briefs"""
    briefs: list[EventBriefResponse]
    total: int
