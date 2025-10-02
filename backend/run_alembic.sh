#!/bin/bash

# Script to run Alembic commands with proper environment loading
# Usage: ./run_alembic.sh [alembic command and arguments]
# Example: ./run_alembic.sh revision --autogenerate -m "Initial migration"
# Example: ./run_alembic.sh upgrade head

set -e

# Load environment variables from .env file
if [ -f .env ]; then
    echo "📄 Loading environment from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️  No .env file found. Make sure DATABASE_URL is set in environment."
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set! Please run ./setup_database.sh first."
    exit 1
fi

# Mask password in URL for display
MASKED_URL=$(echo "$DATABASE_URL" | sed 's/:\/\/[^:]*:[^@]*@/:\/\/***:***@/')
echo "🔗 Using DATABASE_URL: $MASKED_URL"

# Run alembic with the provided arguments
echo "🚀 Running: alembic $@"
alembic "$@"
