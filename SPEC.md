# Event Venue Marketplace

## Overview
A mobile-first two-sided marketplace connecting event hosts with NYC venues. Hosts submit event briefs, venues respond with offers, and an AI-powered matcher ranks the best fits.

## Problem Statement
Finding the right venue for corporate events in NYC is time-consuming and fragmented. Event planners need to contact multiple venues individually, explain their requirements repeatedly, and compare offers manually. Venues miss out on qualified leads because they're not discoverable or available when hosts are searching.

This platform solves both problems: hosts get AI-ranked venue matches based on their specific needs, and venues receive qualified leads with all the details they need to respond quickly.

## Target Audience
**Primary (MVP):** Corporate event planners in NYC organizing meetings, offsites, conferences, and team events (20-200 people).

**Secondary (Future):** Expanding to weddings, birthdays, and other private events with type-specific experiences.

## Core Features

### For Hosts
1. **60-Second Event Brief Wizard** - Mobile-optimized form capturing event requirements (type, date, location, headcount, budget, amenities)
2. **AI Match Results** - Ranked list of venues with "why it matches" explanations based on capacity, price, location, and amenities fit
3. **Offers Inbox** - Structured offer cards from venues with pricing, packages, inclusions, and expiration dates
4. **Request-to-Book** - Send booking requests to venues; option for instant book where enabled
5. **Reviews** - Two-way review system after event completion

### For Venues
1. **Venue Onboarding** - 15-30 minute setup: photos, location, capacity, amenities, pricing packages, availability calendar
2. **Lead Inbox** - View event briefs from qualified hosts with all requirements
3. **Offer Builder** - Respond with structured offers (space-only or packages with pricing and terms)
4. **Calendar Integration** - Sync Google Calendar or ICS feed to prevent double-bookings
5. **Reviews** - Receive and respond to host reviews

### Platform Features
1. **Hybrid AI Matching** - Rules-based scoring for speed + LLM-generated explanations for transparency
2. **Email/SMS Relay** - Notifications for new briefs, offers, and bookings
3. **Stripe Payments** - Deposit or full payment (test mode for MVP, evolving to Stripe Connect)
4. **Two-Way Reviews** - Build trust and quality through feedback
5. **NYC Geography Focus** - All boroughs with Manhattan + Brooklyn emphasis

## Nice-to-Have Features (Future)

- **Instant Booking** - Venues opt-in to auto-accept for pre-approved event types
- **Real-Time Calendar Sync** - Two-way Google Calendar integration
- **Deal Mechanics** - Time-bound promos and special offers
- **Advanced Filters** - Transit access, noise rules, insurance requirements
- **Vendor Marketplace** - Expand to catering, DJs, photographers, etc.

## UI/UX Specifications

### Design Style
- **Mobile-First**: Thumb-friendly navigation, bottom tabs, one question per screen for wizards
- **Modern & Clean**: Tailwind CSS with shadcn/ui components for consistency and accessibility
- **Fast & Responsive**: Skeleton loading states, optimistic UI updates, instant feedback
- **Professional**: Appropriate for corporate event planners while remaining approachable

### Design Inspiration
- **Airbnb** - Search and discovery patterns, host/guest dual-sided experience
- **Resy/OpenTable** - Booking flow, offer cards, availability visualization
- **Modern SaaS Apps** - Clean dashboards, card-based layouts, progressive disclosure

### Color Scheme
- Primary: Professional blue (trust, corporate)
- Accent: Warm orange/coral (energy, events)
- Neutrals: Slate grays for text and backgrounds
- Success/Error: Standard green/red for feedback

### Key UX Priorities
1. **Speed to completion** - Hosts can create a brief in <60 seconds
2. **Clarity** - AI explanations make matching transparent, not a black box
3. **Mobile optimization** - All core flows work seamlessly on mobile devices
4. **Trust signals** - Reviews, verification badges, clear pricing

## Success Criteria

**MVP is successful when:**
- Hosts can create a brief and receive ranked venue matches in <2 minutes
- Venues can respond with offers in <5 minutes
- End-to-end booking flow (brief → match → offer → payment) works without errors
- AI explanations are relevant and helpful (manual review)
- Mobile UI feels native with smooth interactions
- Seed data provides realistic testing with 15-25 NYC venues

**Product-market fit indicators (post-launch):**
- Hosts create multiple briefs (repeat usage)
- Venues respond to >50% of briefs they receive (quality leads)
- Bookings convert at >10% of offers sent
- Both sides leave reviews after events

## Constraints & Requirements

### Technical Constraints
- **Mobile-First**: Must work perfectly on iOS Safari and Android Chrome
- **Local Development**: One-command setup with Docker Compose
- **Mocked Services**: Use test mode/mocks for Stripe, SMS, email (real integrations later)
- **NYC Only**: Geography limited to 5 boroughs for MVP

### Integration Requirements
- **Stripe** - Test mode for MVP, clear upgrade path to Stripe Connect
- **Calendar** - Accept ICS URLs or Google Calendar links (basic sync for MVP)
- **Email/SMS** - Mock relay system (console logs + file storage)

### Performance Requirements
- Brief wizard loads in <1 second
- Match results appear in <3 seconds (including AI explanations)
- Mobile interactions feel instant (<100ms feedback)

### Platform Requirements
- Works on iOS Safari 14+, Android Chrome 90+
- Responsive design: 375px (mobile) to 1920px (desktop)
- PWA-ready (installable, offline-capable homepage)

## Technical Approach

### Architecture
**Monorepo** with separate frontend and backend:
- `frontend/` - Next.js 15 PWA (TypeScript, Tailwind, React 19)
- `backend/` - FastAPI + PostgreSQL (Python 3.11+, SQLAlchemy, Alembic)

### Tech Stack

**Frontend:**
- Next.js 15 (App Router) + React 19 + TypeScript 5
- Tailwind CSS 4 + shadcn/ui components
- Zustand (state management) + React Hook Form + Zod (validation)
- Framer Motion (animations) + Lucide React (icons)
- PWA configuration (manifest, service worker)

**Backend:**
- FastAPI + Pydantic v2 (validation)
- PostgreSQL 15 + SQLAlchemy 2.0 (ORM) + Alembic (migrations)
- Python-jose (JWT auth) + mock OTP for phone verification
- Anthropic Claude API (Haiku model for cost-efficient AI explanations)
- Stripe SDK (test mode)

**Development:**
- Docker Compose (Postgres local dev)
- Vitest (frontend tests) + pytest (backend tests)
- ESLint + Prettier (code quality)
- FastAPI auto-generated OpenAPI docs

### Database Schema
12 core entities: User, Venue, VenuePhoto, VenueAmenity, VenuePricing, VenueAvailability, EventBrief, MatchResult, Offer, Booking, Review, MessageRelayLog

### Key Decisions Made
1. **PWA over Native** - Faster iteration, single codebase, easy migration to Capacitor for app stores later
2. **Hybrid Matching** - Rules-based scoring for reliability + LLM explanations for UX
3. **Monorepo** - Simpler setup, shared types, single deployment
4. **Mocked Services** - Focus on core flow first, swap in real integrations later
5. **Local-First** - Get it working locally with clear instructions before deployment

### Future Migration Paths
- **App Stores**: Wrap with Capacitor (~1-2 days, zero code changes)
- **Stripe Connect**: Upgrade from simple payments to marketplace model
- **Real-Time Features**: Add WebSockets for live notifications
- **Vendor Marketplace**: Expand beyond venues to full event ecosystem

---

**Created**: January 12, 2026
**For**: Will Reynoir (@wreynoir)
**Version**: 1.0 (MVP Specification)
