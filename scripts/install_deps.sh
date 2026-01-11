#!/usr/bin/env bash

echo "[deps] Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "[deps] Installing frontend dependencies..."
cd frontend || exit 1
npm install
cd ..
