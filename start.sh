#!/bin/bash

echo "=========================================="
echo "🚗 Starting Ride-Sharing Optimizer"
echo "=========================================="
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check prerequisites
if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed"
    exit 1
fi

# Kill any existing processes on ports 5000 and 5173
echo "🔍 Checking for existing processes..."
lsof -ti:5000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Start backend in background
echo "🐍 Starting backend server on port 5000..."
python3 app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start. Check backend.log for details."
    exit 1
fi

echo "✓ Backend server started (PID: $BACKEND_PID)"

# Start frontend
echo "⚛️  Starting frontend on port 5173..."
echo ""
echo "=========================================="
echo "✅ Application is starting!"
echo "=========================================="
echo ""
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "=========================================="
echo ""

# Trap Ctrl+C to kill both processes
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID; exit" INT

# Start frontend (this will keep the script running)
npm run dev

# If npm run dev exits, kill backend
kill $BACKEND_PID
