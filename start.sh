#!/usr/bin/env bash
set -e

echo "====================================="
echo " Discord AI Ecosystem — Starting "
echo "====================================="

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# -------------------------------------------------
# STEP 1: LOAD ENVIRONMENT (ROOT .env)
# -------------------------------------------------
cd "$ROOT_DIR"

if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    echo "[start] .env not found, creating from .env.example"
    cp .env.example .env
  else
    echo "[FATAL] .env and .env.example not found"
    exit 1
  fi
fi

echo "[start] Loading environment variables"
set -a
source .env
set +a

# Safety checks
if [ -z "$ENCRYPTION_KEY" ]; then
  echo "[FATAL] ENCRYPTION_KEY is not set in .env"
  exit 1
fi

if [ -z "$DISCORD_BOT_TOKEN" ] && [ -z "$DISCORD_TOKEN" ]; then
  echo "[FATAL] DISCORD_BOT_TOKEN is not set in .env"
  exit 1
fi

# -------------------------------------------------
# STEP 2: BACKEND VENV & DEPENDENCIES
# -------------------------------------------------
echo "[start] Preparing backend environment"
cd "$ROOT_DIR/backend"

if [ ! -d "venv" ]; then
  python -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# -------------------------------------------------
# STEP 3: MIGRATIONS (OPTIONAL / SAFE)
# -------------------------------------------------
if [ -f "$ROOT_DIR/scripts/migrate.sh" ]; then
  echo "[start] Running migrations"
  chmod +x "$ROOT_DIR/scripts/migrate.sh"
  "$ROOT_DIR/scripts/migrate.sh" || echo "[warn] migrations skipped"
fi

# -------------------------------------------------
# STEP 4: START BACKEND + DISCORD BOT
# -------------------------------------------------
echo "[start] Launching backend and Discord bot"
python main.py
