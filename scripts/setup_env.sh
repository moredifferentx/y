#!/usr/bin/env bash

# Ensure .env exists
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "[setup] .env created from template"
else
  echo "[setup] .env already exists"
fi

# Export environment variables so Python can see them
echo "[setup] Loading environment variables from .env"

set -a
source .env
set +a
