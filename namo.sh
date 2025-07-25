#!/bin/bash

# Namo Environment Management Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    printf "${1}${2}${NC}\n"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  dev          Start development environment (uses docker-compose.override.yml automatically)"
    echo "  prod         Start production environment (uses docker-compose.prod.yml)"
    echo "  stop         Stop current environment"
    echo "  logs         Show logs"
    echo "  health       Check health of services"
    echo "  clean        Clean up Docker resources"
    echo ""
    echo "Options:"
    echo "  --build      Force rebuild of images"
    echo "  --help       Show this help message"
}

# Function to start development environment
start_dev() {
    local build_flag=$1
    
    print_color $BLUE "Starting development environment..."
    print_color $YELLOW "Using .env (development) and docker-compose.override.yml"
    
    if [ "$build_flag" = "--build" ]; then
        docker-compose up -d --build
    else
        docker-compose up -d
    fi
    
    print_color $GREEN "✓ Development environment started!"
    print_color $YELLOW "Frontend: http://localhost:5173"
    print_color $YELLOW "Backend API: http://localhost:8000"
    print_color $YELLOW "Database: localhost:5432"
}

# Function to start production environment
start_prod() {
    local build_flag=$1
    
    print_color $BLUE "Starting production environment..."
    print_color $YELLOW "Using docker-compose.prod.yml with .env.production"
    
    if [ "$build_flag" = "--build" ]; then
        ENVIRONMENT=production docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production up -d --build
    else
        ENVIRONMENT=production docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.production up -d
    fi
    
    print_color $GREEN "✓ Production environment started!"
    print_color $YELLOW "Frontend: http://localhost"
    print_color $YELLOW "Backend API: http://localhost:8000"
}

# Function to stop services
stop_services() {
    print_color $BLUE "Stopping services..."
    
    # Try to stop both environments
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down 2>/dev/null || true
    
    print_color $GREEN "✓ Services stopped"
}

# Function to show logs
show_logs() {
    print_color $BLUE "Showing logs (development by default)..."
    docker-compose logs -f
}

# Function to show production logs
show_prod_logs() {
    print_color $BLUE "Showing production logs..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f
}

# Function to check health
check_health() {
    print_color $BLUE "Checking health of services..."
    
    # Check backend
    if curl -s -f http://localhost:8000/health > /dev/null; then
        print_color $GREEN "✓ Backend is healthy"
    else
        print_color $RED "✗ Backend is not responding"
    fi
    
    # Check frontend (try both dev and prod ports)
    if curl -s -f http://localhost:5173 > /dev/null; then
        print_color $GREEN "✓ Frontend (dev) is healthy"
    elif curl -s -f http://localhost > /dev/null; then
        print_color $GREEN "✓ Frontend (prod) is healthy"
    else
        print_color $RED "✗ Frontend is not responding"
    fi
    
    # Check database
    if docker-compose exec -T db pg_isready > /dev/null 2>&1; then
        print_color $GREEN "✓ Database is healthy"
    else
        print_color $RED "✗ Database is not responding"
    fi
}

# Function to clean up
clean_up() {
    print_color $BLUE "Cleaning up Docker resources..."
    
    docker-compose down -v --rmi all 2>/dev/null || true
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down -v --rmi all 2>/dev/null || true
    docker system prune -f
    
    print_color $GREEN "✓ Cleanup completed"
}

# Main script logic
case "${1:-}" in
    dev)
        start_dev "$2"
        ;;
    prod)
        start_prod "$2"
        ;;
    stop)
        stop_services
        ;;
    logs)
        if [ "$2" = "prod" ]; then
            show_prod_logs
        else
            show_logs
        fi
        ;;
    health)
        check_health
        ;;
    clean)
        clean_up
        ;;
    --help|-h|help)
        show_usage
        ;;
    *)
        print_color $BLUE "Docker Compose Environment Management"
        echo ""
        print_color $YELLOW "Development: Uses docker-compose.yml + docker-compose.override.yml + .env"
        print_color $YELLOW "Production:  Uses docker-compose.yml + docker-compose.prod.yml + .env.production"
        echo ""
        show_usage
        ;;
esac
