#!/usr/bin/env bash
set -e
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"
echo "========================================"
echo "           TRACE LAUNCHER"
echo "========================================"
if [ ! -x ".venv/bin/python" ]; then
    echo "ERROR: Python virtual environment not found."
    echo "Create it using: python3 -m venv .venv"
    exit 1
    
fi
if [ ! -f "frontend/package.json" ]; then
    echo "ERROR: frontend/package.json not found."
    exit 1
    
fi
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    (
        cd frontend
        npm install
    )
    
fi
echo "Starting TRACE backend..."
.venv/bin/python -m uvicorn src.api:app --reload \
    > trace-backend.log 2>&1 &

BACKEND_PID=$!
echo "Starting TRACE frontend..."
(
    cd frontend
    npm run dev
) > trace-frontend.log 2>&1 &

FRONTEND_PID=$!
cleanup() {
    echo "Stopping TRACE..."
    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    exit 0
}
trap cleanup INT TERM
echo "Waiting for services..."
sleep 5
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:5173" >/dev/null 2>&1 &
elif command -v open >/dev/null 2>&1; then
    open "http://localhost:5173"
fi
echo "TRACE dashboard: http://localhost:5173"
echo "Backend logs: trace-backend.log"
echo "Frontend logs: trace-frontend.log"
echo "Press Ctrl+C to stop TRACE."
wait
