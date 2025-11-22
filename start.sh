#!/bin/bash

# Build and start all services
echo "🚀 Building and starting IoT Simulator..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 5

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ IoT Simulator is running!"
echo "🌐 Access the web interface at: http://localhost:5000"
echo "📱 Controls page: http://localhost:5000/control"
echo "📊 Dashboard: http://localhost:5000/dashboard"
echo ""
echo "📝 View logs with: docker-compose logs -f"
echo "🛑 Stop with: docker-compose down"
