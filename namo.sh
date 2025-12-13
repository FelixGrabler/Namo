#!/bin/bash

# Namo Environment Management Script

set -e

DEV_COMPOSE="docker-compose.dev.yml"
PROD_COMPOSE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_color() {
    printf "%b%s%b\n" "$1" "$2" "$NC"
}

show_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  dev          Start development environment ($DEV_COMPOSE)"
    echo "  prod         Start production environment ($PROD_COMPOSE)"
    echo "  stop         Stop current environment"
    echo "  logs         Show development logs (use 'logs prod' for production)"
    echo "  health       Check health of services"
    echo "  clean        Clean up Docker resources"
    echo ""
    echo "Options:"
    echo "  --build      Force rebuild of images"
    echo "  --help       Show this help message"
}

start_dev() {
    local build_flag=$1
    local compose_cmd=(docker-compose -f "$DEV_COMPOSE")

    print_color "$BLUE" "Starting development environment..."
    print_color "$YELLOW" "Using $DEV_COMPOSE and .env"

    if [ "$build_flag" = "--build" ]; then
        "${compose_cmd[@]}" up -d --build
    else
        "${compose_cmd[@]}" up -d
    fi

    print_color "$GREEN" "[OK] Development environment started!"
    print_color "$YELLOW" "Frontend: http://localhost:5173"
    print_color "$YELLOW" "Backend API: http://localhost:8060"
    print_color "$YELLOW" "Database: localhost:15432"
}

start_prod() {
    local build_flag=$1

    print_color "$BLUE" "Starting production environment..."
    print_color "$YELLOW" "Using $PROD_COMPOSE with .env.production"

    if [ "$build_flag" = "--build" ]; then
        ENVIRONMENT=production docker-compose -f "$PROD_COMPOSE" --env-file .env.production up -d --build
    else
        ENVIRONMENT=production docker-compose -f "$PROD_COMPOSE" --env-file .env.production up -d
    fi

    print_color "$GREEN" "[OK] Production environment started!"
    print_color "$YELLOW" "Frontend: http://localhost:8080"
    print_color "$YELLOW" "Backend API: http://localhost:8001"
}

stop_services() {
    print_color "$BLUE" "Stopping services..."
    docker-compose -f "$DEV_COMPOSE" down 2>/dev/null || true
    docker-compose -f "$PROD_COMPOSE" down 2>/dev/null || true
    print_color "$GREEN" "[OK] Services stopped"
}

show_logs() {
    print_color "$BLUE" "Showing development logs..."
    docker-compose -f "$DEV_COMPOSE" logs -f
}

show_prod_logs() {
    print_color "$BLUE" "Showing production logs..."
    docker-compose -f "$PROD_COMPOSE" logs -f
}

check_health() {
    print_color "$BLUE" "Checking health of services..."

    local backend_ok=false
    if curl -s -f http://localhost:8060/health > /dev/null; then
        print_color "$GREEN" "[OK] Backend (dev) is healthy"
        backend_ok=true
    fi
    if curl -s -f http://localhost:8001/health > /dev/null; then
        print_color "$GREEN" "[OK] Backend (prod) is healthy"
        backend_ok=true
    fi
    if [ "$backend_ok" = false ]; then
        print_color "$RED" "[ERR] Backend is not responding (dev:8060, prod:8001)"
    fi

    local frontend_ok=false
    if curl -s -f http://localhost:5173 > /dev/null; then
        print_color "$GREEN" "[OK] Frontend (dev) is healthy"
        frontend_ok=true
    fi
    if curl -s -f http://localhost:8080 > /dev/null; then
        print_color "$GREEN" "[OK] Frontend (prod) is healthy"
        frontend_ok=true
    fi
    if [ "$frontend_ok" = false ]; then
        print_color "$RED" "[ERR] Frontend is not responding (dev:5173, prod:8080)"
    fi

    if docker-compose -f "$DEV_COMPOSE" exec -T db pg_isready > /dev/null 2>&1; then
        print_color "$GREEN" "[OK] Development database is healthy"
    elif docker-compose -f "$PROD_COMPOSE" exec -T db pg_isready > /dev/null 2>&1; then
        print_color "$GREEN" "[OK] Production database is healthy"
    else
        print_color "$RED" "[ERR] Database is not responding"
    fi
}

clean_up() {
    print_color "$BLUE" "Cleaning up Docker resources..."
    docker-compose -f "$DEV_COMPOSE" down -v --rmi all 2>/dev/null || true
    docker-compose -f "$PROD_COMPOSE" down -v --rmi all 2>/dev/null || true
    docker system prune -f
    print_color "$GREEN" "[OK] Cleanup completed"
}

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
        print_color "$BLUE" "Docker Compose Environment Management"
        echo ""
        print_color "$YELLOW" "Development: $DEV_COMPOSE + .env"
        print_color "$YELLOW" "Production:  $PROD_COMPOSE + .env.production"
        echo ""
        show_usage
        ;;
esac
