# Namo 👶📝

**A baby name decision app by Felix Grabler**

Namo helps you browse, like, and dislike baby names from real-world name data.

Sources (will) include Austria, Germany, Switzerland, UK, Australia, USA, Spain, France, Liechtenstein, and maybe more.

## 🚀 Tech Stack

### Frontend

- [Vue 3](https://vuejs.org/) — modern frontend framework
- [Vite](https://vitejs.dev/) — lightning-fast dev/build tool
- [Pinia](https://pinia.vuejs.org/) — state management
- [Axios](https://axios-http.com/) — HTTP client

### Backend

- [FastAPI](https://fastapi.tiangolo.com/) — Python web API framework
- [PostgreSQL](https://www.postgresql.org/) — relational database
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for DB access
- [Alembic](https://alembic.sqlalchemy.org/) — DB migrations
- [bcrypt](https://pypi.org/project/bcrypt/) — password hashing
- [JWT](https://jwt.io/) — token-based authentication

## ✅ Core Features (v0)

- User registration & login (username/password)
- Load names from Austria (rank, count, gender)
- Swipe yes/no on names
- Store votes in backend
- Simple UI with vote buttons
- No filters or sorting (yet)

## 🧠 Planned Features

- Filter by gender, length, first letter, frequency
- Add more countries (DE, UK, etc.)
- Collaboration between users (couples)

## ⚙️ Development & Production Setup

This project uses Docker Compose with environment-specific configurations for both development and production.

### Configuration Structure

- **`docker-compose.yml`** - Base configuration + development environment variables
- **`docker-compose.override.yml`** - Development overrides (used automatically)
- **`docker-compose.prod.yml`** - Production configuration + production environment variables
- **`secrets/`** - Sensitive data (passwords, API keys, tokens)

### Dockerfiles

- **`app/backend/Dockerfile.dev`** - Development backend (hot reload, dev tools)
- **`app/backend/Dockerfile`** - Production backend (optimized, Gunicorn)
- **`app/frontend/Dockerfile.dev`** - Development frontend (Vite dev server)
- **`app/frontend/Dockerfile`** - Production frontend (Nginx, static files)

### Quick Start

#### Development Environment

```bash
# Option 1: Using Docker Compose directly (automatic override)
docker-compose up -d

# Option 2: Using Make
make dev

# Option 3: Using the management script
./namo.sh dev
```

**Development URLs:**

- Frontend: http://localhost:5173 (Vite dev server)
- Backend API: http://localhost:8000
- Database: localhost:5432

#### Production Environment

```bash
# Option 1: Using Make
make prod

# Option 2: Using the management script
./namo.sh prod
```

**Production URLs:**

- Frontend: http://localhost (Nginx)
- Backend API: http://localhost:8000

### Development vs Production Differences

| Feature                | Development            | Production                |
| ---------------------- | ---------------------- | ------------------------- |
| **Backend Server**     | Uvicorn with reload    | Gunicorn with 4 workers   |
| **Frontend Server**    | Vite dev server        | Nginx static files        |
| **Hot Reload**         | ✅ Enabled             | ❌ Disabled               |
| **Debug Mode**         | ✅ Enabled             | ❌ Disabled               |
| **CORS**               | Permissive (localhost) | Restrictive (domain only) |
| **JWT Expiry**         | 30 minutes             | 15 minutes                |
| **Container Security** | Standard user          | Non-root user             |

### Common Commands

```bash
# Management script
./namo.sh dev           # Start development
./namo.sh prod          # Start production
./namo.sh stop          # Stop all services
./namo.sh logs          # Show logs
./namo.sh health        # Check service health

# Make commands
make dev               # Start development
make prod              # Start production
make logs              # Show logs
make test              # Run tests
make clean             # Clean up everything
```

### Production Deployment Checklist

Before deploying to production:

1. **Update `.env.production`:**

   - Change `POSTGRES_PASSWORD` to a strong password
   - Change `SECRET_KEY` to a strong secret
   - Update `CORS_ORIGINS` to your domain
   - Update `VITE_API_URL` to your API domain

2. **Configure SSL/HTTPS in `nginx/nginx.conf`**
3. **Set up proper firewall rules**
4. **Configure monitoring and backups**

---

## Legacy Setup (Manual)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
