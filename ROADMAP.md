# 🗺️ Travel Planner - Complete Development Roadmap

## Executive Summary

**Project**: Travel utility and itinerary planner for foreign visitors to Korea  
**Timeline**: 12 weeks to MVP launch  
**Tech Stack**: Next.js 14 + FastAPI + PostgreSQL  
**Business Model**: Freemium (subscription-based)

---

## 📋 Phase 0: Prerequisites & Setup (Week 0)

### Required API Keys & Accounts

#### 1. Kakao Developers Account
- **URL**: https://developers.kakao.com
- **What you need**:
  - JavaScript Key (for map rendering)
  - REST API Key (for place search)
- **Steps**:
  1. Sign up at Kakao Developers
  2. Create a new application
  3. Go to "App Settings" → "Platform" → Add Web platform
  4. Add your domain (http://localhost:3000 for dev)
  5. Go to "App Keys" → Copy JavaScript Key and REST API Key
  6. Enable "Local" API in "Product Settings"

#### 2. Google OAuth Credentials
- **URL**: https://console.cloud.google.com
- **Steps**:
  1. Create a new project
  2. Enable "Google+ API"
  3. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
  4. Application type: Web application
  5. Authorized redirect URIs: http://localhost:3000/api/auth/callback/google
  6. Copy Client ID and Client Secret

#### 3. ExchangeRate-API Key
- **URL**: https://www.exchangerate-api.com
- **Steps**:
  1. Sign up for free account
  2. Copy your API key from dashboard
  3. Free tier: 1,500 requests/month

#### 4. Naver Developers (Optional - for fallback)
- **URL**: https://developers.naver.com
- **Steps**:
  1. Register application
  2. Enable "Maps" and "Search" APIs
  3. Copy Client ID and Client Secret

### Development Environment Setup

```bash
# Install required tools
# 1. Docker Desktop (https://www.docker.com/products/docker-desktop)
# 2. Node.js 18+ (https://nodejs.org)
# 3. Python 3.11+ (https://www.python.org)
# 4. Git (https://git-scm.com)

# Verify installations
docker --version
node --version
python --version
git --version
```

---

## 🏗️ Phase 1: Project Foundation (Week 1-2)

### Week 1: Repository & Infrastructure

**Goals**:
- Set up version control
- Configure development environment
- Verify all API connections

**Tasks**:

1. **Initialize Repository**
```bash
git init
git add .
git commit -m "Initial project structure"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your real API keys
```

3. **Test Docker Setup**
```bash
docker compose up --build
# Wait for all services to start
# Backend should be at http://localhost:8000
# Frontend should be at http://localhost:3000
```

4. **Verify API Connections**
- Visit http://localhost:8000/docs
- Test `/health` endpoint
- Test `/api/v1/search/places` with a sample query

**Deliverables**:
- ✅ Working Docker environment
- ✅ All API keys configured
- ✅ Backend API documentation accessible
- ✅ Database tables created

### Week 2: Authentication & Basic UI

**Goals**:
- Implement Google OAuth login
- Create basic navigation structure
- Set up internationalization

**Tasks**:

1. **Backend Authentication**
- Test `/api/v1/auth/google` endpoint
- Verify JWT token generation
- Test token validation

2. **Frontend Authentication**
- Implement NextAuth.js configuration
- Create login page
- Test Google sign-in flow

3. **Basic UI Components**
- Header with language switcher
- Navigation menu
- Footer

**Deliverables**:
- ✅ Users can sign in with Google
- ✅ JWT tokens are issued and validated
- ✅ Basic UI structure in place

---

## 🎯 Phase 2: Core Features (Week 3-8)

### Week 3-4: Itinerary Management

**Goals**:
- Full CRUD for itineraries
- Dashboard UI
- Itinerary detail page

**Tasks**:

1. **Backend**
- Test all itinerary endpoints
- Verify data validation
- Test error handling

2. **Frontend**
- Dashboard page (list itineraries)
- Create itinerary form
- Edit/delete functionality

**Testing Checklist**:
- [ ] Create itinerary with valid dates
- [ ] Try to create with end_date < start_date (should fail)
- [ ] List all itineraries
- [ ] View single itinerary
- [ ] Update itinerary
- [ ] Delete itinerary

**Deliverables**:
- ✅ Users can manage itineraries
- ✅ All CRUD operations work
- ✅ Data validation prevents invalid dates

### Week 5-6: Map Integration & Place Search

**Goals**:
- Integrate Kakao Maps
- Implement place search
- Add places to itinerary

**Tasks**:

1. **Kakao Maps Integration**
```javascript
// Test map rendering
// Test marker placement
// Test info windows
```

2. **Place Search**
- Test Kakao keyword search API
- Implement search UI
- Display search results

3. **Add Places to Itinerary**
- Click search result → add to itinerary
- Display places on map
- Edit place details

**Testing Checklist**:
- [ ] Map renders correctly
- [ ] Search for "restaurant" in Seoul
- [ ] Search results appear
- [ ] Click result → marker appears on map
- [ ] Place is saved to database
- [ ] Reload page → markers still appear

**Deliverables**:
- ✅ Kakao map displays correctly
- ✅ Place search works in English
- ✅ Users can add places to itinerary
- ✅ Places persist in database

### Week 7-8: Budget & Currency Tools

**Goals**:
- Budget tracking
- Currency converter
- Expense categorization

**Tasks**:

1. **Budget Backend**
- Test budget CRUD endpoints
- Verify currency handling
- Test aggregation queries

2. **Budget Frontend**
- Budget entry form
- Expense list
- Total calculation by category

3. **Currency Converter**
- Test exchange rate API
- Implement caching (5 min)
- Display conversion UI

**Testing Checklist**:
- [ ] Add expense in USD
- [ ] Add expense in KRW
- [ ] View total by category
- [ ] Convert 100 USD to KRW
- [ ] Verify exchange rate updates

**Deliverables**:
- ✅ Users can track expenses
- ✅ Currency conversion works
- ✅ Budget totals are accurate

---

## 🧪 Phase 3: Testing & QA (Week 9-10)

### Week 9: Automated Testing

**Backend Tests**:
```bash
cd backend
pytest --cov=app tests/
# Target: 80%+ coverage
```

**Test Cases**:
1. Authentication
   - Valid Google OAuth flow
   - Invalid authorization code
   - JWT token expiration

2. Itineraries
   - Create with valid data
   - Create with invalid dates
   - Unauthorized access

3. Place Search
   - Valid search query
   - Empty results
   - API timeout handling

4. Exchange Rates
   - Valid currency codes
   - Invalid currency codes
   - API caching

**Frontend Tests**:
```bash
cd frontend
npm test
# Test components and pages
```

**Deliverables**:
- ✅ 80%+ test coverage
- ✅ All critical paths tested
- ✅ CI/CD pipeline configured

### Week 10: Performance & Security

**Performance Optimization**:
1. **Frontend**
   - Lighthouse score > 90
   - LCP < 2.5s
   - Image optimization
   - Code splitting

2. **Backend**
   - Database query optimization
   - API response time < 200ms
   - Implement caching

**Security Audit**:
- [ ] SQL injection prevention (SQLAlchemy ORM)
- [ ] XSS prevention (React escaping)
- [ ] CSRF protection
- [ ] JWT secret rotation
- [ ] HTTPS enforcement
- [ ] Rate limiting

**Deliverables**:
- ✅ Performance benchmarks met
- ✅ Security vulnerabilities addressed
- ✅ Load testing completed

---

## 🚀 Phase 4: Deployment (Week 11-12)

### Week 11: AWS Infrastructure Setup

**Required AWS Services**:
1. **RDS (PostgreSQL)**
   - Instance: db.t3.small
   - Multi-AZ: No (initially)
   - Backup: 7 days retention

2. **ECS (Elastic Container Service)**
   - Fargate launch type
   - 2 tasks (backend)
   - Auto-scaling enabled

3. **ECR (Elastic Container Registry)**
   - Repository for backend image
   - Repository for frontend image

4. **S3 + CloudFront**
   - Static assets
   - Next.js build output

5. **Secrets Manager**
   - API keys
   - Database credentials
   - JWT secrets

**Deployment Steps**:
```bash
# 1. Build Docker images
docker build -t travel-backend ./backend
docker build -t travel-frontend ./frontend

# 2. Push to ECR
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com
docker tag travel-backend:latest <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com/travel-backend:latest
docker push <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com/travel-backend:latest

# 3. Deploy to ECS
aws ecs update-service --cluster travel-cluster --service backend --force-new-deployment
```

**Deliverables**:
- ✅ Production environment running
- ✅ HTTPS configured
- ✅ Database backups enabled
- ✅ Monitoring & logging active

### Week 12: Launch Preparation

**Pre-Launch Checklist**:
- [ ] Terms of Service page
- [ ] Privacy Policy page
- [ ] GDPR compliance
- [ ] Cookie consent
- [ ] Error tracking (Sentry)
- [ ] Analytics (Google Analytics 4)
- [ ] Landing page SEO
- [ ] Social media accounts
- [ ] Support email setup

**Soft Launch**:
1. Beta testing with 10-20 users
2. Collect feedback
3. Fix critical bugs
4. Monitor performance

**Public Launch**:
1. Announce on social media
2. Post on Reddit (r/Korea, r/travel)
3. Submit to Product Hunt
4. Reach out to travel bloggers

**Deliverables**:
- ✅ Production site live
- ✅ Beta feedback incorporated
- ✅ Marketing materials ready
- ✅ Support channels active

---

## 📊 Phase 5: Post-Launch (Week 13+)

### Key Metrics to Track

| Metric | Target (Month 1) | Target (Month 3) |
|--------|------------------|------------------|
| DAU | 100 | 1,000 |
| MAU | 500 | 5,000 |
| Sign-up conversion | 5% | 10% |
| Itinerary creation rate | 30% | 40% |
| Pro subscription conversion | 2% | 5% |
| 7-day retention | 30% | 40% |
| 30-day retention | 15% | 20% |

### Monitoring Tools

1. **Google Analytics 4**
   - User acquisition
   - Behavior flow
   - Conversion tracking

2. **Sentry**
   - Error tracking
   - Performance monitoring
   - Release tracking

3. **AWS CloudWatch**
   - Server metrics
   - Database performance
   - API latency

### Iteration Cycle

**Weekly**:
- Review metrics
- Analyze user feedback
- Prioritize bug fixes

**Monthly**:
- Feature planning
- A/B testing results
- Performance review

---

## 🎯 Feature Roadmap (Phase 2)

### Month 4-6: Enhanced Features

1. **Social Features**
   - Share itinerary (view-only link)
   - Collaborative editing
   - Comments & suggestions

2. **Advanced Budget Tools**
   - Budget vs. actual comparison
   - Split expenses (group travel)
   - Export to PDF

3. **Offline Support**
   - PWA installation
   - Offline map caching
   - Sync when online

4. **Additional Languages**
   - Spanish
   - French
   - German

### Month 7-9: Mobile App

1. **React Native Development**
   - iOS app
   - Android app
   - Push notifications

2. **App Store Optimization**
   - Screenshots
   - App description
   - Keyword research

### Month 10-12: Integrations

1. **Booking Integration**
   - Hotels (Booking.com API)
   - Flights (Skyscanner API)
   - Tours (GetYourGuide API)

2. **Real-time Transit**
   - Seoul Metro API
   - Bus arrival times
   - Route optimization

---

## ✅ Feature Implementation Checklist

### Core Features (MVP)

- [x] Google OAuth authentication
- [x] JWT token management
- [x] Multi-language UI (en/ko/ja/zh)
- [x] Itinerary CRUD
- [x] Kakao Maps integration
- [x] Place search (English)
- [x] Add places to itinerary
- [x] Budget tracking
- [x] Currency converter
- [x] PostgreSQL database
- [x] Docker containerization
- [x] API documentation (Swagger)

### Strong Features (MVP)

- [ ] Real-time transit info (Phase 2)
- [x] Exchange rate API
- [x] Basic budget tool
- [ ] Offline mode (Phase 2)

### Future Features (Phase 2)

- [ ] Naver Maps fallback
- [ ] Collaborative itineraries
- [ ] Social sharing
- [ ] Mobile native app
- [ ] Booking integrations
- [ ] Advanced analytics
- [ ] Stripe subscription
- [ ] Email notifications

---

## 🔧 Development Best Practices

### Git Workflow

```bash
# Feature branch
git checkout -b feature/place-search
# ... make changes ...
git add .
git commit -m "feat: implement Kakao place search"
git push origin feature/place-search
# Create pull request
```

### Commit Message Convention

```
feat: add new feature
fix: bug fix
docs: documentation update
style: formatting changes
refactor: code restructuring
test: add tests
chore: maintenance tasks
```

### Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests are included
- [ ] Documentation updated
- [ ] No console.log statements
- [ ] Error handling implemented
- [ ] Security considerations addressed

---

## 📚 Required Documentation

### For Developers

1. **API Documentation**
   - Auto-generated: http://localhost:8000/docs
   - All endpoints documented
   - Request/response examples

2. **Database Schema**
   - ERD diagram
   - Table descriptions
   - Index strategy

3. **Architecture Diagram**
   - System components
   - Data flow
   - External dependencies

### For Users

1. **User Guide**
   - Getting started
   - Feature tutorials
   - FAQ

2. **Video Tutorials**
   - How to create itinerary
   - How to search places
   - How to track budget

---

## 🆘 Troubleshooting Guide

### Common Issues

**1. Docker containers won't start**
```bash
# Check logs
docker compose logs backend
docker compose logs frontend

# Rebuild
docker compose down
docker compose up --build
```

**2. Database connection error**
```bash
# Verify PostgreSQL is running
docker ps | grep postgres

# Check connection string in .env
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/traveldb
```

**3. Kakao Maps not loading**
- Verify NEXT_PUBLIC_KAKAO_JS_KEY in .env
- Check browser console for errors
- Verify domain is registered in Kakao Developers

**4. Google OAuth fails**
- Verify redirect URI matches exactly
- Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- Ensure Google+ API is enabled

---

## 📞 Support & Resources

### Official Documentation

- **Kakao Maps**: https://apis.map.kakao.com/web/documentation/
- **Kakao Local API**: https://developers.kakao.com/docs/latest/en/local/dev-guide
- **Naver Maps**: https://navermaps.github.io/maps.js.en/docs/
- **Next.js**: https://nextjs.org/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **SQLAlchemy**: https://docs.sqlalchemy.org

### Community

- **GitHub Issues**: <your-repo-url>/issues
- **Discord**: (create a server for beta testers)
- **Email**: support@your-domain.com

---

## 🎉 Success Criteria

### Technical

- ✅ 99.9% uptime
- ✅ < 200ms API response time
- ✅ < 3s page load time
- ✅ 80%+ test coverage
- ✅ Zero critical security vulnerabilities

### Business

- ✅ 1,000 MAU by Month 3
- ✅ 5% free-to-paid conversion
- ✅ 40% 7-day retention
- ✅ 4.5+ star rating (when reviews available)

### User Satisfaction

- ✅ Positive feedback from beta testers
- ✅ < 5% churn rate
- ✅ Active community engagement

---

**Last Updated**: 2025-01-19  
**Version**: 1.0  
**Status**: Ready for Development
