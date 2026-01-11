#!/usr/bin/env bash

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[setup] .env created from template"
else
  echo "[setup] .env already exists"
fi
