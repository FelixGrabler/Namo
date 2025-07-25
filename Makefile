.PHONY: help dev prod down clean logs shell test

# Default target
help:
	@echo "Namo Docker Management"
	@echo "======================"
	@echo "Available commands:"
	@echo "  make dev          - Start development environment (uses docker-compose.override.yml automatically)"
	@echo "  make prod         - Start production environment" 
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

# Development environment (automatically uses docker-compose.override.yml)
dev:
	@echo "Starting development environment..."
	@echo "Using docker-compose.yml + docker-compose.override.yml"
	@echo "All configuration is embedded in Docker Compose files"
	docker-compose up -d
	@echo "Development environment started!"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend API: http://localhost:8000"
	@echo "Database: localhost:5432"

# Production environment 
prod:
	@echo "Starting production environment..."
	@echo "Using docker-compose.yml + docker-compose.prod.yml"
	@echo "All configuration is embedded in Docker Compose files"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "Production environment started!"

# Stop development environment
down:
	@echo "Stopping development environment..."
	docker-compose down

# Stop production environment
down-prod:
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

# Clean everything
clean:
	@echo "Cleaning up all Docker resources..."
	docker-compose down -v --rmi all 2>/dev/null || true
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down -v --rmi all 2>/dev/null || true
	docker system prune -f

# Show logs
logs:
	docker-compose logs -f

logs-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Open shell in backend container
shell:
	docker-compose exec backend /bin/bash

shell-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec backend /bin/bash

# Run tests
test:
	docker-compose exec backend python -m pytest

# Build images
build:
	@echo "Building development images..."
	docker-compose build

build-prod:
	@echo "Building production images..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Database operations
db-migrate:
	docker-compose exec backend alembic upgrade head

db-migrate-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec backend alembic upgrade head

# Health checks
health:
	@echo "Checking development environment health..."
	@curl -f http://localhost:8000/health || echo "Backend health check failed"
	@curl -f http://localhost:5173 || echo "Frontend health check failed"

health-prod:
	@echo "Checking production environment health..."
	@curl -f http://localhost:8000/health || echo "Backend health check failed"
	@curl -f http://localhost || echo "Frontend health check failed"
