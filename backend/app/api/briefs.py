"""
Event Brief API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.base import get_db
from app.models.user import User
from app.models.brief import EventBrief
from app.schemas.brief import (
    EventBriefCreate,
    EventBriefUpdate,
    EventBriefResponse,
    EventBriefListResponse,
)
from app.services.matcher import VenueMatcher
from app.services.llm import MatchExplainer
from app.models.offer import MatchResult

router = APIRouter(prefix="/briefs", tags=["briefs"])


@router.post("/", response_model=EventBriefResponse, status_code=status.HTTP_201_CREATED)
def create_brief(
    brief: EventBriefCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new event brief.
    Only hosts can create briefs.
    Automatically triggers venue matching in the background.
    """
    # Check if user is a host
    if not current_user.is_host:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only hosts can create event briefs",
        )

    # Create the brief
    db_brief = EventBrief(
        host_id=current_user.id,
        **brief.model_dump(),
    )
    db.add(db_brief)
    db.commit()
    db.refresh(db_brief)

    # Trigger matching in background
    background_tasks.add_task(_generate_matches_for_brief, db, db_brief)

    return db_brief


def _generate_matches_for_brief(db: Session, brief: EventBrief):
    """
    Background task to generate matches for a newly created brief.
    """
    try:
        # Initialize services
        matcher = VenueMatcher(db)
        explainer = MatchExplainer()

        # Find matches
        scored_venues = matcher.find_matches(brief, limit=10)

        # Store matches with explanations
        for rank, (venue, score, details) in enumerate(scored_venues, start=1):
            # Generate explanation using Claude
            try:
                explanation = explainer.generate_explanation(
                    venue, brief, score, details
                )
            except Exception as e:
                # Use fallback if Claude API fails
                print(f"Failed to generate explanation: {e}")
                explanation = explainer._generate_fallback_explanation(
                    venue, brief, score, details
                )

            # Create match result
            match_result = MatchResult(
                brief_id=brief.id,
                venue_id=venue.id,
                score=score,
                explanation=explanation,
                rank=rank
            )
            db.add(match_result)

        db.commit()
        print(f"Auto-generated {len(scored_venues)} matches for brief {brief.id}")

    except Exception as e:
        db.rollback()
        print(f"Error generating matches: {e}")


@router.get("/", response_model=EventBriefListResponse)
def list_briefs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List event briefs.
    - Hosts see their own briefs
    - Venue owners see all active briefs
    """
    query = db.query(EventBrief)

    # If user is a host, only show their briefs
    if current_user.is_host and not current_user.is_venue_owner:
        query = query.filter(EventBrief.host_id == current_user.id)
    # If user is a venue owner, show all active briefs
    elif current_user.is_venue_owner:
        # For now, show all briefs. In production, add filtering by:
        # - Location match
        # - Capacity match
        # - Active status
        pass
    else:
        # User is neither host nor venue owner
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Order by most recent first
    query = query.order_by(EventBrief.created_at.desc())

    total = query.count()
    briefs = query.offset(skip).limit(limit).all()

    return EventBriefListResponse(briefs=briefs, total=total)


@router.get("/{brief_id}", response_model=EventBriefResponse)
def get_brief(
    brief_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific event brief by ID.
    - Hosts can view their own briefs
    - Venue owners can view any active brief
    """
    brief = db.query(EventBrief).filter(EventBrief.id == brief_id).first()

    if not brief:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brief not found",
        )

    # Check permissions
    is_owner = brief.host_id == current_user.id
    is_venue_owner = current_user.is_venue_owner

    if not (is_owner or is_venue_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this brief",
        )

    return brief


@router.patch("/{brief_id}", response_model=EventBriefResponse)
def update_brief(
    brief_id: int,
    brief_update: EventBriefUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an event brief.
    Only the host who created the brief can update it.
    """
    brief = db.query(EventBrief).filter(EventBrief.id == brief_id).first()

    if not brief:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brief not found",
        )

    # Check if current user is the owner
    if brief.host_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own briefs",
        )

    # Update fields
    update_data = brief_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(brief, field, value)

    db.commit()
    db.refresh(brief)

    return brief


@router.delete("/{brief_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brief(
    brief_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete (cancel) an event brief.
    Only the host who created the brief can delete it.
    """
    brief = db.query(EventBrief).filter(EventBrief.id == brief_id).first()

    if not brief:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brief not found",
        )

    # Check if current user is the owner
    if brief.host_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own briefs",
        )

    db.delete(brief)
    db.commit()

    return None
