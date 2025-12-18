# DT Tools API (FastAPI Backend)

Backend service for DT Tools, built with FastAPI and Python 3.11+. Provides health checks, dev-only auth, and mock data APIs for the frontend.

## Requirements

- Python 3.11 or higher

## Setup

```bash
cd dt-tools-demo-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Copy the example environment file and adjust values if needed:

```bash
cp .env.example .env
```

Default environment variables:

- `APP_NAME="DT Tools API"`
- `ENV=local`
- `HOST=0.0.0.0`
- `PORT=8000`
- `CORS_ORIGINS="http://localhost:5173,http://localhost:3000"`
- `JWT_SECRET="dev-secret"` (dev-only, do not use in production)
- `JWT_EXPIRES_MINUTES=120`

## Running the Server

From the `dt-tools-demo-backend` directory:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The interactive API docs will be available at:

- Swagger UI: http://localhost:8000/docs

## Testing

Run the test suite with:

```bash
pytest
```

## Example Usage

### 1. Health Check

```bash
curl -s http://localhost:8000/api/v1/health
```

### 2. Login (Dev-Only)

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@pfizer.com", "password": "anything"}'
```

The response will contain an `access_token`:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "email": "user@pfizer.com",
    "name": "Demo User",
    "roles": ["planner"]
  }
}
```

### 3. Fetch Mock Data (Protected)

First, store the token in a shell variable:

```bash
TOKEN="<paste access_token here>"
```

Then call a protected mock data endpoint, for example PreCheck dashboard data:

```bash
curl -s http://localhost:8000/api/v1/mock/precheck-dashboard \
  -H "Authorization: Bearer $TOKEN"
```

Or fetch all mock payloads at once:

```bash
curl -s http://localhost:8000/api/v1/mock/all \
  -H "Authorization: Bearer $TOKEN"
```

## CORS and Frontend Integration

CORS is configured to allow requests from:

- `http://localhost:5173`
- `http://localhost:3000`

The frontend can call the backend using `fetch` or Axios, including credentials and authorization headers. In non-local environments, update `CORS_ORIGINS` accordingly in your `.env` or deployment configuration.


