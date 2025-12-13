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
└── docker-compose.yml        # Production deployment
└── docker-compose.dev.yml    # Local development setup
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
docker-compose -f docker-compose.dev.yml up -d
```

4. **Access the application**

- Frontend: http://localhost:5173
- Backend API: http://localhost:8060
- API Documentation: http://localhost:8060/docs

### Production Development

```bash
docker-compose -f docker-compose.yml up -d
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
- [API Documentation](http://localhost:8060/docs) (when running)

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
docker pull ghcr.io/felixgrabler/namo/backend:latest
```

### Support

For detailed troubleshooting, see:

- [Kubernetes Deployment Guide](docs/KUBERNETES_DEPLOYMENT.md#troubleshooting-common-issues)
- [GitHub Actions Guide](docs/GITHUB_ACTIONS.md#troubleshooting)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
