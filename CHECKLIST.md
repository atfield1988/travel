# ✅ Development Checklist

## Phase 0: Setup (Week 0)

### API Keys & Accounts
- [ ] Kakao Developers account created
- [ ] Kakao JavaScript Key obtained
- [ ] Kakao REST API Key obtained
- [ ] Google Cloud Console project created
- [ ] Google OAuth Client ID obtained
- [ ] Google OAuth Client Secret obtained
- [ ] ExchangeRate-API account created
- [ ] ExchangeRate-API key obtained
- [ ] (Optional) Naver Developers account created

### Development Environment
- [ ] Docker Desktop installed
- [ ] Node.js 18+ installed
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Code editor (VS Code) installed
- [ ] Repository cloned
- [ ] .env file created from .env.example
- [ ] All API keys added to .env

### Initial Verification
- [ ] `docker compose up --build` runs successfully
- [ ] Backend accessible at http://localhost:8000
- [ ] Frontend accessible at http://localhost:3000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Database tables created
- [ ] No errors in Docker logs

## Phase 1: Foundation (Week 1-2)

### Week 1: Infrastructure
- [ ] Git repository initialized
- [ ] Branch protection rules configured
- [ ] Docker containers start without errors
- [ ] PostgreSQL connection verified
- [ ] Backend health endpoint responds
- [ ] Frontend loads without errors
- [ ] CORS configured correctly

### Week 2: Authentication
- [ ] Google OAuth flow tested manually
- [ ] JWT tokens generated correctly
- [ ] Token validation works
- [ ] Login page created
- [ ] User can sign in with Google
- [ ] User session persists
- [ ] Logout functionality works

## Phase 2: Core Features (Week 3-8)

### Week 3-4: Itinerary Management
- [ ] Create itinerary endpoint tested
- [ ] List itineraries endpoint tested
- [ ] Get single itinerary endpoint tested
- [ ] Update itinerary endpoint tested
- [ ] Delete itinerary endpoint tested
- [ ] Dashboard page displays itineraries
- [ ] Create itinerary form works
- [ ] Date validation prevents invalid dates
- [ ] Edit itinerary functionality works
- [ ] Delete confirmation dialog implemented

### Week 5-6: Map & Search
- [ ] Kakao Maps SDK loads correctly
- [ ] Map renders centered on Seoul
- [ ] Place search API endpoint tested
- [ ] Search returns results for English queries
- [ ] Search UI implemented
- [ ] Search results display correctly
- [ ] Click result adds marker to map
- [ ] Add place to itinerary works
- [ ] Places persist in database
- [ ] Markers reload on page refresh

### Week 7-8: Budget & Currency
- [ ] Budget CRUD endpoints tested
- [ ] Add budget entry works
- [ ] List budgets works
- [ ] Budget totals calculate correctly
- [ ] Category filtering works
- [ ] Exchange rate API tested
- [ ] Currency converter displays rates
- [ ] Rate caching implemented (5 min)
- [ ] Multiple currencies supported
- [ ] Budget UI is user-friendly

## Phase 3: Testing & QA (Week 9-10)

### Week 9: Automated Testing
- [ ] Backend unit tests written
- [ ] Backend integration tests written
- [ ] Test coverage > 80%
- [ ] Frontend component tests written
- [ ] E2E tests written (Cypress)
- [ ] All tests pass
- [ ] CI/CD pipeline configured
- [ ] Tests run on every PR

### Week 10: Performance & Security
- [ ] Lighthouse score > 90
- [ ] LCP < 2.5s
- [ ] API response time < 200ms
- [ ] Database queries optimized
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] CSRF protection implemented
- [ ] Rate limiting configured
- [ ] HTTPS enforced
- [ ] Security headers configured

## Phase 4: Deployment (Week 11-12)

### Week 11: AWS Setup
- [ ] AWS account created
- [ ] RDS PostgreSQL instance created
- [ ] ECR repositories created
- [ ] ECS cluster created
- [ ] Docker images built
- [ ] Images pushed to ECR
- [ ] ECS tasks configured
- [ ] Load balancer configured
- [ ] Domain name registered
- [ ] SSL certificate obtained

### Week 12: Launch
- [ ] Production environment tested
- [ ] Database migration completed
- [ ] Environment variables configured
- [ ] Monitoring enabled (CloudWatch)
- [ ] Error tracking enabled (Sentry)
- [ ] Analytics enabled (GA4)
- [ ] Terms of Service page created
- [ ] Privacy Policy page created
- [ ] Beta testing completed
- [ ] Public launch announced

## Ongoing: Maintenance

### Daily
- [ ] Check error logs
- [ ] Monitor uptime
- [ ] Review user feedback

### Weekly
- [ ] Review metrics (DAU, MAU)
- [ ] Analyze user behavior
- [ ] Prioritize bug fixes
- [ ] Plan new features

### Monthly
- [ ] Security updates
- [ ] Dependency updates
- [ ] Performance review
- [ ] Feature releases
