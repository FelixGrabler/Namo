# Namo - Baby Name Analytics Platform

A full-stack web application for analyzing baby name trends and statistics across multiple countries, built with FastAPI backend, Vue.js frontend, and PostgreSQL database.

## 🚀 Features

- **Multi-country name data analysis**
- **Real-time API with FastAPI**
- **Modern Vue.js frontend with Vite**
- **PostgreSQL database with persistent storage**
- **Docker containerization**
- **Kubernetes deployment ready**
- **CI/CD with GitHub Actions**
- **SSL/TLS support with automatic certificate management**

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Vue.js SPA    │◄──►│  FastAPI        │◄──►│  PostgreSQL     │
│   (Frontend)    │    │  (Backend)      │    │  (Database)     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌────▼────┐             ┌────▼────┐             ┌────▼────┐
    │ Nginx   │             │ Uvicorn │             │ Volume  │
    │ (Proxy) │             │ (ASGI)  │             │ (Data)  │
    └─────────┘             └─────────┘             └─────────┘
```

## 🛠️ Technology Stack

### Backend

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend

- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type-safe JavaScript

### Infrastructure

- **Docker & Docker Compose** - Containerization
- **Kubernetes** - Container orchestration
- **Nginx** - Reverse proxy and static file serving
- **GitHub Actions** - CI/CD pipeline
- **Let's Encrypt** - SSL certificates

## 📁 Project Structure

```
namo/
├── app/
│   ├── backend/              # FastAPI backend application
│   │   ├── models/           # Database models
│   │   ├── routes/           # API endpoints
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── auth/             # Authentication logic
│   │   ├── utils/            # Utility functions
│   │   └── main.py           # Application entry point
│   └── frontend/             # Vue.js frontend application
│       ├── src/              # Source code
│       ├── public/           # Static assets
│       └── package.json      # Dependencies
├── data/                     # Raw data files by country
├── k8s/                      # Kubernetes manifests
│   ├── base/                 # Base configurations
│   └── overlays/             # Environment-specific overrides
├── docs/                     # Documentation
├── scripts/                  # Deployment scripts
├── nginx/                    # Nginx configuration
├── secrets/                  # Secret files (dev only)
└── docker-compose.yml        # Local development setup
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/FelixGrabler/Namo.git
cd Namo
```

2. **Set up environment secrets**

```bash
cp secrets/dev_postgres_password.example.txt secrets/dev_postgres_password.txt
# Edit the secret files with your values
```

3. **Start the development environment**

```bash
docker-compose up -d
```

4. **Access the application**

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Development

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## ☸️ Kubernetes Deployment

### Prerequisites for Production

- Kubernetes cluster (v1.20+)
- kubectl configured
- Domain name (`grabler.me`)
- GitHub repository with Actions enabled

### Quick Deploy to Kubernetes

1. **Set up the cluster**

```bash
./scripts/setup-k8s.sh
```

2. **Configure GitHub Secrets**

Set up these secrets in your GitHub repository:

| Secret               | Description                    |
| -------------------- | ------------------------------ |
| `KUBECONFIG`         | Base64-encoded kubeconfig file |
| `POSTGRES_PASSWORD`  | PostgreSQL password            |
| `SECRET_KEY`         | FastAPI JWT secret key         |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token (optional)  |
| `TELEGRAM_CHAT_ID`   | Telegram chat ID (optional)    |

3. **Deploy**

```bash
git push origin main  # Triggers automatic deployment
```

4. **Access your application**

- Website: https://grabler.me
- API: https://api.grabler.me

### Manual Kubernetes Deployment

```bash
# Deploy to production
kubectl apply -k k8s/overlays/production

# Monitor deployment
kubectl get pods -n namo -w
```

## 🔧 Configuration

### Environment Variables

#### Backend

- `ENVIRONMENT` - Application environment (development/production)
- `DATABASE_HOST` - PostgreSQL host
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password
- `SECRET_KEY` - JWT secret key
- `DEBUG` - Enable debug mode
- `LOG_LEVEL` - Logging level

#### Frontend

- `VITE_API_URL` - Backend API URL
- `VITE_ENVIRONMENT` - Environment name
- `VITE_APP_NAME` - Application name

### Secret Management

For production, secrets are managed through:

- Kubernetes Secrets
- GitHub Secrets (for CI/CD)
- External secret managers (recommended for large deployments)

## 📊 Data Sources

The application includes baby name data from:

- 🇦🇺 Australia (1952-2024)
- 🇦🇹 Austria
- 🇩🇪 Germany
- 🇫🇷 France
- 🇮🇹 Italy
- 🇱🇮 Liechtenstein
- 🇳🇱 Netherlands
- 🇨🇭 Switzerland
- 🇪🇸 Spain
- 🇬🇧 United Kingdom
- 🇺🇸 United States

## 🧪 Testing

### Backend Tests

```bash
cd app/backend
python -m pytest
```

### Frontend Tests

```bash
cd app/frontend
npm test
```

### Local Kubernetes Testing

```bash
./scripts/deploy-local.sh
```

## 📈 Monitoring

### Application Health

- Backend: `/health` endpoint
- Frontend: Root endpoint (`/`)
- Database: PostgreSQL health checks

### Kubernetes Monitoring

```bash
# Check pod status
kubectl get pods -n namo

# View logs
kubectl logs -f deployment/backend -n namo

# Check ingress
kubectl get ingress -n namo
```

## 🔒 Security

- HTTPS with automatic Let's Encrypt certificates
- JWT-based authentication
- CORS configuration
- Container security scanning
- Secret management
- Network policies (recommended)

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Tests** - Runs backend and frontend tests
2. **Builds** - Creates Docker images
3. **Pushes** - Uploads images to GitHub Container Registry
4. **Deploys** - Updates Kubernetes cluster
5. **Verifies** - Checks deployment health

## 📚 Documentation

- [Kubernetes Deployment Guide](docs/KUBERNETES_DEPLOYMENT.md)
- [GitHub Actions Setup](docs/GITHUB_ACTIONS.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Issues**

```bash
# Check if PostgreSQL is running
kubectl exec -it deployment/postgres -n namo -- pg_isready
```

2. **SSL Certificate Issues**

```bash
# Check certificate status
kubectl get certificates -n namo
```

3. **Image Pull Issues**

```bash
# Verify image exists
docker pull ghcr.io/your-username/namo/backend:latest
```

### Support

For detailed troubleshooting, see:

- [Kubernetes Deployment Guide](docs/KUBERNETES_DEPLOYMENT.md#troubleshooting-common-issues)
- [GitHub Actions Guide](docs/GITHUB_ACTIONS.md#troubleshooting)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Baby name data from various national statistics offices
- Open source community for the amazing tools and frameworks 👶📝

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
