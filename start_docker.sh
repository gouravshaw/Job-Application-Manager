#!/bin/bash

echo "===================================="
echo "Job Application Manager - Docker"
echo "===================================="
echo ""
echo "Checking Docker..."

if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed!"
    echo "Please install Docker and try again."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "ERROR: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

echo "Docker is running!"
echo ""
echo "Building and starting containers..."
echo "This may take a few minutes on first run..."
echo ""

docker-compose up --build

echo ""
echo "Application stopped."

