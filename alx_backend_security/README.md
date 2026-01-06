# IP Tracking API - Quick Start Guide

A Django REST API with IP tracking, rate limiting, and comprehensive Swagger documentation.

## Features

- ✅ IP-based rate limiting for anonymous requests
- ✅ User-based rate limiting for authenticated requests
- ✅ Interactive Swagger UI documentation
- ✅ ReDoc alternative documentation
- ✅ Easy testing with provided test script

## Setup & Installation

### 1. Apply Database Migrations
```bash
python3 manage.py migrate
```

### 2. Create a Superuser (Optional - for authenticated testing)
```bash
python3 manage.py createsuperuser
```

### 3. Start the Development Server
```bash
python3 manage.py runserver
```

## API Endpoints

### Documentation
- **Swagger UI**: http://127.0.0.1:8000/ip_tracking/docs/
- **ReDoc**: http://127.0.0.1:8000/ip_tracking/redoc/
- **JSON Schema**: http://127.0.0.1:8000/ip_tracking/swagger.json

### API Routes
- `POST /ip_tracking/login/anonymous/` - Anonymous login (5 req/min per IP)
- `POST /ip_tracking/login/authenticated/` - Authenticated login (10 req/min per user)
- `GET /ip_tracking/user/info/` - Get current user info

## Testing

### Option 1: Use Swagger UI (Recommended)
1. Open http://127.0.0.1:8000/ip_tracking/docs/
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

### Option 2: Use the Test Script
```bash
python3 test_api.py
```

This will run automated tests including:
- User info retrieval
- Anonymous login
- Rate limiting demonstration
- Authentication check

### Option 3: Use cURL

**Test Anonymous Login:**
```bash
curl -X POST http://127.0.0.1:8000/ip_tracking/login/anonymous/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

**Test Rate Limiting (run 6 times quickly):**
```bash
for i in {1..6}; do
  echo "Request $i:"
  curl -X POST http://127.0.0.1:8000/ip_tracking/login/anonymous/ \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpass"}'
  echo -e "\n---"
  sleep 0.5
done
```

**Get User Info:**
```bash
curl http://127.0.0.1:8000/ip_tracking/user/info/
```

### Option 4: Use Python Requests
```python
import requests

# Test anonymous login
response = requests.post(
    'http://127.0.0.1:8000/ip_tracking/login/anonymous/',
    json={'username': 'testuser', 'password': 'testpass'}
)
print(response.json())
```

## Rate Limiting

### Anonymous Endpoint
- **Limit**: 5 requests per minute
- **Key**: IP address
- **Method**: POST only

### Authenticated Endpoint
- **Limit**: 10 requests per minute
- **Key**: Username
- **Method**: POST only
- **Requires**: Valid authentication token

## Expected Responses

### Successful Login (200 OK)
```json
{
  "status": "success",
  "message": "Login attempt recorded",
  "ip_address": "127.0.0.1",
  "rate_limit_info": {
    "limit": "5 requests per minute",
    "method": "IP-based"
  }
}
```

### Rate Limit Exceeded (429 Too Many Requests)
```json
{
  "error": "Rate limit exceeded. Try again later."
}
```

### User Info (200 OK)
```json
{
  "user": "anonymous",
  "ip_address": "127.0.0.1",
  "is_authenticated": false
}
```

## Troubleshooting

### Server not responding?
Make sure the development server is running:
```bash
python3 manage.py runserver
```

### Rate limit not working?
The rate limit resets every minute. Wait 60 seconds between test runs.

### Authentication errors?
For authenticated endpoints, you need to:
1. Create a superuser: `python3 manage.py createsuperuser`
2. Get an authentication token
3. Include it in your request headers: `Authorization: Bearer <token>`

## Project Structure
```
ip_tracking/
├── views.py          # API endpoint logic
├── urls.py           # URL routing
├── models.py         # Database models (if any)
└── tests.py          # Unit tests
```

## Next Steps

1. ✅ Test the API using Swagger UI
2. ✅ Run the automated test script
3. ✅ Implement actual login logic in views
4. ✅ Add database models for IP tracking
5. ✅ Set up token authentication for authenticated endpoints
6. ✅ Add logging for security monitoring

## License
MIT License