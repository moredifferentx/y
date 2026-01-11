#!/usr/bin/env bash

mkdir -p data

if [ ! -f data/memory.db ]; then
  echo "[migrate] Initializing memory database"
  sqlite3 data/memory.db < migrations/memory.sql
else
  echo "[migrate] Memory database already exists"
fi
