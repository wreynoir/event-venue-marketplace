# Event Venue Marketplace

A mobile-first two-sided marketplace connecting event hosts with NYC venues. Hosts submit event briefs, AI ranks matches, and venues respond with structured offers.

## Project Overview

See [SPEC.md](./SPEC.md) for detailed product specifications, features, and technical approach.

**Key Features:**
- 60-second event brief wizard (mobile-optimized)
- AI-powered venue matching with transparent explanations
- Structured offer system for venues
- Request-to-book flow with Stripe payments
- Two-way reviews for trust and quality

**Target Market:** Corporate events in NYC (MVP), expanding to weddings and private events.

## Tech Stack

### Frontend
- **Framework:** Next.js 15 (App Router) + React 19
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 4 + shadcn/ui
- **State:** Zustand + React Context
- **Forms:** React Hook Form + Zod validation
- **PWA:** Mobile-first with app store migration path via Capacitor

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 15 + SQLAlchemy 2.0
- **Migrations:** Alembic
- **Auth:** JWT (python-jose) + mock OTP
- **AI:** Anthropic Claude API (Haiku for cost efficiency)
- **Payments:** Stripe (test mode)

### Development
- **Local DB:** Docker Compose (PostgreSQL)
- **Testing:** Vitest (frontend) + pytest (backend)
- **API Docs:** Auto-generated FastAPI OpenAPI/Swagger

## Prerequisites

- **Node.js:** >= 20.9.0 (recommended: v22+)
- **Python:** >= 3.11
- **Docker:** For local PostgreSQL database
- **Git:** Version control

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/wreynoir/event-venue-marketplace.git
cd event-venue-marketplace
```

### 2. Start the Database

```bash
# Start PostgreSQL with Docker Compose
docker-compose up -d

# Verify it's running
docker-compose ps
```

### 3. Set Up the Backend

```bash
cd backend

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example and fill in values)
cp .env.example .env

# Run database migrations (once implemented)
# alembic upgrade head

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/api/docs
- **API Docs (ReDoc):** http://localhost:8000/api/redoc

### 4. Set Up the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file (copy from .env.example)
cp .env.example .env.local

# Start the development server
npm run dev
```

The frontend will be available at:
- **App:** http://localhost:3000

### 5. Run Everything

**Terminal 1 - Database:**
```bash
docker-compose up
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

## Environment Variables

### Backend (.env)

See `backend/.env.example` for all required variables:
- Database connection (PostgreSQL)
- JWT secret key
- Anthropic API key (for AI matching)
- Stripe keys (test mode)
- Mock service configs (email, SMS)

### Frontend (.env.local)

See `frontend/.env.example` for required variables:
- API base URL
- Stripe publishable key

## Project Structure

```
event-venue-marketplace/
├── frontend/              # Next.js 15 PWA
│   ├── app/              # App router pages
│   ├── components/       # React components
│   ├── lib/              # Utilities, API clients, stores
│   └── public/           # Static assets
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API route handlers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── core/         # Config and utilities
│   ├── alembic/          # Database migrations
│   ├── seed_data/        # NYC venue seed data
│   └── tests/            # pytest tests
├── docker-compose.yml    # PostgreSQL setup
├── SPEC.md               # Product specifications
└── README.md             # This file
```

## Development Workflow

### Running Tests

**Frontend:**
```bash
cd frontend
npm run test
```

**Backend:**
```bash
cd backend
source venv/bin/activate
pytest
```

### Database Migrations

```bash
cd backend
source venv/bin/activate

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Seed Data

```bash
cd backend
source venv/bin/activate

# Run seed script (once implemented)
python seed_data/seed_nyc_venues.py
```

### Stripe Webhook Testing (Local)

```bash
# Install Stripe CLI: https://stripe.com/docs/stripe-cli
stripe login

# Forward webhooks to local backend
stripe listen --forward-to localhost:8000/api/webhooks/stripe
```

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs:** http://localhost:8000/api/docs
- **Alternative Docs:** http://localhost:8000/api/redoc

## Deployment

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Deploy to Vercel (manual or via GitHub integration)
```

### Backend (Railway/Render)
- Configure environment variables
- Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Connect PostgreSQL database

## Roadmap

### Phase 1: MVP (Current)
- ✅ Project scaffold and setup
- 🚧 Venue onboarding flow
- 🚧 Host brief wizard
- 🚧 AI matching engine (rules + LLM)
- 🚧 Offers system
- 🚧 Booking and payments (Stripe test mode)
- 🚧 Reviews system
- 🚧 Email/SMS relay (mocked)

### Phase 2A: App Store Launch
- Wrap with Capacitor
- Native push notifications
- Submit to Apple App Store + Google Play

### Phase 2B: Marketplace Features
- Instant booking
- Real-time calendar sync (Google Calendar two-way)
- Stripe Connect (marketplace payments)
- Contracts and cancellation policies
- Vendor marketplace (catering, DJs, etc.)

### Technical Debt
- Replace mocks with real Twilio (SMS/OTP)
- Replace mocks with real SendGrid/Resend (email)
- Add Redis for caching
- WebSockets for real-time notifications
- Image CDN for venue photos
- Rate limiting and API security
- Analytics (PostHog/Mixpanel)

## Contributing

This is a personal project by [Will Reynoir](https://github.com/wreynoir). Built with [Claude Code](https://claude.com/claude-code).

## License

MIT License - See LICENSE file for details

---

**Questions or Issues?** Open an issue on [GitHub](https://github.com/wreynoir/event-venue-marketplace/issues)
