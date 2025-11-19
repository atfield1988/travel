# 📡 API Reference

Base URL: `http://localhost:8000/api/v1` (development)

All endpoints require authentication except `/auth/*`.

## Authentication

### POST /auth/google

Exchange Google authorization code for JWT tokens.

**Request Body**:
```json
{
  "code": "google_authorization_code"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**:
- 400: Invalid authorization code
- 500: Server error

---

## Users

### GET /users/me

Get current user profile.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200):
```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "language_code": "en",
  "currency_code": "USD",
  "avatar_url": "https://..."
}
```

### PUT /users/me

Update current user profile.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "display_name": "Jane Doe",
  "language_code": "ko",
  "currency_code": "KRW"
}
```

**Response** (200): Updated user object

---

## Itineraries

### GET /itineraries

List all itineraries for current user.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Query Parameters**:
- `limit` (int, default: 10): Number of results
- `offset` (int, default: 0): Pagination offset

**Response** (200):
```json
[
  {
    "id": 1,
    "title": "Seoul Trip",
    "description": "5 days in Seoul",
    "start_date": "2025-03-01",
    "end_date": "2025-03-05",
    "created_at": "2025-01-19T10:00:00Z",
    "updated_at": "2025-01-19T10:00:00Z"
  }
]
```

### POST /itineraries

Create a new itinerary.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "title": "Seoul Trip",
  "description": "5 days exploring Seoul",
  "start_date": "2025-03-01",
  "end_date": "2025-03-05"
}
```

**Response** (201): Created itinerary object

**Errors**:
- 400: Invalid dates (end_date before start_date)

### GET /itineraries/{id}

Get single itinerary details.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200): Itinerary object

**Errors**:
- 404: Itinerary not found
- 403: Not authorized

---

## Itinerary Items

### GET /itineraries/{itinerary_id}/items

List all places in an itinerary.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200):
```json
[
  {
    "id": 1,
    "place_name": "Myeongdong Shopping District",
    "latitude": 37.5636,
    "longitude": 126.9826,
    "visit_date": "2025-03-01",
    "visit_order": 1,
    "memo": "Shopping and street food",
    "place_type": "attraction",
    "kakao_place_id": "12345",
    "created_at": "2025-01-19T10:00:00Z",
    "updated_at": "2025-01-19T10:00:00Z"
  }
]
```

### POST /itineraries/{itinerary_id}/items

Add a place to an itinerary.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "place_name": "Myeongdong Shopping District",
  "latitude": 37.5636,
  "longitude": 126.9826,
  "visit_date": "2025-03-01",
  "visit_order": 1,
  "memo": "Shopping and street food",
  "place_type": "attraction",
  "kakao_place_id": "12345"
}
```

**Response** (201): Created item object

---

## Budgets

### GET /itineraries/{itinerary_id}/budgets

List all budget entries for an itinerary.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200):
```json
[
  {
    "id": 1,
    "category": "food",
    "amount": 50.00,
    "currency": "USD",
    "spent_at": "2025-03-01T12:00:00Z",
    "description": "Lunch at Korean BBQ",
    "created_at": "2025-01-19T10:00:00Z",
    "updated_at": "2025-01-19T10:00:00Z"
  }
]
```

### POST /itineraries/{itinerary_id}/budgets

Add a budget entry.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "category": "food",
  "amount": 50.00,
  "currency": "USD",
  "spent_at": "2025-03-01T12:00:00Z",
  "description": "Lunch at Korean BBQ"
}
```

**Response** (201): Created budget object

---

## Search

### GET /search/places

Search for places using Kakao Local API.

**Query Parameters**:
- `q` (string, required): Search query
- `latitude` (float, required): Center latitude
- `longitude` (float, required): Center longitude
- `language` (string, default: "en"): Language code
- `limit` (int, default: 15): Number of results

**Example**:
```
GET /search/places?q=restaurant&latitude=37.5665&longitude=126.9780&limit=10
```

**Response** (200):
```json
[
  {
    "id": "12345",
    "name": "Korean BBQ Restaurant",
    "latitude": 37.5636,
    "longitude": 126.9826,
    "address": "123 Myeongdong-gil, Jung-gu, Seoul",
    "phone": "02-1234-5678",
    "kakao_place_id": "12345"
  }
]
```

**Errors**:
- 502: Kakao API error

---

## Exchange Rates

### GET /exchange/rates

Get current exchange rates.

**Query Parameters**:
- `base_currency` (string, default: "USD"): Base currency code
- `target_currencies` (string, default: "KRW,JPY,CNY"): Comma-separated target currencies

**Example**:
```
GET /exchange/rates?base_currency=USD&target_currencies=KRW,JPY,CNY
```

**Response** (200):
```json
{
  "base": "USD",
  "rates": {
    "KRW": 1320.50,
    "JPY": 148.25,
    "CNY": 7.24
  },
  "timestamp": "2025-01-19T10:00:00Z"
}
```

**Errors**:
- 502: ExchangeRate API error

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes**:
- 400: Bad Request (invalid input)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (not authorized for resource)
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error
- 502: Bad Gateway (external API error)

---

## Rate Limiting

- Free tier: 100 requests/minute per IP
- Pro tier: 1000 requests/minute per user

Exceeded limits return 429 Too Many Requests.

---

## Official API Documentation

Interactive API docs (Swagger UI): http://localhost:8000/docs
