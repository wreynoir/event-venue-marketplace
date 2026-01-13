"""
Matching API endpoints - Generate and retrieve venue matches for briefs
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.base import get_db
from app.models.user import User
from app.models.brief import EventBrief
from app.models.offer import MatchResult
from app.models.venue import Venue
from app.services.matcher import VenueMatcher
from app.services.llm import MatchExplainer

router = APIRouter(prefix="/matching", tags=["matching"])


@router.post("/briefs/{brief_id}/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_matches(
    brief_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate venue matches for a brief.
    This runs the matching algorithm and stores results in the database.
    """
    # Get the brief
    brief = db.query(EventBrief).filter(EventBrief.id == brief_id).first()
    if not brief:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brief not found"
        )

    # Check permissions - only the brief owner or venue owners can trigger matching
    if brief.host_id != current_user.id and not current_user.is_venue_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to generate matches for this brief"
        )

    # Check if matches already exist
    existing_matches = db.query(MatchResult).filter(
        MatchResult.brief_id == brief_id
    ).count()

    if existing_matches > 0:
        return {
            "message": "Matches already exist for this brief",
            "brief_id": brief_id,
            "match_count": existing_matches
        }

    # Run matching in background
    background_tasks.add_task(
        _generate_and_store_matches,
        db,
        brief
    )

    return {
        "message": "Matching started - results will be available shortly",
        "brief_id": brief_id
    }


@router.get("/briefs/{brief_id}/matches")
async def get_matches(
    brief_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get match results for a brief.
    Returns venues ranked by match score with explanations.
    """
    # Get the brief
    brief = db.query(EventBrief).filter(EventBrief.id == brief_id).first()
    if not brief:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brief not found"
        )

    # Check permissions - only the brief owner can view matches
    if brief.host_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view matches for this brief"
        )

    # Get matches (ordered by rank)
    matches = db.query(MatchResult).filter(
        MatchResult.brief_id == brief_id
    ).order_by(MatchResult.rank).all()

    if not matches:
        # No matches yet - trigger generation
        return {
            "brief_id": brief_id,
            "matches": [],
            "message": "No matches found. Generating matches..."
        }

    # Format response with venue details
    results = []
    for match in matches:
        venue = db.query(Venue).filter(Venue.id == match.venue_id).first()
        if venue:
            results.append({
                "match_id": match.id,
                "rank": match.rank,
                "score": match.score,
                "explanation": match.explanation,
                "venue": {
                    "id": venue.id,
                    "name": venue.name,
                    "description": venue.description,
                    "borough": venue.borough.value,
                    "neighborhood": venue.neighborhood,
                    "address": venue.address,
                    "capacity_min": venue.capacity_min,
                    "capacity_max": venue.capacity_max,
                    "base_price": venue.base_price,
                    "min_spend": venue.min_spend,
                },
                "created_at": match.created_at
            })

    return {
        "brief_id": brief_id,
        "match_count": len(results),
        "matches": results
    }


def _generate_and_store_matches(db: Session, brief: EventBrief):
    """
    Background task to generate matches and store them in the database.
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
        print(f"Generated {len(scored_venues)} matches for brief {brief.id}")

    except Exception as e:
        db.rollback()
        print(f"Error generating matches: {e}")
        raise
