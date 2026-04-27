#!/usr/bin/env bash
# Bootstrap script to run on an EC2 instance (Amazon Linux 2 / Ubuntu)
# Usage: scp this file to EC2, then: chmod +x deploy-backend.sh && ./deploy-backend.sh
set -e

echo "→ Installing Python 3 & pip..."
sudo apt-get update -y && sudo apt-get install -y python3 python3-pip python3-venv || \
  sudo yum install -y python3 python3-pip

echo "→ Copying backend files..."
# Assumes backend/ directory is in the same location as this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../backend"

cd "$BACKEND_DIR"

echo "→ Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "→ Installing dependencies..."
pip install -r requirements.txt

echo "→ Starting FastAPI with uvicorn on port 8000..."
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
echo "✓ Backend running. PID: $!"
echo "  Logs: $BACKEND_DIR/uvicorn.log"
echo "  Health check: curl http://localhost:8000/health"
