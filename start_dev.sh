#!/bin/bash
# This script starts the development environment for the easyapi-crud-demo.

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to clean up background processes on exit
cleanup() {
    echo "Shutting down backend server..."
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID
    fi
    exit
}

# Trap SIGINT and SIGTERM to run the cleanup function
trap cleanup SIGINT SIGTERM

# --- Backend Setup ---
echo "--- Setting up and starting backend ---"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
echo "Installing backend dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

# Start backend server in the background
echo "Starting backend server on http://localhost:8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID. Logs are in backend.log"
cd ..

# --- Frontend Setup ---
echo ""
echo "--- Setting up and starting frontend ---"
cd frontend

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm ci

# Start frontend dev server
echo "Starting frontend development server..."
echo "View the application at http://localhost:5173 (or the URL provided by Vite)"
echo "Press Ctrl+C to stop both frontend and backend servers."
VITE_API_BASE=http://localhost:8000 npm run dev

# The script will wait here until the user stops the frontend server.
# The trap will then trigger the cleanup function.