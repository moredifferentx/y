#!/usr/bin/env bash

echo "[dev] Starting backend + frontend (dev mode)"

# Backend
python backend/main.py &

# Frontend
cd frontend || exit 1
npm run dev
