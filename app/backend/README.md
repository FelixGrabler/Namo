# Namo Backend API

A FastAPI-based backend for the Namo name voting application.

## Features

- **User Management**: Registration and authentication with JWT tokens
- **Name Management**: CRUD operations for names with filtering
- **Voting System**: Like/dislike voting with statistics
- **PostgreSQL Database**: Robust data storage with relationships
- **Docker Support**: Easy deployment with Docker Compose

## Database Schema

### Users Table

```sql
users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
)
```

### Names Table

```sql
names (
  id SERIAL PRIMARY KEY,
  source TEXT NOT NULL,          -- e.g. 'Austria'
  name TEXT NOT NULL,
  gender TEXT CHECK (gender IN ('m', 'f')),
  rank INTEGER,
  count INTEGER
)
```

### Votes Table

```sql
votes (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  name_id INTEGER REFERENCES names(id),
  vote BOOLEAN,                  -- TRUE = like, FALSE = dislike
  UNIQUE (user_id, name_id)      -- 1 vote per name per user
)
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Names

- `GET /names/random` - Get a random name (with optional gender filter)
- `GET /names/` - Get list of names with pagination and filters
- `POST /names/` - Create a new name entry
- `GET /names/{name_id}` - Get a specific name by ID

### Votes

- `POST /votes/` - Create or update a vote for a name
- `GET /votes/my-votes` - Get current user's votes
- `DELETE /votes/{vote_id}` - Delete a vote
- `GET /votes/{name_id}/stats` - Get voting statistics for a name

### Utility

- `GET /` - API welcome message
- `GET /health` - Health check endpoint

## Quick Start

### Using Docker Compose (Recommended)

1. Start the services:

```bash
docker-compose up -d
```

2. Initialize the database with sample data:

```bash
docker-compose exec backend python init_db.py
```

3. Test the API:

```bash
docker-compose exec backend python test_api.py
```

The API will be available at `http://localhost:8000`

### Manual Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your database configuration
```

3. Set up PostgreSQL database and update DATABASE_URL in .env

4. Initialize the database:

```bash
python init_db.py
```

5. Run the application:

```bash
uvicorn main:app --reload
```

## Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
```

## API Documentation

Once the server is running, you can access:

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. After registering and logging in, include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Example Usage

### Register a new user

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Get a random name

```bash
curl -X GET "http://localhost:8000/names/random" \
  -H "Authorization: Bearer <your-token>"
```

### Vote on a name

```bash
curl -X POST "http://localhost:8000/votes/" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"name_id": 1, "vote": true}'
```

## Development

The application is built with:

- **FastAPI**: Modern, fast web framework for Python
- **SQLAlchemy**: Python SQL toolkit and ORM
- **PostgreSQL**: Advanced open source relational database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for secure authentication

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

This will test user registration, login, name retrieval, voting, and statistics endpoints.
