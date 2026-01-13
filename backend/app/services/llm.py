"""
LLM service for generating match explanations using Claude API
"""

import os
from typing import Dict, List
from anthropic import Anthropic

from app.models.venue import Venue
from app.models.brief import EventBrief


class MatchExplainer:
    """
    Uses Claude API to generate natural language explanations
    for why a venue matches an event brief.
    """

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)

    def generate_explanation(
        self,
        venue: Venue,
        brief: EventBrief,
        score: float,
        match_details: Dict
    ) -> str:
        """
        Generate a natural language explanation for why this venue matches.

        Returns:
            A concise explanation (3-5 bullet points) formatted as markdown.
        """
        prompt = self._build_prompt(venue, brief, score, match_details)

        try:
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Using Haiku for speed and cost
                max_tokens=500,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the text content from the response
            explanation = message.content[0].text
            return explanation

        except Exception as e:
            # Fallback to a generic explanation if API fails
            return self._generate_fallback_explanation(venue, brief, score, match_details)

    def _build_prompt(
        self,
        venue: Venue,
        brief: EventBrief,
        score: float,
        match_details: Dict
    ) -> str:
        """Build the prompt for Claude."""

        # Format event type
        event_type = brief.event_type.value.replace('_', ' ').title()

        # Format borough
        venue_borough = venue.borough.value.replace('_', ' ').title()
        pref_borough = brief.borough_pref.value.replace('_', ' ').title() if brief.borough_pref else "Any"

        prompt = f"""You are a venue matching expert. Generate a concise explanation (3-5 bullet points) for why this venue is a good match for this event.

EVENT DETAILS:
- Type: {event_type}
- Guest Count: {brief.headcount} people
- Date: {brief.date_preferred}
- Location Preference: {pref_borough}
- Budget: ${brief.budget_min or 0} - ${brief.budget_max}
- Food/Beverage: {brief.food_bev_level.value.replace('_', ' ').title()}
- Alcohol: {brief.alcohol_level.value.replace('_', ' ').title()}
- AV Needs: {brief.av_needs.value.replace('_', ' ').title()}

VENUE DETAILS:
- Name: {venue.name}
- Location: {venue_borough}, {venue.neighborhood or 'NYC'}
- Capacity: {venue.capacity_min}-{venue.capacity_max} people
- Base Price: ${venue.base_price or 'Contact for pricing'}
- Minimum Spend: ${venue.min_spend or 'N/A'}

MATCH SCORE: {score:.1f}/100

SCORING BREAKDOWN:
- Capacity Match: {match_details['capacity']['score']:.1f}/{match_details.get('capacity_weight', 30)} points
- Price Match: {match_details['price']['score']:.1f}/{match_details.get('price_weight', 25)} points
- Location Match: {match_details['location']['score']:.1f}/{match_details.get('location_weight', 20)} points
- Amenities Match: {match_details['amenities']['score']:.1f}/{match_details.get('amenities_weight', 15)} points

Generate 3-5 bullet points explaining why this venue is a good match. Focus on:
1. The strongest match aspects (highest scoring categories)
2. Specific details that make it suitable for this event type
3. Any standout features or advantages

Format as markdown bullet points. Keep each point concise (one sentence). Be enthusiastic but honest.

Example format:
- Perfect capacity for your {brief.headcount}-person {event_type.lower()}
- Excellent location in {venue_borough}, matching your preference
- Within your budget with transparent pricing
- Great amenities for corporate events

DO NOT include a heading or title. Start directly with the bullet points."""

        return prompt

    def _generate_fallback_explanation(
        self,
        venue: Venue,
        brief: EventBrief,
        score: float,
        match_details: Dict
    ) -> str:
        """
        Generate a simple fallback explanation if the API fails.
        """
        bullets = []

        # Capacity
        if match_details['capacity']['score'] > 20:
            bullets.append(
                f"- Comfortably accommodates your {brief.headcount} guests "
                f"(capacity: {venue.capacity_min}-{venue.capacity_max})"
            )

        # Location
        if match_details['location']['score'] > 15:
            venue_borough = venue.borough.value.replace('_', ' ').title()
            bullets.append(f"- Great location in {venue_borough}")

        # Price
        if match_details['price']['score'] > 15:
            bullets.append(f"- Within your budget of ${brief.budget_max}")

        # Amenities
        if match_details['amenities']['score'] > 10:
            bullets.append("- Has the amenities you need for your event")

        # Overall score
        if score >= 80:
            bullets.append("- Excellent overall match for your requirements")
        elif score >= 60:
            bullets.append("- Strong match for your event needs")

        return "\n".join(bullets) if bullets else "- Matches your event requirements"
