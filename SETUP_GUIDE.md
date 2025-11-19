# 🚀 Complete Setup Guide

## Prerequisites

Before you begin, ensure you have:

- **Docker Desktop** 24.x+ installed
- **Node.js** 18.x+ installed (for local development)
- **Python** 3.11+ installed (for local development)
- **Git** installed
- A **Google account** (for OAuth)
- A **Kakao account** (for Maps API)

---

## Step 1: Get API Keys (30 minutes)

### 1.1 Kakao Developers

**Purpose**: Map rendering and place search

1. Visit https://developers.kakao.com
2. Click "시작하기" (Get Started) or "로그인" (Login)
3. Sign up or log in with your Kakao account
4. Click "내 애플리케이션" (My Applications)
5. Click "애플리케이션 추가하기" (Add Application)
6. Enter:
   - App Name: `Travel Planner`
   - Company Name: (your name or company)
7. Click "저장" (Save)

**Get JavaScript Key**:
1. In your app dashboard, go to "앱 키" (App Keys)
2. Copy the **JavaScript 키** (JavaScript Key)
3. Save it as: `NEXT_PUBLIC_KAKAO_JS_KEY`

**Get REST API Key**:
1. In the same "앱 키" section
2. Copy the **REST API 키** (REST API Key)
3. Save it as: `KAKAO_REST_API_KEY`

**Configure Platform**:
1. Go to "플랫폼" (Platform) in left menu
2. Click "Web 플랫폼 등록" (Register Web Platform)
3. Enter site domain: `http://localhost:3000`
4. Click "저장" (Save)

**Enable APIs**:
1. Go to "제품 설정" (Product Settings) → "Kakao 로그인" (Kakao Login)
2. Click "활성화 설정" (Activation Settings) → ON
3. Redirect URI: `http://localhost:3000/api/auth/callback/kakao`
4. Go to "Local" in left menu
5. Ensure it's activated

---

### 1.2 Google OAuth

**Purpose**: User authentication

1. Visit https://console.cloud.google.com
2. Click "Select a project" → "New Project"
3. Enter:
   - Project name: `Travel Planner`
   - Location: (leave default)
4. Click "Create"

**Enable Google+ API**:
1. In the left menu, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and click "Enable"

**Create OAuth Credentials**:
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: `Travel Planner`
   - User support email: (your email)
   - Developer contact: (your email)
   - Click "Save and Continue"
   - Scopes: Skip (click "Save and Continue")
   - Test users: Add your email
   - Click "Save and Continue"
4. Back to "Create OAuth Client ID":
   - Application type: **Web application**
   - Name: `Travel Planner Web`
   - Authorized JavaScript origins: `http://localhost:3000`
   - Authorized redirect URIs: `http://localhost:3000/api/auth/callback/google`
5. Click "Create"
6. Copy **Client ID** → Save as: `GOOGLE_CLIENT_ID`
7. Copy **Client Secret** → Save as: `GOOGLE_CLIENT_SECRET`

---

### 1.3 ExchangeRate-API

**Purpose**: Currency conversion

1. Visit https://www.exchangerate-api.com
2. Click "Get Free Key"
3. Enter your email address
4. Check your email for the API key
5. Copy the key → Save as: `EXCHANGE_RATE_API_KEY`

**Free Tier Limits**:
- 1,500 requests per month
- Updates once per day
- Sufficient for MVP

---

### 1.4 Naver Developers (Optional - Phase 2)

**Purpose**: Fallback place search

1. Visit https://developers.naver.com
2. Sign up or log in
3. Click "Application" → "Register Application"
4. Enter:
   - Application Name: `Travel Planner`
   - APIs: Select "Maps" and "Search"
5. Copy **Client ID** → Save as: `NAVER_CLIENT_ID`
6. Copy **Client Secret** → Save as: `NAVER_CLIENT_SECRET`

---

## Step 2: Clone Repository (2 minutes)

```bash
# Clone the repository
git clone <your-repository-url>
cd travel-planner

# Verify structure
ls -la
# You should see: backend/, frontend/, docker-compose.yml, etc.
```

---

## Step 3: Configure Environment (5 minutes)

### 3.1 Create .env File

```bash
# Copy the template
cp .env.example .env

# Open in your editor
nano .env
# or
code .env
# or
vim .env
```

### 3.2 Fill in Your API Keys

Replace ALL `YOUR_..._HERE` placeholders with your actual keys:

```bash
# Backend
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/traveldb
JWT_SECRET_KEY=super-secret-jwt-key-change-me-in-production
GOOGLE_CLIENT_ID=<paste your Google Client ID>
GOOGLE_CLIENT_SECRET=<paste your Google Client Secret>
KAKAO_REST_API_KEY=<paste your Kakao REST API Key>
EXCHANGE_RATE_API_KEY=<paste your ExchangeRate API Key>

# Frontend
NEXT_PUBLIC_KAKAO_JS_KEY=<paste your Kakao JavaScript Key>
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=super-secret-nextauth-change-me-in-production
```

**Important**: 
- Do NOT add quotes around the values
- Do NOT commit .env to Git (it's in .gitignore)
- Keep your API keys secret

---

## Step 4: Start the Application (3 minutes)

### 4.1 Start All Services

```bash
# Build and start all containers
docker compose up --build

# This will:
# 1. Pull PostgreSQL image
# 2. Build backend image
# 3. Build frontend image
# 4. Start all services
```

### 4.2 Wait for Services to Start

Watch the logs for these messages:

```
✅ travel-db      | database system is ready to accept connections
✅ travel-backend | Uvicorn running on http://0.0.0.0:8000
✅ travel-frontend| ready - started server on 0.0.0.0:3000
```

This usually takes 2-3 minutes on first run.

---

## Step 5: Verify Installation (5 minutes)

### 5.1 Check Backend

1. Open browser: http://localhost:8000
   - Should see: `{"message": "Travel Planner API", "docs": "/docs"}`

2. Open API docs: http://localhost:8000/docs
   - Should see Swagger UI with all endpoints

3. Test health endpoint:
   - Click on `/health` → "Try it out" → "Execute"
   - Should return: `{"status": "healthy"}`

### 5.2 Check Frontend

1. Open browser: http://localhost:3000
   - Should redirect to login page

2. Check for errors:
   - Open browser console (F12)
   - Should see no errors

### 5.3 Check Database

```bash
# Connect to database
docker exec -it travel-db psql -U postgres -d traveldb

# List tables
\dt

# Should see:
# - users
# - itineraries
# - itinerary_items
# - budgets

# Exit
\q
```

---

## Step 6: Test Core Features (10 minutes)

### 6.1 Test Login

1. Go to http://localhost:3000
2. Click "Sign in with Google"
3. Complete Google OAuth flow
4. Should redirect to dashboard

**Troubleshooting**:
- If OAuth fails, check:
  - `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in .env
  - Redirect URI in Google Console matches exactly
  - Google+ API is enabled

### 6.2 Test Itinerary Creation

1. On dashboard, click "New Itinerary"
2. Fill in:
   - Title: "Seoul Trip"
   - Start Date: (any future date)
   - End Date: (after start date)
3. Click "Create"
4. Should redirect to itinerary detail page

### 6.3 Test Map

1. On itinerary detail page
2. Map should load centered on Seoul
3. Check browser console for errors

**Troubleshooting**:
- If map doesn't load:
  - Check `NEXT_PUBLIC_KAKAO_JS_KEY` in .env
  - Verify domain is registered in Kakao Developers
  - Check browser console for specific error

### 6.4 Test Place Search

1. Open browser console (F12)
2. Run this command:
```javascript
fetch('http://localhost:8000/api/v1/search/places?q=restaurant&latitude=37.5665&longitude=126.9780&limit=5')
  .then(r => r.json())
  .then(console.log)
```
3. Should see array of places with names, addresses, coordinates

### 6.5 Test Budget

1. On itinerary detail page
2. Scroll to Budget section
3. Add an expense:
   - Category: "food"
   - Amount: 50
   - Currency: USD
   - Date: (today)
4. Click "Add budget entry"
5. Should appear in list with total

### 6.6 Test Currency Converter

1. On itinerary detail page
2. Scroll to Currency Converter
3. Enter amount: 100
4. Select target currency: KRW
5. Should show converted amount

---

## Step 7: Development Workflow

### 7.1 View Logs

```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend

# Database only
docker compose logs -f db
```

### 7.2 Restart Services

```bash
# Restart all
docker compose restart

# Restart backend only
docker compose restart backend

# Restart frontend only
docker compose restart frontend
```

### 7.3 Stop Services

```bash
# Stop all (keeps data)
docker compose stop

# Stop and remove containers (keeps data)
docker compose down

# Stop and remove everything including data
docker compose down -v
```

### 7.4 Rebuild After Code Changes

```bash
# Rebuild and restart
docker compose up --build

# Rebuild specific service
docker compose up --build backend
```

---

## Step 8: Common Issues & Solutions

### Issue 1: Port Already in Use

**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**:
```bash
# Find what's using the port
# On Mac/Linux:
lsof -i :3000

# On Windows:
netstat -ano | findstr :3000

# Kill the process or change port in docker-compose.yml
```

### Issue 2: Database Connection Failed

**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# If not, restart
docker compose down
docker compose up --build
```

### Issue 3: Kakao Maps Not Loading

**Error**: Console shows "Kakao is not defined"

**Solution**:
1. Check `NEXT_PUBLIC_KAKAO_JS_KEY` in .env
2. Verify domain registered in Kakao Developers
3. Clear browser cache
4. Restart frontend: `docker compose restart frontend`

### Issue 4: Google OAuth Fails

**Error**: "redirect_uri_mismatch"

**Solution**:
1. Go to Google Cloud Console
2. Check Authorized redirect URIs
3. Must be exactly: `http://localhost:3000/api/auth/callback/google`
4. No trailing slash
5. Save and wait 5 minutes for changes to propagate

### Issue 5: Exchange Rate API Error

**Error**: 502 Bad Gateway

**Solution**:
1. Check `EXCHANGE_RATE_API_KEY` in .env
2. Verify API key at https://www.exchangerate-api.com
3. Check if you've exceeded free tier limit (1,500/month)

---

## Step 9: Next Steps

### For Development

1. **Read the Roadmap**: See `ROADMAP.md` for 12-week plan
2. **Check Features**: See `CHECKLIST.md` for implementation status
3. **API Reference**: See `API_REFERENCE.md` for all endpoints
4. **Start Coding**: Follow Phase 1 in roadmap

### For Testing

```bash
# Run backend tests
docker exec travel-backend pytest

# Run frontend tests
docker exec travel-frontend npm test

# Run with coverage
docker exec travel-backend pytest --cov=app
```

### For Deployment

1. **Week 11**: Follow deployment section in `ROADMAP.md`
2. **AWS Setup**: Configure RDS, ECS, ECR
3. **CI/CD**: Set up GitHub Actions
4. **Monitoring**: Configure CloudWatch, Sentry

---

## Step 10: Getting Help

### Documentation

- **README.md**: Project overview
- **ROADMAP.md**: Development plan
- **CHECKLIST.md**: Feature checklist
- **QUICKSTART.md**: 10-minute guide
- **API_REFERENCE.md**: API documentation
- **PROJECT_SUMMARY.md**: High-level overview
- **VERIFICATION_REPORT.md**: Verification details
- **SETUP_GUIDE.md**: This file

### Official Docs

- Kakao Maps: https://apis.map.kakao.com/web/documentation/
- Kakao Local: https://developers.kakao.com/docs/latest/en/local/dev-guide
- Next.js: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com
- PostgreSQL: https://www.postgresql.org/docs/

### Support

- **GitHub Issues**: Create an issue for bugs
- **Email**: support@your-domain.com
- **Discord**: (create a server for community)

---

## Appendix: Environment Variables Reference

### Backend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql+asyncpg://...` |
| `JWT_SECRET_KEY` | Yes | Secret for JWT signing | Random string |
| `GOOGLE_CLIENT_ID` | Yes | Google OAuth client ID | From Google Console |
| `GOOGLE_CLIENT_SECRET` | Yes | Google OAuth secret | From Google Console |
| `KAKAO_REST_API_KEY` | Yes | Kakao REST API key | From Kakao Developers |
| `EXCHANGE_RATE_API_KEY` | Yes | ExchangeRate API key | From ExchangeRate-API |
| `NAVER_CLIENT_ID` | No | Naver API client ID | From Naver Developers |
| `NAVER_CLIENT_SECRET` | No | Naver API secret | From Naver Developers |

### Frontend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_KAKAO_JS_KEY` | Yes | Kakao JavaScript key | From Kakao Developers |
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL | `http://localhost:8000` |
| `NEXTAUTH_URL` | Yes | Frontend URL | `http://localhost:3000` |
| `NEXTAUTH_SECRET` | Yes | NextAuth secret | Random string |
| `GOOGLE_CLIENT_ID` | Yes | Same as backend | From Google Console |
| `GOOGLE_CLIENT_SECRET` | Yes | Same as backend | From Google Console |

---

## Success Checklist

Before proceeding to development, verify:

- [ ] All API keys obtained
- [ ] .env file configured
- [ ] Docker containers running
- [ ] Backend accessible at :8000
- [ ] Frontend accessible at :3000
- [ ] Database tables created
- [ ] Google login works
- [ ] Can create itinerary
- [ ] Map displays correctly
- [ ] Place search returns results
- [ ] Budget tracking works
- [ ] Currency conversion works
- [ ] No errors in logs
- [ ] All documentation read

---

**Congratulations! Your development environment is ready! 🎉**

Proceed to `ROADMAP.md` to start Phase 1 development.
