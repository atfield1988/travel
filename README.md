# Travel Planner for Foreign Visitors to Korea

A mobile-first web platform helping foreign travelers navigate Korea with accurate maps, real-time transit info, and itinerary planning.

## Tech Stack

- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python 3.11) + SQLAlchemy 2.0
- **Database**: PostgreSQL 15
- **Maps**: Kakao Maps API (primary) + Naver Maps (fallback)
- **Auth**: NextAuth.js (Google OAuth)
- **Deployment**: Docker + AWS (ECS, RDS, CloudFront)

## Quick Start

### Prerequisites

- Docker Desktop 24.x+
- Node.js 18.x+
- Python 3.11+
- API Keys (see below)

### Required API Keys

1. **Kakao Developers** (https://developers.kakao.com)
   - JavaScript Key (for map rendering)
   - REST API Key (for place search)

2. **Google OAuth** (https://console.cloud.google.com)
   - Client ID
   - Client Secret

3. **ExchangeRate-API** (https://www.exchangerate-api.com)
   - API Key (free tier: 1,500 requests/month)

4. **Naver Developers** (https://developers.naver.com) - Optional
   - Client ID
   - Client Secret

### Setup

```bash
# 1. Clone repository
git clone <your-repo-url>
cd travel-planner

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env with your real API keys
nano .env  # or use your preferred editor

# 4. Start all services
docker compose up --build

# 5. Open browser
# Frontend: http://localhost:3000
# Backend API docs: http://localhost:8000/docs
```

### First Run

1. Navigate to http://localhost:3000
2. Click "Sign in with Google"
3. Create your first itinerary
4. Add places using the map search
5. Track your budget and convert currencies

## Project Structure

```
travel-planner/
├── backend/           # FastAPI application
├── frontend/          # Next.js application
├── docker-compose.yml # Local development stack
└── .env              # Environment variables (create from .env.example)
```

## Development

```bash
# Run backend tests
docker exec travel-backend pytest

# Run frontend tests
docker exec travel-frontend npm test

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Rebuild after code changes
docker compose up --build
```

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## License

MIT
