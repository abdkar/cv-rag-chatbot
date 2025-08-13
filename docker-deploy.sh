#!/bin/bash

# CV RAG Chatbot Docker Deployment Script
# This script helps build and deploy the CV RAG chatbot using Docker

set -e

# Global variables
DOCKER_COMPOSE_AVAILABLE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker."
        exit 1
    fi
    
    # Check for Docker Compose (optional)
    if command_exists docker-compose || docker compose version >/dev/null 2>&1; then
        DOCKER_COMPOSE_AVAILABLE=true
        print_success "Docker and Docker Compose available"
    else
        DOCKER_COMPOSE_AVAILABLE=false
        print_warning "Docker Compose not found. Using Docker-only mode."
        print_success "Docker available"
    fi
}

# Check environment file
check_environment() {
    print_status "Checking environment configuration..."
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
        print_warning "Please edit .env file and add your Google API key"
        return 1
    fi
    
    if grep -q "your_google_api_key_here" .env; then
        print_warning "Please update .env file with your actual Google API key"
        return 1
    fi
    
    print_success "Environment configuration OK"
    return 0
}

# Check required files
check_files() {
    print_status "Checking required files..."
    
    local missing_files=()
    
    if [ ! -f "knowledge_base.txt" ]; then
        missing_files+=("knowledge_base.txt")
    fi
    
    if [ ! -f "phto.jpg" ]; then
        missing_files+=("phto.jpg")
    fi
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        print_error "Missing required files: ${missing_files[*]}"
        print_error "Please add these files before building the container"
        return 1
    fi
    
    print_success "All required files present"
    return 0
}

# Build Docker image
build_image() {
    print_status "Building Docker image..."
    
    if docker build -t cv-rag-chatbot:latest .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Start services
start_services() {
    print_status "Starting services..."
    
    if [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
        print_status "Using Docker Compose..."
        if docker-compose up -d || docker compose up -d; then
            print_success "Services started successfully with Docker Compose"
        else
            print_error "Failed to start services with Docker Compose"
            exit 1
        fi
    else
        print_status "Using Docker only..."
        # Stop any existing container
        docker stop cv-rag-chatbot 2>/dev/null || true
        docker rm cv-rag-chatbot 2>/dev/null || true
        
        # Create and start container
        if docker run -d \
            --name cv-rag-chatbot \
            -p 8501:8501 \
            --env-file .env \
            -v "$(pwd)/knowledge_base.txt:/app/knowledge_base.txt:ro" \
            -v "$(pwd)/phto.jpg:/app/phto.jpg:ro" \
            -v cv-rag-vector-store:/app/vector_store \
            -v cv-rag-logs:/app/logs \
            --restart unless-stopped \
            cv-rag-chatbot:latest; then
            print_success "Container started successfully with Docker"
        else
            print_error "Failed to start container"
            exit 1
        fi
    fi
    
    print_status "Application will be available at: http://localhost:8501"
    print_status "Use './docker-deploy.sh logs' to view logs"
}

# Stop services
stop_services() {
    print_status "Stopping services..."
    
    if [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
        if docker-compose down || docker compose down; then
            print_success "Services stopped successfully with Docker Compose"
        else
            print_error "Failed to stop services with Docker Compose"
            exit 1
        fi
    else
        if docker stop cv-rag-chatbot && docker rm cv-rag-chatbot; then
            print_success "Container stopped successfully"
        else
            print_warning "Container may not have been running"
        fi
    fi
}

# Show logs
show_logs() {
    print_status "Showing container logs..."
    
    if [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
        docker-compose logs -f || docker compose logs -f
    else
        docker logs -f cv-rag-chatbot
    fi
}

# Show status
show_status() {
    print_status "Container status:"
    
    if [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
        docker-compose ps || docker compose ps
    else
        docker ps --filter name=cv-rag-chatbot
    fi
    
    print_status "Testing application health..."
    sleep 5
    
    if curl -f http://localhost:8501/_stcore/health >/dev/null 2>&1; then
        print_success "Application is healthy and responding"
        print_success "Access your CV RAG Chatbot at: http://localhost:8501"
    else
        print_warning "Application may still be starting up..."
        print_status "Check logs with: ./docker-deploy.sh logs"
    fi
}

# Clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    
    # Stop and remove containers
    if [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
        docker-compose down -v || docker compose down -v
    else
        docker stop cv-rag-chatbot 2>/dev/null || true
        docker rm cv-rag-chatbot 2>/dev/null || true
        docker volume rm cv-rag-vector-store cv-rag-logs 2>/dev/null || true
    fi
    
    # Remove image
    docker rmi cv-rag-chatbot:latest 2>/dev/null || true
    
    # Clean system
    docker system prune -f
    
    print_success "Cleanup completed"
}

# Help function
show_help() {
    echo "CV RAG Chatbot Docker Deployment Script"
    echo "======================================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  start     Start the application services"
    echo "  stop      Stop the application services"
    echo "  restart   Restart the application services"
    echo "  logs      Show application logs"
    echo "  status    Show application status"
    echo "  cleanup   Clean up Docker resources"
    echo "  deploy    Full deployment (build + start)"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Build and start the application"
    echo "  $0 logs      # View application logs"
    echo "  $0 stop      # Stop the application"
}

# Main script logic
main() {
    case "${1:-help}" in
        "build")
            check_prerequisites
            check_files
            build_image
            ;;
        "start")
            check_prerequisites
            if ! check_environment; then
                exit 1
            fi
            start_services
            show_status
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            sleep 2
            start_services
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "status")
            show_status
            ;;
        "cleanup")
            cleanup
            ;;
        "deploy")
            check_prerequisites
            if ! check_environment; then
                print_error "Please fix environment configuration first"
                exit 1
            fi
            check_files
            build_image
            start_services
            show_status
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function
main "$@"
