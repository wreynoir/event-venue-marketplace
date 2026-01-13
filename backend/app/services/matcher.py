"""
Venue matching service - Rules-based scoring algorithm
"""

from typing import List, Dict, Tuple
from datetime import datetime, date
from sqlalchemy.orm import Session

from app.models.venue import Venue
from app.models.brief import EventBrief


class VenueMatcher:
    """
    Rules-based venue matching with scoring algorithm.
    Scores venues based on how well they match the event brief requirements.
    """

    # Scoring weights
    WEIGHT_CAPACITY = 30
    WEIGHT_PRICE = 25
    WEIGHT_LOCATION = 20
    WEIGHT_AMENITIES = 15
    WEIGHT_AVAILABILITY = 10

    def __init__(self, db: Session):
        self.db = db

    def find_matches(self, brief: EventBrief, limit: int = 10) -> List[Tuple[Venue, float, Dict]]:
        """
        Find and score venues that match the brief.

        Returns:
            List of tuples: (venue, score, match_details)
            - venue: The Venue object
            - score: Float between 0-100
            - match_details: Dict with scoring breakdown
        """
        # Get all verified venues
        venues = self.db.query(Venue).filter(
            Venue.verification_status == "verified"
        ).all()

        # Score each venue
        scored_venues = []
        for venue in venues:
            score, details = self._score_venue(venue, brief)
            if score > 0:  # Only include venues with some match
                scored_venues.append((venue, score, details))

        # Sort by score (highest first)
        scored_venues.sort(key=lambda x: x[1], reverse=True)

        # Return top matches
        return scored_venues[:limit]

    def _score_venue(self, venue: Venue, brief: EventBrief) -> Tuple[float, Dict]:
        """
        Score a single venue against a brief.

        Returns:
            Tuple of (total_score, details_dict)
        """
        details = {}

        # 1. Capacity Score (30 points)
        capacity_score = self._score_capacity(venue, brief)
        details['capacity'] = {
            'score': capacity_score,
            'venue_range': f"{venue.capacity_min}-{venue.capacity_max}",
            'required': brief.headcount,
        }

        # 2. Price Score (25 points)
        price_score = self._score_price(venue, brief)
        details['price'] = {
            'score': price_score,
            'venue_base': venue.base_price,
            'venue_min_spend': venue.min_spend,
            'budget': brief.budget_max,
        }

        # 3. Location Score (20 points)
        location_score = self._score_location(venue, brief)
        details['location'] = {
            'score': location_score,
            'venue_borough': venue.borough.value,
            'preferred_borough': brief.borough_pref.value if brief.borough_pref else None,
        }

        # 4. Amenities Score (15 points)
        amenities_score = self._score_amenities(venue, brief)
        details['amenities'] = {
            'score': amenities_score,
            'food_bev_match': brief.food_bev_level.value,
            'alcohol_match': brief.alcohol_level.value,
            'av_match': brief.av_needs.value,
        }

        # 5. Availability Score (10 points)
        # For MVP, we'll give full points (no calendar integration yet)
        availability_score = self.WEIGHT_AVAILABILITY
        details['availability'] = {
            'score': availability_score,
            'note': 'Calendar sync not implemented in MVP',
        }

        # Calculate total score
        total_score = (
            capacity_score +
            price_score +
            location_score +
            amenities_score +
            availability_score
        )

        details['total'] = total_score
        details['max_possible'] = 100

        return total_score, details

    def _score_capacity(self, venue: Venue, brief: EventBrief) -> float:
        """
        Score based on capacity match.
        - Perfect match (within range): 100% of weight
        - Close match (within 20%): 70% of weight
        - Too small: 0%
        - Too large (but usable): 50% of weight
        """
        headcount = brief.headcount

        # Perfect match - within venue's stated range
        if venue.capacity_min <= headcount <= venue.capacity_max:
            return self.WEIGHT_CAPACITY

        # Too small - can't accommodate
        if headcount > venue.capacity_max:
            # Check if it's close (within 20%)
            if headcount <= venue.capacity_max * 1.2:
                return self.WEIGHT_CAPACITY * 0.7
            return 0

        # Too large - venue can handle it but might feel empty
        if headcount < venue.capacity_min:
            # Check if it's close (within 20%)
            if headcount >= venue.capacity_min * 0.8:
                return self.WEIGHT_CAPACITY * 0.7
            return self.WEIGHT_CAPACITY * 0.5

        return 0

    def _score_price(self, venue: Venue, brief: EventBrief) -> float:
        """
        Score based on price match.
        Uses venue's base_price or min_spend if available.
        """
        # If we don't have pricing info, give neutral score
        if not venue.base_price and not venue.min_spend:
            return self.WEIGHT_PRICE * 0.5

        # Use the higher of base_price or min_spend as the cost estimate
        venue_cost = max(venue.base_price or 0, venue.min_spend or 0)

        # Within budget
        if venue_cost <= brief.budget_max:
            # Check if it's within min-max range
            if brief.budget_min and venue_cost >= brief.budget_min:
                return self.WEIGHT_PRICE  # Perfect match
            elif not brief.budget_min:
                return self.WEIGHT_PRICE  # Good match (no minimum specified)
            else:
                return self.WEIGHT_PRICE * 0.7  # Below minimum but affordable

        # Slightly over budget (within 10%)
        if venue_cost <= brief.budget_max * 1.1:
            return self.WEIGHT_PRICE * 0.6

        # Too expensive
        return 0

    def _score_location(self, venue: Venue, brief: EventBrief) -> float:
        """
        Score based on location match.
        """
        # No preference specified - all locations are equal
        if not brief.borough_pref:
            return self.WEIGHT_LOCATION

        # Exact borough match
        if venue.borough == brief.borough_pref:
            # Check neighborhood match if specified
            if brief.neighborhood_pref and venue.neighborhood:
                if brief.neighborhood_pref.lower() in venue.neighborhood.lower():
                    return self.WEIGHT_LOCATION  # Perfect match
                return self.WEIGHT_LOCATION * 0.9  # Borough match, different neighborhood
            return self.WEIGHT_LOCATION  # Borough match, no neighborhood pref

        # Different borough - lower score
        # Manhattan <-> Brooklyn are close, give partial points
        close_boroughs = {
            'manhattan': ['brooklyn'],
            'brooklyn': ['manhattan'],
        }

        venue_borough = venue.borough.value
        pref_borough = brief.borough_pref.value

        if venue_borough in close_boroughs.get(pref_borough, []):
            return self.WEIGHT_LOCATION * 0.5

        # Different borough, not adjacent
        return self.WEIGHT_LOCATION * 0.3

    def _score_amenities(self, venue: Venue, brief: EventBrief) -> float:
        """
        Score based on amenities match.
        Checks if venue can provide required food/beverage, alcohol, and AV.
        """
        score = 0
        max_score = self.WEIGHT_AMENITIES

        # For MVP, we'll give partial scores based on requirements
        # In production, you'd check venue.amenities for specific capabilities

        # Food/Beverage (5 points)
        if brief.food_bev_level.value == 'none':
            score += max_score * 0.33  # No requirement, easy match
        elif brief.food_bev_level.value == 'light_bites':
            score += max_score * 0.25  # Assume most venues can do light bites
        elif brief.food_bev_level.value == 'full_catering':
            score += max_score * 0.20  # Full catering is harder, lower score

        # Alcohol (5 points)
        if brief.alcohol_level.value == 'none':
            score += max_score * 0.33  # No requirement, easy match
        elif brief.alcohol_level.value == 'beer_wine':
            score += max_score * 0.25  # Most venues can do beer/wine
        elif brief.alcohol_level.value == 'full_bar':
            score += max_score * 0.20  # Full bar is harder, lower score

        # AV Needs (5 points)
        if brief.av_needs.value == 'none':
            score += max_score * 0.34  # No requirement, easy match
        elif brief.av_needs.value == 'basic_mic':
            score += max_score * 0.25  # Basic AV is common
        elif brief.av_needs.value == 'full_setup':
            score += max_score * 0.20  # Full AV setup is harder, lower score

        return score
