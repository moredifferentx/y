#!/usr/bin/env bash
set -e

echo "====================================="
echo " Discord AI Ecosystem — Starting "
echo "====================================="

# Step 1: Environment
./scripts/setup_env.sh

# Step 2: Dependencies
./scripts/install_deps.sh

# Step 3: Migrations
./scripts/migrate.sh

# Step 4: Start services
echo "[start] Launching system..."
python backend/main.py
