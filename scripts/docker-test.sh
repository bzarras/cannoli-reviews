#!/bin/bash

# Script to test Docker build and run locally

set -e

echo "Building Docker image..."
docker build -t cannoli-reviews:test .

echo "Running container..."
docker run -d --name cannoli-reviews-test -p 8001:8001 cannoli-reviews:test

echo "Waiting for container to start..."
sleep 10

echo "Testing health check..."
if curl -f http://localhost:8001/ > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "Visit http://localhost:8001 to see the application"
else
    echo "❌ Application failed to start"
    docker logs cannoli-reviews-test
    exit 1
fi

echo ""
echo "To stop the container:"
echo "docker stop cannoli-reviews-test && docker rm cannoli-reviews-test" 
