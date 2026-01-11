#!/usr/bin/env bash
set -e

echo "====================================="
echo " Discord AI Ecosystem — Starting "
echo "====================================="

# -------------------------------------------------
# STEP 1: LOAD ENVIRONMENT (MUST BE IN THIS PROCESS)
# -------------------------------------------------
if [ ! -f ".env" ]; then
  echo "[start] .env not found, creating from .env.example"
  cp .env.example .env
fi

echo "[start] Exporting environment variables from .env"
set -a
source .env
set +a

# Safety check (prevents silent failure)
if [ -z "$ENCRYPTION_KEY" ]; then
  echo "[FATAL] ENCRYPTION_KEY is not set. Check your .env file."
  exit 1
fi

# -------------------------------------------------
# STEP 2: DEPENDENCIES
# -------------------------------------------------
chmod +x scripts/*.sh
./scripts/install_deps.sh

# -------------------------------------------------
# STEP 3: MIGRATIONS
# -------------------------------------------------
./scripts/migrate.sh

# -------------------------------------------------
# STEP 4: START BACKEND
# -------------------------------------------------
echo "[start] Launching system..."
python backend/main.py
