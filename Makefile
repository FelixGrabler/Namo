.PHONY: help dev prod down clean logs shell test

# Default target
help:
	@echo "Namo Docker Management"
	@echo "======================"
	@echo "Available commands:"
	@echo "  make dev          - Start development environment (docker-compose.dev.yml)"
	@echo "  make prod         - Start production environment (docker-compose.yml)"
	@echo "  make down         - Stop development services"
	@echo "  make down-prod    - Stop production services"
	@echo "  make clean        - Remove all containers, volumes, and images"
	@echo "  make logs         - Show logs for development environment"
	@echo "  make logs-prod    - Show logs for production environment"
	@echo "  make shell        - Open shell in development backend container"
	@echo "  make shell-prod   - Open shell in production backend container"
	@echo "  make test         - Run tests in development environment"
	@echo "  make build        - Build development images"
	@echo "  make build-prod   - Build production images"

# Development environment
dev:
	@echo "Starting development environment..."
	@echo "Using docker-compose.dev.yml"
	@echo "All configuration is embedded in Docker Compose files"
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Development environment started!"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend API: http://localhost:8060"
	@echo "Database: localhost:15432"

# Production environment
prod:
	@echo "Starting production environment..."
	@echo "Using docker-compose.yml"
	@echo "All configuration is embedded in Docker Compose files"
	ENVIRONMENT=production docker-compose -f docker-compose.yml --env-file .env.production up -d
	@echo "Production environment started!"

# Stop development environment
down:
	@echo "Stopping development environment..."
	docker-compose -f docker-compose.dev.yml down

# Stop production environment
down-prod:
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.yml down

# Clean everything
clean:
	@echo "Cleaning up all Docker resources..."
	docker-compose -f docker-compose.dev.yml down -v --rmi all 2>/dev/null || true
	docker-compose -f docker-compose.yml down -v --rmi all 2>/dev/null || true
	docker system prune -f

# Show logs
logs:
	docker-compose -f docker-compose.dev.yml logs -f

logs-prod:
	docker-compose -f docker-compose.yml logs -f

# Open shell in backend container
shell:
	docker-compose -f docker-compose.dev.yml exec backend /bin/bash

shell-prod:
	docker-compose -f docker-compose.yml exec backend /bin/bash

# Run tests
test:
	docker-compose -f docker-compose.dev.yml exec backend python -m pytest

# Build images
build:
	@echo "Building development images..."
	docker-compose -f docker-compose.dev.yml build

build-prod:
	@echo "Building production images..."
	ENVIRONMENT=production docker-compose -f docker-compose.yml --env-file .env.production build

# Database operations
db-migrate:
	docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

db-migrate-prod:
	docker-compose -f docker-compose.yml exec backend alembic upgrade head

# Health checks
health:
	@echo "Checking development environment health..."
	@curl -f http://localhost:8060/health || echo "Backend health check failed"
	@curl -f http://localhost:5173 || echo "Frontend health check failed"

health-prod:
	@echo "Checking production environment health..."
	@curl -f http://localhost:8001/health || echo "Backend health check failed"
	@curl -f http://localhost:8080 || echo "Frontend health check failed"
