#!/bin/bash

# Open Notes - Startup Script
# Starts both frontend and backend servers

echo "🚀 Starting Open Notes..."

# Kill any existing processes on our ports
echo "Cleaning up old processes..."
lsof -ti:8357 | xargs kill -9 2>/dev/null
lsof -ti:36950 | xargs kill -9 2>/dev/null

# Set environment variables
export WEBUI_AUTH=true

# Start backend server
echo "Starting backend server on port 36950..."
cd backend

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install requirements if needed
source venv/bin/activate

# Check if uvicorn is installed
if ! python3 -c "import uvicorn" 2>/dev/null; then
    echo "Installing Python dependencies (this may take a few minutes on first run)..."
    pip install --upgrade pip
    pip install uvicorn fastapi
    # Install other minimal requirements
    pip install -r requirements-minimal.txt 2>/dev/null || true
fi

python3 -m uvicorn open_webui.main:app --port 36950 --host 0.0.0.0 --forwarded-allow-ips '*' --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:36950/health > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    sleep 1
done

# Start frontend server
echo "Starting frontend server on port 8357..."
npm run pyodide:fetch && vite dev --host --port 8357 &
FRONTEND_PID=$!

echo ""
echo "✅ Open Notes is running!"
echo "📝 Frontend: http://localhost:8357"
echo "🔧 Backend API: http://localhost:36950"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to handle shutdown
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $FRONTEND_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    exit 0
}

# Set up trap to handle Ctrl+C
trap cleanup INT

# Keep script running
wait