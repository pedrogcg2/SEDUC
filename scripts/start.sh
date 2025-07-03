#!/bin/bash

# SEDUC Docker Startup Script

set -e

echo "🚀 Starting SEDUC with Docker Compose..."

# Function to wait for database to be ready
wait_for_db() {
    echo "⏳ Waiting for PostgreSQL to be ready..."
    until docker-compose exec -T postgres pg_isready -U master -d sqldb-seduc; do
        echo "Database is not ready yet. Waiting..."
        sleep 2
    done
    echo "✅ PostgreSQL is ready!"
}

# Function to initialize database
init_database() {
    echo "🗄️  Initializing database..."
    docker-compose exec -T api python init_db.py
    echo "✅ Database initialized!"
}

# Function to check if database is already initialized
check_db_initialized() {
    docker-compose exec -T postgres psql -U master -d sqldb-seduc -c "SELECT COUNT(*) FROM users;" > /dev/null 2>&1
    return $?
}

# Initialize the database and create tables
python3 api/init_db.py

# Seed the database with initial data
python3 data/seed.py

# Start services
echo "📦 Starting services..."
docker-compose up -d postgres

# Wait for database
wait_for_db

# Check if database needs initialization
if ! check_db_initialized; then
    echo "🔄 Database needs initialization..."
    init_database
else
    echo "✅ Database already initialized"
fi

# Start API
echo "🌐 Starting API..."
docker-compose up -d api

echo "🎉 SEDUC is running!"
echo ""
echo "📋 Services:"
echo "  • API: http://localhost:5000"
echo "  • PostgreSQL: localhost:5432"
echo "  • pgAdmin: http://localhost:8080 (optional)"
echo ""
echo "🔑 Default admin credentials:"
echo "  • Username: admin"
echo "  • Password: admin123"
echo ""
echo "📝 Useful commands:"
echo "  • View logs: docker-compose logs -f"
echo "  • Stop services: docker-compose down"
echo "  • Restart: docker-compose restart" 