#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$PROJECT_DIR" || exit 1

# Start FastAPI backend
osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR' && source .venv/bin/activate && python -m uvicorn src.api:app --reload\""

# Start React frontend
osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR/frontend' && npm run dev\""

# Wait for the servers to start
sleep 3

# Open the dashboard
open "http://localhost:5173"