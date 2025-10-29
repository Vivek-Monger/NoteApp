#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration - Update these with your Docker Hub username
DOCKER_HUB_USERNAME="your-dockerhub-username"
IMAGE_NAME="noteapp"
IMAGE_TAG="latest"

echo -e "${BLUE}=== Django NoteApp Docker Setup ===${NC}\n"

# Function to display usage
usage() {
    echo "Usage: $0 [build|run|stop|push|help]"
    echo ""
    echo "Commands:"
    echo "  build  - Build the Docker image"
    echo "  run    - Build and run the container"
    echo "  stop   - Stop and remove the container"
    echo "  push   - Build, tag, and push to Docker Hub"
    echo "  help   - Show this help message"
    exit 1
}

# Function to build the image
build_image() {
    echo -e "${BLUE}Building Docker image...${NC}"
    docker-compose build
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Image built successfully!${NC}"
    else
        echo -e "${RED}✗ Failed to build image${NC}"
        exit 1
    fi
}

# Function to run the container
run_container() {
    echo -e "${BLUE}Starting container...${NC}"
    docker-compose up -d
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Container started successfully!${NC}"
        echo -e "${YELLOW}App is running at: http://localhost:8000${NC}"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: ./run_docker.sh stop"
    else
        echo -e "${RED}✗ Failed to start container${NC}"
        exit 1
    fi
}

# Function to stop the container
stop_container() {
    echo -e "${BLUE}Stopping and removing container...${NC}"
    docker-compose down
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Container stopped successfully!${NC}"
    else
        echo -e "${RED}✗ Failed to stop container${NC}"
        exit 1
    fi
}

# Function to push to Docker Hub
push_to_dockerhub() {
    # Check if username is set
    if [ "$DOCKER_HUB_USERNAME" == "your-dockerhub-username" ]; then
        echo -e "${RED}✗ Please update DOCKER_HUB_USERNAME in this script first!${NC}"
        echo "Edit run_docker.sh and replace 'your-dockerhub-username' with your Docker Hub username"
        exit 1
    fi
    
    FULL_IMAGE_NAME="$DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG"
    
    echo -e "${BLUE}Building image for Docker Hub...${NC}"
    docker build -t $FULL_IMAGE_NAME .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Image built successfully!${NC}"
        
        echo -e "${YELLOW}You need to login to Docker Hub first${NC}"
        echo "Run: docker login"
        read -p "Press Enter when you're logged in..."
        
        echo -e "${BLUE}Pushing image to Docker Hub...${NC}"
        docker push $FULL_IMAGE_NAME
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Image pushed successfully!${NC}"
            echo "Image URL: docker.io/$FULL_IMAGE_NAME"
        else
            echo -e "${RED}✗ Failed to push image${NC}"
            exit 1
        fi
    else
        echo -e "${RED}✗ Failed to build image${NC}"
        exit 1
    fi
}

# Main script logic
case "$1" in
    build)
        build_image
        ;;
    run)
        build_image
        run_container
        ;;
    stop)
        stop_container
        ;;
    push)
        push_to_dockerhub
        ;;
    help|--help|-h)
        usage
        ;;
    "")
        echo -e "${YELLOW}No command specified. Running 'run' by default...${NC}\n"
        build_image
        run_container
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}\n"
        usage
        ;;
esac

