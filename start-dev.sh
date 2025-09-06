#!/bin/bash

# Hackathon Management System - Development Startup Script

echo "🚀 Starting Hackathon Management System..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "❌ .env file not found!"
    exit 1
fi

# Check if port is in use and kill any existing processes
PORT=${PORT:-3001}
echo "🔍 Checking port $PORT..."

# Find and kill any processes using the port
PIDS=$(lsof -ti:$PORT)
if [ ! -z "$PIDS" ]; then
    echo "⚠️  Port $PORT is in use by process(es): $PIDS"
    echo "🔄 Killing existing processes..."
    kill -9 $PIDS
    sleep 2
    echo "✅ Port $PORT is now free"
fi

# Ensure database connection is ready
echo "🔗 Verifying database connection..."
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set!"
    exit 1
fi

echo "✅ Database URL configured"
echo "📍 Database: $(echo $DATABASE_URL | cut -d'@' -f2 | cut -d'/' -f1)"

# Start the development server
echo "🎯 Starting development server on port $PORT..."
npm run dev
