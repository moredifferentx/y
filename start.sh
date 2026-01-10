#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Discord AI Chatbot - Startup Script"
echo "========================================"

ROOT=$(cd "$(dirname "$0")" && pwd)
VENVDIR="$ROOT/.venv"

# Step 1: Create virtual environment
echo "📦 Setting up Python virtual environment..."
if [ ! -d "$VENVDIR" ]; then
  python3 -m venv "$VENVDIR"
  echo "✓ Virtual environment created"
else
  echo "✓ Virtual environment already exists"
fi

# Step 2: Activate venv
source "$VENVDIR/bin/activate"
echo "✓ Virtual environment activated"

# Step 3: Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip -q

# Step 4: Install dependencies
echo "📥 Installing dependencies..."
pip install -r "$ROOT/requirements.txt" -q
echo "✓ Dependencies installed"

# Step 5: Check environment
echo "🔍 Checking environment..."
if [ ! -f "$ROOT/.env" ]; then
  echo "⚠️  .env file not found!"
  echo "   Copy .env.example to .env and fill in your tokens:"
  echo "   cp .env.example .env"
  exit 1
fi

# Check for Discord token
if ! grep -q "DISCORD_BOT_TOKEN=" "$ROOT/.env"; then
  echo "⚠️  Warning: DISCORD_BOT_TOKEN not set in .env"
  echo "   Discord bot will not start without it"
fi

# Step 6: Create required directories
echo "📁 Creating directories..."
mkdir -p "$ROOT/logs"
mkdir -p "$ROOT/plugins"
mkdir -p "$ROOT/languages"

# Step 7: Show startup info
echo ""
echo "✨ All set! Starting bot..."
echo "========================================"
echo "📡 FastAPI Dashboard: http://localhost:8000/static/index.html"
echo "🤖 Discord Bot: Connecting..."
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

# Step 8: Load environment and start
export PYTHONUNBUFFERED=1
cd "$ROOT"
python3 -m backend.app

