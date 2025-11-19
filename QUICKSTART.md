# 🚀 Quick Start Guide

## Get Running in 10 Minutes

### Step 1: Get API Keys (5 minutes)

#### Kakao Developers
1. Go to https://developers.kakao.com
2. Sign up / Log in
3. Click "My Application" → "Add an application"
4. Enter app name: "Travel Planner"
5. Go to "App Settings" → "Platform" → "Web"
   - Add: `http://localhost:3000`
6. Go to "App Keys"
   - Copy **JavaScript Key**
   - Copy **REST API Key**
7. Go to "Product Settings" → "Kakao Login"
   - Activate Kakao Login
   - Redirect URI: `http://localhost:3000/api/auth/callback/kakao`

#### Google OAuth
1. Go to https://console.cloud.google.com
2. Create new project: "Travel Planner"
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Application type: **Web application**
6. Authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback/google`
7. Copy **Client ID** and **Client Secret**

#### ExchangeRate-API
1. Go to https://www.exchangerate-api.com
2. Sign up (free)
3. Copy your **API Key** from dashboard

### Step 2: Clone & Configure (2 minutes)

```bash
# Clone repository
git clone <your-repo-url>
cd travel-planner

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# Use your favorite editor (nano, vim, VS Code, etc.)
nano .env
```

**Required values in .env**:
```bash
# Replace these with your actual keys:
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
KAKAO_REST_API_KEY=your_kakao_rest_key_here
NEXT_PUBLIC_KAKAO_JS_KEY=your_kakao_js_key_here
EXCHANGE_RATE_API_KEY=your_exchange_rate_key_here

# These can stay as-is for local development:
JWT_SECRET_KEY=super-secret-jwt-key-change-me-in-production
NEXTAUTH_SECRET=super-secret-nextauth-change-me-in-production
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/traveldb
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
```

### Step 3: Start Everything (3 minutes)

```bash
# Start all services with Docker
docker compose up --build

# Wait for:
# ✅ Database: "database system is ready to accept connections"
# ✅ Backend: "Uvicorn running on http://0.0.0.0:8000"
# ✅ Frontend: "ready - started server on 0.0.0.0:3000"
```

### Step 4: Verify It Works

Open your browser:

1. **Frontend**: http://localhost:3000
   - Should see login page
   
2. **Backend API Docs**: http://localhost:8000/docs
   - Should see Swagger UI with all endpoints

3. **Test Login**:
   - Click "Sign in with Google"
   - Complete Google OAuth flow
   - Should redirect to dashboard

4. **Test API**:
   - Go to http://localhost:8000/docs
   - Try `/health` endpoint
   - Should return `{"status": "healthy"}`

### Step 5: Create Your First Itinerary

1. After logging in, click "New Itinerary"
2. Fill in:
   - Title: "Seoul Trip"
   - Start Date: (any future date)
   - End Date: (after start date)
3. Click "Create"
4. You should see your itinerary in the dashboard

### Step 6: Add a Place

1. Open your itinerary
2. The map should load (centered on Seoul)
3. Use the search bar to find "Myeongdong"
4. Click a search result
5. A marker should appear on the map
6. The place is now saved to your itinerary

---

## Troubleshooting

### "Cannot connect to database"
```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# If not, restart
docker compose down
docker compose up --build
```

### "Kakao Maps not loading"
- Check browser console for errors
- Verify `NEXT_PUBLIC_KAKAO_JS_KEY` in .env
- Make sure `http://localhost:3000` is registered in Kakao Developers

### "Google OAuth fails"
- Verify redirect URI exactly matches: `http://localhost:3000/api/auth/callback/google`
- Check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in .env
- Ensure Google+ API is enabled in Google Cloud Console

### "Port already in use"
```bash
# Stop all containers
docker compose down

# Check what's using the port
# On Mac/Linux:
lsof -i :3000
lsof -i :8000

# On Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill the process or change ports in docker-compose.yml
```

---

## Next Steps

1. **Read the full roadmap**: See `ROADMAP.md`
2. **Check the feature checklist**: See `CHECKLIST.md`
3. **Explore the API**: http://localhost:8000/docs
4. **Start developing**: Follow the roadmap phases

---

## Development Commands

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Stop services
docker compose down

# Rebuild after code changes
docker compose up --build

# Run backend tests
docker exec travel-backend pytest

# Run frontend tests
docker exec travel-frontend npm test

# Access database
docker exec -it travel-db psql -U postgres -d traveldb
```

---

## Project Structure

```
travel-planner/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── routers/     # API endpoints
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── main.py      # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/            # Next.js application
│   ├── app/            # Pages (App Router)
│   ├── components/     # React components
│   ├── i18n/          # Translations
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml  # Local development stack
├── .env               # Environment variables (create this)
├── .env.example       # Template
├── README.md          # Project overview
├── ROADMAP.md         # Development roadmap
├── CHECKLIST.md       # Feature checklist
└── QUICKSTART.md      # This file
```

---

## Support

- **Issues**: Create an issue on GitHub
- **Email**: support@your-domain.com
- **Documentation**: See README.md and ROADMAP.md

---

**Ready to build something amazing! 🚀**
