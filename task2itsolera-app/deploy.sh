#!/bin/bash

# Geological Analysis Application Deployment Script
# This script automates the deployment process for the geological analysis application

set -e  # Exit on any error

echo "🚀 Starting Geological Analysis Application Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are available"
}

# Check if required files exist
check_files() {
    print_status "Checking required files..."
    
    required_files=("app.py" "requirements.txt" "Dockerfile" "docker-compose.yml" "nginx.conf")
    missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "Missing required files: ${missing_files[*]}"
        exit 1
    fi
    
    # Check if data directory exists
    if [[ ! -d "task2itsolera" ]]; then
        print_error "Data directory 'task2itsolera' not found"
        exit 1
    fi
    
    print_success "All required files are present"
}

# Stop existing containers
stop_containers() {
    print_status "Stopping existing containers..."
    docker-compose down --remove-orphans 2>/dev/null || true
    print_success "Existing containers stopped"
}

# Build and start containers
deploy_containers() {
    print_status "Building and starting containers..."
    
    # Build the application image
    print_status "Building application image..."
    docker-compose build --no-cache
    
    # Start the services
    print_status "Starting services..."
    docker-compose up -d
    
    print_success "Containers started successfully"
}

# Wait for application to be ready
wait_for_app() {
    print_status "Waiting for application to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -f http://localhost:5000/health &>/dev/null; then
            print_success "Application is ready!"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - Application not ready yet, waiting..."
        sleep 10
        ((attempt++))
    done
    
    print_error "Application failed to start within expected time"
    return 1
}

# Show deployment status
show_status() {
    print_status "Deployment Status:"
    echo ""
    
    # Show running containers
    docker-compose ps
    
    echo ""
    print_status "Application URLs:"
    echo "  - Main Application: http://localhost:5000"
    echo "  - Through Nginx: http://localhost:80"
    echo "  - Health Check: http://localhost:5000/health"
    
    echo ""
    print_status "Useful Commands:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Stop services: docker-compose down"
    echo "  - Restart services: docker-compose restart"
    echo "  - Update and redeploy: ./deploy.sh"
}

# Main deployment function
main() {
    echo "=========================================="
    echo "  Geological Analysis App Deployment"
    echo "=========================================="
    echo ""
    
    # Run deployment steps
    check_docker
    check_files
    stop_containers
    deploy_containers
    
    # Wait for application to be ready
    if wait_for_app; then
        print_success "Deployment completed successfully!"
        echo ""
        show_status
    else
        print_error "Deployment failed!"
        echo ""
        print_status "Checking container logs..."
        docker-compose logs
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "stop")
        print_status "Stopping services..."
        docker-compose down
        print_success "Services stopped"
        ;;
    "restart")
        print_status "Restarting services..."
        docker-compose restart
        print_success "Services restarted"
        ;;
    "logs")
        print_status "Showing logs..."
        docker-compose logs -f
        ;;
    "status")
        show_status
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Deploy the application"
        echo "  stop       Stop all services"
        echo "  restart    Restart all services"
        echo "  logs       Show application logs"
        echo "  status     Show deployment status"
        echo "  help       Show this help message"
        ;;
    *)
        main
        ;;
esac
